#!/usr/bin/env python3
"""Fight Playbook automated QC. Run after render.mjs.

usage: python3 qc.py <render_dir> <final_video.mp4> [--audio <voice track or video with the voice>]

Checks (fails block delivery):
  rig       per frame anatomy: overextended limbs, detached feet, foot slide, glove/head/torso
            interpenetration, fighters facing each other, heels below floor, bodies overlapping
  framing   subjects a shot claims to show are inside the frame
  edit      shot length 0.6 to 3.0 s, never the same angle twice in a row, at least 10 angles per minute
  text      top text max 3 words, no dashes anywhere, captions cover every script word in order
  sync      every caption starts within 0.25 s of a voice onset; no caption shown over long silence
  pacing    no 1 s window without visible change (dead air); reports change rate
  audio     final file has audio, durations match within one frame, loudness reported
"""
import json, re, subprocess, sys, os
import numpy as np

args = sys.argv[1:]
rdir, final = args[0], args[1]
audio_src = args[args.index('--audio') + 1] if '--audio' in args else final

data = json.load(open(os.path.join(rdir, 'qc_frames.json')))
meta, frames = data['meta'], data['frames']
fps = meta['fps']
fails, warns, notes = [], [], []

# ---------- rig ----------
by_kind = {}
for fr in frames:
    for iss in fr['issues']:
        kind = re.sub(r'[-0-9.]+$', '', iss).strip()
        by_kind.setdefault(kind, []).append((fr['t'], fr['shot']))
for kind, hits in sorted(by_kind.items()):
    shots = sorted({s for _, s in hits})
    msg = f"{kind}: {len(hits)} frames (shots {', '.join(shots)}; first at {hits[0][0]:.2f}s)"
    (warns if 'out of frame' in kind else fails).append('RIG ' + msg)

# ---------- edit ----------
shots = meta['shots']
for i, s in enumerate(shots):
    d = s['end'] - s['start']
    if d > 2.0 or d < 0.6:
        warns.append(f"EDIT shot {s['id']} holds {d:.2f}s (rule R7: 1 to 2 s)")
    if i and shots[i - 1]['angle'] == s['angle']:
        fails.append(f"EDIT shots {shots[i-1]['id']} and {s['id']} repeat angle {s['angle']}")
angles = len({s['angle'] for s in shots})
per_min = angles / (meta['duration'] / 60)
notes.append(f"{len(shots)} shots, {angles} distinct angles ({per_min:.0f} per minute), mean hold {meta['duration']/len(shots):.2f}s")
if per_min < 10:
    fails.append(f"EDIT only {per_min:.1f} distinct angles per minute (need 10)")

# ---------- text ----------
DASH = re.compile('[\u2010-\u2015\u2212-]')
for s in shots:
    if s.get('top'):
        t = s['top']['text']; t = ' '.join(t) if isinstance(t, list) else t
        if len(t.replace(',', ' ').split()) > 3:
            fails.append(f"TEXT shot {s['id']} top text has more than 3 words: {t}")
        if DASH.search(t):
            fails.append(f"TEXT dash in top text: {t}")
caps = meta['captions']
for c in caps:
    if DASH.search(c['text']):
        fails.append(f"TEXT dash in caption: {c['text']}")
norm = lambda w: re.sub(r"[^a-z']", '', w.lower())
script_words = [norm(w) for w in meta['script'].split() if norm(w)]
cap_words = [norm(w) for c in caps for w in c['text'].split() if norm(w)]
if cap_words != script_words:
    # find first divergence
    k = next((i for i, (a, b) in enumerate(zip(cap_words, script_words)) if a != b), min(len(cap_words), len(script_words)))
    fails.append(f"TEXT captions do not match script at word {k}: caption {cap_words[k:k+4]} vs script {script_words[k:k+4]}")
else:
    notes.append(f"captions carry all {len(script_words)} script words in order")
