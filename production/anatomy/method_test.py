#!/usr/bin/env python3
"""Generation method comparison for combat stills (Sean's combat anatomy brief, 2026-11-24).
A: text to image (Grok's prompt blocks + character references, no pose)
B: pose controlled (3D rig render passed FIRST, "redraw the first image", same blocks)
(C, the rigged render itself, needs no generation: the motion library stills and clips.)
First pass only, no retries, so the result measures reliability.
usage: python3 method_test.py --poses DIR --out DIR [--methods A,B]"""
import argparse, json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'imagebench'))
import bench
m = bench.blocks()
ACT = {
    'jab': "The main character throws a LEFT jab: the left arm fully extended STRAIGHT and horizontal, shoulder, elbow and glove in one line, glove touching the opponent's high guard; the RIGHT glove stays at the chin.",
    'cross': "The main character throws a RIGHT straight (cross) to the opponent's chin: rear foot pivoted with the heel turned out, hips and shoulders turned forward, right arm fully extended straight, LEFT glove at the chin.",
    'lead_body_hook': f"The main character throws a LEFT hook to the body with the LEFT (lead) arm: {m.HOOK}; knees bent, hips and shoulders turned into the punch, the RIGHT glove tight at the chin; {m.CONTACT}.",
    'shovel_uppercut': f"The main character throws a RIGHT shovel uppercut to the body: {m.UPPER}; the LEFT glove stays at the chin; {m.UPCONTACT}.",
}
CAM = {'liver34': "Medium shot, three quarter view from behind the main character's left shoulder, the main character on the RIGHT facing LEFT.",
       'side': "Side view, eye level, the main character on the RIGHT facing LEFT, the opponent on the LEFT facing RIGHT."}
LAY = ("LAYOUT (copy it from the FIRST image, do not change it): exactly TWO people. The main character (black shirt, navy shorts) is on the RIGHT, the opponent "
       "(red top, black shorts) on the LEFT and taller. Their bodies, arms and legs are placed exactly as in the first image. ")
def prompt(move, cam, posed):
    p = " ".join([m.STYLE, "CAMERA: " + CAM[cam], LAY if posed else "", "ACTION: " + ACT[move] + f" Opponent {m.GHIGH}.", m.HERO, m.OPP, m.ONCE['ho'], m.NOFX,
                  "Plain flat sage green background #C4D6C4 with a thin ground line. Barefoot. Wide 16:9 frame."])
    return " ".join(p.split())
ap = argparse.ArgumentParser(); ap.add_argument('--poses', required=True); ap.add_argument('--out', required=True); ap.add_argument('--methods', default='A,B')
a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
log = out / 'runs.jsonl'
for meth in a.methods.split(','):
    os.environ['FP_RESTYLE'] = '1' if meth == 'B' else '0'
    run = bench.eleven('gemini-3.1-flash-image', {'resolution': '2K'})
    for pose in sorted(Path(a.poses).glob('*.png')):
        move, cam = pose.stem.split('.'); dst = out / meth / f'{pose.stem}.png'; dst.parent.mkdir(exist_ok=True)
        if dst.exists(): continue
        t0 = time.time()
        try:
            img, info = run({'id': pose.stem, 'prompt': prompt(move, cam, meth == 'B')}, bench.REFS, pose if meth == 'B' else None); dst.write_bytes(img); err = None
        except Exception as e:
            err = repr(e)[:300]
        rec = {'method': meth, 'cell': pose.stem, 'seconds': round(time.time() - t0, 1), 'error': err}
        open(log, 'a').write(json.dumps(rec) + '\n'); print(json.dumps(rec))
        if err and ' 40' in err: sys.exit('auth or quota error: stopping')
