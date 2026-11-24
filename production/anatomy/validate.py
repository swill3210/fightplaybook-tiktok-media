#!/usr/bin/env python3
"""Fight Playbook anatomy validator (automated half of the combat anatomy gate).

Runs whole body pose estimation on CPU (rtmlib: YOLOX HumanArt detector + RTMW/DWPose style whole body model, ONNX)
and checks every person for: count (ghost or merged figures), identity colours (hero navy shorts, opponent red top),
limb visibility, limb proportions, folded joints, torso left/right consistency, the technique's measurable signature,
distance to the rig reference skeleton (same camera), and for frame sequences, sudden anatomical changes.

Verdicts per check: PASS, UNCERTAIN, FAIL. The asset verdict is FAIL if any check fails, UNCERTAIN if any is uncertain.
UNCERTAIN is a rejection until the combat-anatomy-specialist clears it by visual inspection. A PASS here is NOT proof
of anatomical accuracy: pose models are trained on photos, our characters are stylised, and 2D projection hides
bends (a 90 degree hook seen from behind projects as a straight line). Always pair with visual inspection.

usage:
  python3 validate.py IMG_OR_DIR [--technique jab|cross|hook|shovel|guard|none] [--expect-persons 2]
                      [--reference rig_still.json] [--sequence] [--out report.json] [--overlay DIR]
"""
import argparse, glob, json, math, os, sys
import numpy as np

KP = ['nose', 'leye', 'reye', 'lear', 'rear', 'lsho', 'rsho', 'lelb', 'relb', 'lwri', 'rwri', 'lhip', 'rhip', 'lknee', 'rknee', 'lank', 'rank']
I = {n: i for i, n in enumerate(KP)}
LIMBS = {'left arm': ('lsho', 'lelb', 'lwri'), 'right arm': ('rsho', 'relb', 'rwri'), 'left leg': ('lhip', 'lknee', 'lank'), 'right leg': ('rhip', 'rknee', 'rank')}
BODY = list(range(5, 17))
VIS = 0.30          # keypoint score below this counts as not seen
PERSON = 0.35       # mean body score for a detection to count as a person
# technique signatures for the hero: punching arm and what can be measured in 2D (always view dependent)
TECH = {'jab': ('left', 'straight'), 'cross': ('right', 'straight'), 'hook': ('left', 'bent'), 'shovel': ('right', 'up'), 'guard': (None, None), 'none': (None, None)}

_model = None
def model():
    global _model
    if _model is None:
        from rtmlib import Wholebody
        _model = Wholebody(mode='balanced', backend='onnxruntime', device='cpu')
    return _model

def P(k, n): return np.array(k[I[n]][:2], float)
def dist(a, b): return float(np.linalg.norm(a - b))
def angle(a, b, c):
    u, v = a - b, c - b; d = np.linalg.norm(u) * np.linalg.norm(v)
    return float(math.degrees(math.acos(np.clip(np.dot(u, v) / d, -1, 1)))) if d > 1e-6 else float('nan')

def check(name, status, detail): return {'check': name, 'status': status, 'detail': detail}

def identity(img, k, s):
    """Role from clothing colour: opponent wears a red top; hero has navy shorts and a black top."""
    h, w = img.shape[:2]
    sh = (P(k, 'lsho') + P(k, 'rsho')) / 2; hp = (P(k, 'lhip') + P(k, 'rhip')) / 2
    def patch(c, r):
        x0, x1 = int(max(0, c[0] - r)), int(min(w, c[0] + r)); y0, y1 = int(max(0, c[1] - r)), int(min(h, c[1] + r))
        return img[y0:y1, x0:x1].reshape(-1, 3) if x1 > x0 and y1 > y0 else np.zeros((1, 3))
    T = max(dist(sh, hp), 20)
    top = patch(sh + (hp - sh) * 0.45, T * 0.18); shorts = patch(hp + (hp - sh) * 0.25, T * 0.15)
    b, g, r = top[:, 0].astype(int), top[:, 1].astype(int), top[:, 2].astype(int)
    red = float(np.mean((r > 140) & (g < 90) & (b < 90)))
    sb, sg, sr = shorts[:, 0].astype(int), shorts[:, 1].astype(int), shorts[:, 2].astype(int)
    navy = float(np.mean((sb > sr + 15) & (sb > 45) & (sr < 90)))
    role = 'opponent' if red > 0.35 else 'hero' if navy > 0.25 else 'unknown'
    return role, {'red_top': round(red, 2), 'navy_shorts': round(navy, 2)}