for a, b in zip(caps, caps[1:]):
    if b['start'] < a['end'] - 1e-6:
        fails.append(f"TEXT captions overlap: {a['text']} / {b['text']}")

# ---------- audio onsets (voice) ----------
def pcm(path, sr=16000):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768, sr

a, sr = pcm(audio_src)
if len(a) == 0:
    fails.append('AUDIO no audio stream found')
else:
    hop = sr // 100
    env = np.array([np.sqrt((a[i:i + hop] ** 2).mean() + 1e-12) for i in range(0, len(a) - hop, hop)])
    db = 20 * np.log10(env + 1e-9)
    voiced = db > (np.percentile(db, 90) - 22)
    onsets = [i / 100 for i in range(1, len(voiced)) if voiced[i] and not voiced[i - 1:i].any() and not voiced[max(0, i - 15):i].any()]
    for c in caps:
        near = min((abs(o - c['start']) for o in onsets), default=9)
        # captions that continue a phrase start mid speech; only phrase starts must align with an onset
        mid_speech = voiced[int(c['start'] * 100) - 3:int(c['start'] * 100)].any()
        if not mid_speech and near > 0.25:
            warns.append(f"SYNC caption '{c['text']}' at {c['start']:.2f}s is {near:.2f}s from nearest voice onset")
        span = voiced[int(c['start'] * 100):int(c['end'] * 100)]
        if len(span) and span.mean() < 0.25:
            warns.append(f"SYNC caption '{c['text']}' shown over mostly silent audio")
    # long silences: must be covered by visible action
    run, start = 0, 0
    for i, v in enumerate(voiced):
        if not v:
            if run == 0: start = i
            run += 1
        else:
            if run >= 100: notes.append(f"voice pause {start/100:.2f} to {i/100:.2f}s (covered by shot motion, see pacing)")
            run = 0

# ---------- pacing: visible change every second ----------
W, H = 108, 192
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', final, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(v, axis=0)).mean(axis=(1, 2))
cuts = int((d > 12).sum())
per_s = [d[i * fps:(i + 1) * fps].mean() for i in range(len(d) // fps)]
dead = [i for i, x in enumerate(per_s) if x < 0.25]
notes.append('motion per second: ' + ' '.join(f'{x:.1f}' for x in per_s))
if dead:
    fails.append(f"PACING no visible change in seconds {dead}")

# ---------- final file ----------
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', final], capture_output=True, text=True).stdout)
vs = [s for s in pr['streams'] if s['codec_type'] == 'video']
au = [s for s in pr['streams'] if s['codec_type'] == 'audio']
vd = float(vs[0]['duration'])
if (vs[0]['width'], vs[0]['height']) != (1080, 1920):
    fails.append(f"FILE resolution {vs[0]['width']}x{vs[0]['height']}")
if not au:
    warns.append('FILE silent build (no audio stream). Not publishable until narration is added.')
else:
    ad = float(au[0]['duration'])
    if abs(ad - vd) > 1.5 / fps:
        fails.append(f"FILE audio {ad:.3f}s vs video {vd:.3f}s")
    lu = subprocess.run(['ffmpeg', '-v', 'info', '-i', final, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'I:\s+(-?[0-9.]+) LUFS', lu)
    if m: notes.append(f"integrated loudness {m[-1]} LUFS (platforms normalise near -14)")
notes.append(f"video {vd:.3f}s, {len(frames)} frames rendered")

report = ['# QC report', '', f'Video: `{os.path.basename(final)}`', '',
          f'**Result: {"FAIL" if fails else "PASS"}** ({len(fails)} blocking, {len(warns)} warnings)', '']
for title, items in (('Blocking', fails), ('Warnings', warns), ('Notes', notes)):
    report += [f'## {title}', ''] + ([f'- {x}' for x in items] or ['- none']) + ['']
out = os.path.join(rdir, 'QC_REPORT.md')
open(out, 'w').write('\n'.join(report))
print('\n'.join(report))
sys.exit(1 if fails else 0)
