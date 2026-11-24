#!/usr/bin/env python3
"""Build timeline.json for the Remotion long form from Sean's spec plan, Grok's approved layers
and the real Ryan Kurk narration timings. Every shot is retimed to the voice (never the voice to the shots)."""
import json, os, shutil, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
G = ROOT / "grok_src/edit"
PUB = ROOT / "public"; (PUB / "layers").mkdir(parents=True, exist_ok=True)
FPS = 30
plan = json.load(open(G / "plan_raw.json"))
pts = json.load(open(G / "points.json"))["glove"]
vo = json.load(open(ROOT / "vo_sections.json"))

# section lengths: voice plus a short pad; payoff keeps its action length; board gets a screenshot hold
pads = {"HOOK": 0.55, "SELF TEST": 0.6, "PAYOFF AT SPEED": None, "STEP 1": 0.6, "STEP 2": 0.6, "STEP 3": 0.6, "COMBO AND RETEST": 0.6, "SUMMARY BOARD": 1.6, "CALL TO ACTION": 0.6}
sections = []
t = 0.0
for s in vo:
    L = 6.0 if s["name"] == "PAYOFF AT SPEED" else s["dur"] + pads[s["name"]]
    lead = 0.0 if s["name"] == "HOOK" else 0.12   # first narration word at 0:00 (R14)
    sections.append({"name": s["name"], "spec": [s["spec_start"], s["spec_end"]], "start": round(t, 3), "len": round(L, 3), "vo": f"vo/sec{vo.index(s)}.mp3", "vo_at": round(t + lead, 3),
                     "words": [{"w": w["w"], "s": round(t + lead + w["s"], 3), "e": round(t + lead + w["e"], 3)} for w in s["words"]]})
    t += L
sub_start = t; total = t + 3.2  # SUBSCRIBE card holds over 3 s after the CTA ends
sections.append({"name": "SUBSCRIBE", "spec": [147, 150], "start": round(sub_start, 3), "len": 3.2, "words": []})

def section_of(spec_t):
    for s in sections:
        if s["spec"][0] <= spec_t < s["spec"][1]: return s
    return sections[-1]

def vt(spec_t, sec):  # spec time -> video time inside the section
    a, b = sec["spec"]; return sec["start"] + (spec_t - a) * sec["len"] / (b - a)

shots = []
for p in plan:
    sec = section_of(p["start"])
    a, b = vt(p["start"], sec), vt(min(p["end"], sec["spec"][1]), sec)
    sid = p["id"]; info = json.load(open(G / "v4layers" / f"{sid}.json")) if (G / "v4layers" / f"{sid}.json").exists() else {}
    layers = {}
    for k in ("base", "a", "lines"):
        f = G / "v4layers" / f"{sid}_{k}.png"
        if f.exists():
            dst = PUB / "layers" / f"{sid}_{k}.png"
            if not dst.exists(): shutil.copy2(f, dst)
            layers[k] = f"layers/{sid}_{k}.png"
    shots.append({"id": sid, "section": sec["name"], "start": round(a, 3), "end": round(b, 3), "angle": p["angle"], "flags": p["flags"],
                  "text": [x.strip() for x in p["text_spec"].split(" / ")] if p["text_spec"] else [], "dose": p["dose"], "layers": layers,
                  "glove": pts.get(sid), "phase_frames": {"V2": 12, "V3": 22}.get(sid, 0)})

# 2026-11-24 combat accuracy fix: 22 stills replaced (rig pose redraws, arm edits, mirrors, barefoot edits).
# New glove points and speed lines (relines.py), old chamber layers dropped, truthful angle labels, base framing for variety.
FIX = json.load(open(Path(__file__).parent / "glove_fix.json"))
ANG = {"V2": "close up contact ribs", "V3": "rear three quarter", "V9": "rear three quarter wide", "V15": "high rear three quarter",
       "V20": "side jab to the guard", "V21": "low rear three quarter", "V23": "tight rear three quarter", "V24": "medium side shovel",
       "V33": "wide rear three quarter", "V34": "close up contact low", "V53": "tight contact high", "V70": "close up shovel contact",
       "V79": "close up shovel elbow", "V84": "medium three quarter", "V86": "rear three quarter", "V88": "full body side shovel", "V94": "medium rear three quarter"}