def person_checks(img, k, s, technique):
    out = []
    sh = (P(k, 'lsho') + P(k, 'rsho')) / 2; hp = (P(k, 'lhip') + P(k, 'rhip')) / 2; T = dist(sh, hp)
    if T < 10 or min(s[I['lsho']], s[I['rsho']], s[I['lhip']], s[I['rhip']]) < VIS:
        return [check('torso', 'UNCERTAIN', 'torso keypoints not seen with confidence')], T
    for limb, (a, b, c) in LIMBS.items():
        sc = [s[I[a]], s[I[b]], s[I[c]]]
        if min(sc) < VIS:
            out.append(check(f'{limb} visible', 'UNCERTAIN', f'scores {[round(x, 2) for x in sc]}: occluded, cropped or missing'))
            continue
        s1, s2 = dist(P(k, a), P(k, b)) / T, dist(P(k, b), P(k, c)) / T
        if max(s1, s2) > 1.15: out.append(check(f'{limb} length', 'FAIL', f'segment {max(s1, s2):.2f} x torso (stretched)'))
        elif min(s1, s2) >= 0.25 and not ((0.45 <= s1 / s2 <= 2.2) if 'arm' in limb else (0.4 <= s1 / s2 <= 2.6)): out.append(check(f'{limb} proportion', 'UNCERTAIN', f'upper/lower {s1 / s2:.2f}'))
        else: out.append(check(f'{limb} proportion', 'PASS', f'upper {s1:.2f}, lower {s2:.2f} x torso'))
        ang = angle(P(k, a), P(k, b), P(k, c))
        # arms: a tight guard folds the elbow to 5 to 20 degrees in 2D, so only knees get a fold check (calibration 2026-11-24)
        if 'leg' in limb and ang < 12: out.append(check(f'{limb} joint', 'UNCERTAIN', f'{ang:.0f} degrees: knee folded beyond normal range'))
    v1 = P(k, 'rsho') - P(k, 'lsho'); v2 = P(k, 'rhip') - P(k, 'lhip')
    if float(np.dot(v1, v2)) < 0: out.append(check('torso left/right', 'UNCERTAIN', 'shoulder and hip lines point opposite ways: twist past 90 degrees or swapped sides'))
    else: out.append(check('torso left/right', 'PASS', 'shoulders and hips agree'))
    return out, T

def tech_check(k, s, technique):
    out = []
    side, sig = TECH.get(technique, (None, None))
    if side:
        p = 'l' if side == 'left' else 'r'
        if min(s[I[p + 'sho']], s[I[p + 'elb']], s[I[p + 'wri']]) < VIS:
            out.append(check(f'{technique} arm', 'UNCERTAIN', f'{side} arm not measurable'))
        else:
            e = angle(P(k, p + 'sho'), P(k, p + 'elb'), P(k, p + 'wri'))
            fa = P(k, p + 'wri') - P(k, p + 'elb'); up = math.degrees(math.atan2(-fa[1], abs(fa[0]) + 1e-6))
            if sig == 'straight': st = 'PLAUSIBLE' if e >= 150 else 'UNCERTAIN'
            elif sig == 'bent': st = 'PLAUSIBLE' if e <= 130 else 'UNCERTAIN'
            else: st = 'PLAUSIBLE' if up >= 55 else 'UNCERTAIN'
            out.append(check(f'{technique} signature (2D, view dependent)', st, f'{side} elbow {e:.0f} deg, forearm {up:.0f} deg above horizontal'))
    return out

def procrustes(A, B):
    """Similarity fit of B onto A; returns residual per point."""
    ma, mb = A.mean(0), B.mean(0); A0, B0 = A - ma, B - mb
    U, S, Vt = np.linalg.svd(B0.T @ A0); R = U @ Vt
    sc = S.sum() / max((B0 ** 2).sum(), 1e-9)
    return np.linalg.norm(A0 - sc * B0 @ R, axis=1)

def ref_match(k, s, ref, T):
    idx = [i for i in BODY if s[i] >= VIS]
    if len(idx) < 8: return check('reference match', 'UNCERTAIN', f'only {len(idx)} limb keypoints seen')
    A = np.array([k[i][:2] for i in idx], float); B = np.array([ref[i] for i in idx], float)
    err = procrustes(A, B); e = float(err.mean() / T)
    sw = [I[n.replace('l', 'r', 1)] if n.startswith('l') else I[n.replace('r', 'l', 1)] for n in KP]
    Bs = np.array([ref[sw[i]] for i in idx], float); es = float(procrustes(A, Bs).mean() / T)
    worst = KP[idx[int(err.argmax())]]
    if es < e * 0.6 and e > 0.20: return check('reference match', 'FAIL', f'left and right look swapped (error {e:.2f}, swapped {es:.2f})')
    st = 'PASS' if e < 0.20 else 'UNCERTAIN' if e < 0.26 else 'FAIL'  # calibrated 2026-11-24: approved redraws 0.13 to 0.22, Grok defects 0.26 to 0.47
    return check('reference match', st, f'mean error {e:.2f} x torso, worst {worst} {err.max() / T:.2f}')

def validate(path, technique, expect, ref=None, prev=None):
    import cv2
    img = cv2.imread(path)
    if img is None: sys.exit(f'cannot read image: {path}')
    kps, scs = model()(img)
    people = [(k, s) for k, s in zip(kps, scs) if float(np.mean(s[5:17])) >= PERSON]
    rep = {'asset': path, 'technique': technique, 'persons': [], 'checks': []}
    n = len(people)
    rep['checks'].append(check('person count', 'PASS' if n == expect else 'FAIL' if n > expect else 'UNCERTAIN',
                               f'{n} detected, {expect} expected' + (' (extra figure)' if n > expect else ' (missing, merged or occluded)' if n < expect else '')))
    roles = []
    for k, s in people:
        role, col = identity(img, k, s); roles.append(role)
        checks, T = person_checks(img, k, s, 'none')
        if ref is not None and role in ('hero', 'opponent') and ref.get('hero' if role == 'hero' else 'opp'):
            checks.append(ref_match(k, s, ref['hero' if role == 'hero' else 'opp'], T))
        rep['persons'].append({'role': role, 'colour': col, 'centre': [round(float(x)) for x in np.mean(k[5:17, :2], 0)], 'checks': checks, 'kp': [[round(float(a), 1), round(float(b), 1), round(float(c), 2)] for (a, b), c in zip(k[:17], s[:17])]})
    if expect == 2 and len(rep['persons']) == 2:
        # pairwise (calibration 2026-11-24): the hero's arm often hides the opponent's top, so compare the two figures
        a, b = rep['persons']; op, he = (a, b) if a['colour']['red_top'] >= b['colour']['red_top'] else (b, a)
        ok = he['colour']['navy_shorts'] >= 0.15 and op['colour']['red_top'] >= 0.05 and op['colour']['red_top'] > he['colour']['red_top'] + 0.03
        if ok and (op['role'], he['role']) != ('opponent', 'hero'):
            op['role'], he['role'] = 'opponent', 'hero'
            if ref is not None:  # role was unknown at check time: add the reference match now
                for p, who in ((op, 'opp'), (he, 'hero')):
                    if ref.get(who) and not any(c['check'] == 'reference match' for c in p['checks']):
                        k = np.array(p['kp']); T = max(np.linalg.norm((k[5, :2] + k[6, :2]) / 2 - (k[11, :2] + k[12, :2]) / 2), 20)
                        p['checks'].append(ref_match(k[:, :2], k[:, 2], ref[who], T))
        roles = [p['role'] for p in rep['persons']]
        rep['checks'].append(check('identity', 'PASS' if ok else 'UNCERTAIN', f'roles {roles}; hero navy shorts {he["colour"]["navy_shorts"]}, opponent red top {op["colour"]["red_top"]}'))
    elif expect == 2:
        rep['checks'].append(check('identity', 'UNCERTAIN', f'roles {roles}: cannot pair hero and opponent'))
    if prev is not None:
        for p in rep['persons']:
            q = min(prev['persons'], key=lambda x: np.hypot(x['centre'][0] - p['centre'][0], x['centre'][1] - p['centre'][1]), default=None)
            if not q: continue
            a, b = np.array(p['kp'])[:, :2], np.array(q['kp'])[:, :2]
            T = max(np.linalg.norm((a[5] + a[6]) / 2 - (a[11] + a[12]) / 2), 20)
            for limb, (x, y, z) in LIMBS.items():
                for u, v in ((x, y), (y, z)):
                    d1, d2 = np.linalg.norm(a[I[u]] - a[I[v]]) / T, np.linalg.norm(b[I[u]] - b[I[v]]) / T
                    if abs(d1 - d2) > 0.30: p['checks'].append(check('frame to frame', 'FAIL', f'{limb} {u}-{v} length jumped {d2:.2f} to {d1:.2f} x torso'))
    for p in rep['persons']:  # technique signature for the final hero (after pairwise identity)
        if p['role'] == 'hero' or (expect == 1 and len(rep['persons']) == 1):
            k = np.array(p['kp']); p['checks'] += tech_check(k[:, :2], k[:, 2], technique)
    if technique not in ('none', 'guard') and ref is None:
        # calibration 2026-11-24: Grok's known straight arm V15 passed every 2D check, so technique accuracy can only
        # be measured against the rig reference from the same camera; without one it always needs visual inspection
        rep['checks'].append(check('technique accuracy', 'UNCERTAIN', 'no rig reference for this still: 2D signatures cannot prove the technique; visual inspection required'))
    allc = rep['checks'] + [c for p in rep['persons'] for c in p['checks']]
    rep['verdict'] = 'FAIL' if any(c['status'] == 'FAIL' for c in allc) else 'UNCERTAIN' if any(c['status'] == 'UNCERTAIN' for c in allc) else 'PASS'
    rep['note'] = 'Automated pose checks only. Visual inspection by the combat-anatomy-specialist is required before approval.'
    return rep, img