BZ = {"V23": 1.45, "V53": 1.6, "V94": 1.25, "V33": 0.0, "V86": 1.15}
for sh in shots:
    if sh["id"] in FIX:
        sh["glove"] = FIX[sh["id"]]; sh["layers"].pop("a", None); sh["phase_frames"] = 0
        sh["angle"] = ANG[sh["id"]]
        if BZ.get(sh["id"]): sh["bz"] = BZ[sh["id"]]

# cold open: frame one is action already landing (R14, retention data: drops at 0:01 to 0:03). Swap V1 and V2.
i1, i2 = next(i for i, s in enumerate(shots) if s["id"] == "V1"), next(i for i, s in enumerate(shots) if s["id"] == "V2")
s1, s2 = shots[i1], shots[i2]
d2 = s2["end"] - s2["start"]
s2["start"], s2["end"] = 0.0, round(d2, 3)
s1["start"], s1["end"] = round(d2, 3), round(d2 + (s1["end"] - s1["start"]), 3)
s2["text"], s1["text"] = s1["text"], []  # the hook text lands with the punch
s2["phase_frames"] = 0  # start on contact, not on the start pose
shots[i1], shots[i2] = s2, s1

# tidy: contiguous, frame aligned
shots.sort(key=lambda s: s["start"])
for k, s in enumerate(shots):
    s["from"] = round(s["start"] * FPS)
    s["to"] = round(shots[k + 1]["start"] * FPS) if k + 1 < len(shots) else round(total * FPS)
    s["dur"] = s["to"] - s["from"]
json.dump({"fps": FPS, "frames": round(total * FPS), "sections": sections, "shots": shots}, open(PUB / "timeline.json", "w"), indent=1)
holds = [s["dur"] / FPS for s in shots]
print(f"total {total:.2f}s, {len(shots)} shots, mean hold {sum(holds)/len(holds):.2f}s, max {max(holds):.2f}s ({[s['id'] for s in shots if s['dur']/FPS == max(holds)]}), min {min(holds):.2f}s")
for s in sections: print(f"  {s['name']:18} {s['start']:7.2f} len {s['len']:6.2f}")

# ---------------- sound map (spec: whoosh tick on at speed cuts, soft impact on landings, none in self test or CTA, never on a narration word)
words = [w for s in sections for w in s["words"]]
# Sean 2026-11-24: the "tick never sits on a narration word" rule is REMOVED. SFX land on their exact frame.
def on_word(t, pad=0.04): return False
def nearest_gap(t, max_shift=0.25):
    for d in [0] + [x / 100 for x in range(2, int(max_shift * 100) + 1, 2) for _ in (0, 1)]:
        for c in (t - d, t + d):
            if c >= 0 and not on_word(c): return c
    return None
quiet = {"SELF TEST", "CALL TO ACTION", "SUBSCRIBE"}
sfx, dropped = [], []
for k, s in enumerate(shots):
    if s["section"] in quiet: continue
    if s["section"] in ("PAYOFF AT SPEED",) or (s["section"] == "COMBO AND RETEST" and s["from"] < round((sections[6]["start"] + 7) * FPS)):
        t0 = s["from"] / FPS - 0.05; g = nearest_gap(t0)
        (sfx.append({"type": "whoosh", "frame": round(g * FPS)}) if g is not None else dropped.append(("whoosh", s["id"])))
    if s["glove"]:
        t0 = (s["from"] + s["phase_frames"]) / FPS; g = nearest_gap(t0)
        (sfx.append({"type": "impact", "frame": round(g * FPS)}) if g is not None else dropped.append(("impact", s["id"])))
tl = json.load(open(PUB / "timeline.json")); tl["sfx"] = sfx
tl["music_lifts"] = [round(sections[i]["start"] * FPS) for i in (3, 4, 5, 6)]
json.dump(tl, open(PUB / "timeline.json", "w"), indent=1)
print(f"sfx placed {len(sfx)} ({sum(e['type']=='whoosh' for e in sfx)} whoosh, {sum(e['type']=='impact' for e in sfx)} impact), dropped because every nearby moment had a spoken word: {dropped}")