def overlay(img, rep, ref, out):
    import cv2
    o = img.copy()
    E = [(5, 7), (7, 9), (6, 8), (8, 10), (5, 6), (11, 12), (5, 11), (6, 12), (11, 13), (13, 15), (12, 14), (14, 16)]
    for p in rep['persons']:
        k = p['kp']; col = (40, 40, 230) if p['role'] == 'opponent' else (230, 120, 30)
        for a, b in E:
            if k[a][2] >= VIS and k[b][2] >= VIS: cv2.line(o, (int(k[a][0]), int(k[a][1])), (int(k[b][0]), int(k[b][1])), col, 5)
    if ref:
        for who in ('hero', 'opp'):
            r = ref.get(who)
            if r:
                for a, b in E: cv2.line(o, tuple(map(int, r[a])), tuple(map(int, r[b])), (0, 200, 0), 2)
    cv2.imwrite(out, o)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--technique', default='none'); ap.add_argument('--expect-persons', type=int, default=2)
    ap.add_argument('--reference'); ap.add_argument('--sequence', action='store_true'); ap.add_argument('--out'); ap.add_argument('--overlay')
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.path, '*.png')) + glob.glob(os.path.join(a.path, '*.jpg'))) if os.path.isdir(a.path) else [a.path]
    ref = json.load(open(a.reference))['kp'] if a.reference else None
    reps, prev = [], None
    for f in files:
        r, img = validate(f, a.technique, a.expect_persons, ref, prev if a.sequence else None); reps.append(r); prev = r
        if a.overlay: os.makedirs(a.overlay, exist_ok=True); overlay(img, r, ref, os.path.join(a.overlay, os.path.basename(f)))
        bad = [f"{c['check']}: {c['detail']}" for c in r['checks'] + [c for p in r['persons'] for c in p['checks']] if c['status'] in ('FAIL', 'UNCERTAIN')]
        print(f"{r['verdict']:9} {os.path.basename(f)}  " + (' | '.join(bad[:4]) if bad else 'all automated checks pass'))
    if a.out: json.dump(reps if len(reps) > 1 else reps[0], open(a.out, 'w'), indent=1)

if __name__ == '__main__':
    main()
