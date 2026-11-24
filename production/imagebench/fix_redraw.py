#!/usr/bin/env python3
"""Redraw failed liver stills from the 3D rig pose (rig render passed FIRST, Nano Banana 2 via ElevenLabs).
usage: python3 fix_redraw.py --poses DIR --out DIR [--only V3,V24]"""
import argparse, json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ["FP_RESTYLE"] = "1"
import bench
m = bench.blocks()
HOOKA = f"The main character throws a LEFT hook to the body with the LEFT (lead) arm: {m.HOOK}; knees bent to lower the level, hips and shoulders turned into the punch, the RIGHT glove tight at the chin; {m.CONTACT}. Opponent {m.GHIGH}."
SHOV = f"The main character throws a RIGHT shovel uppercut to the body: {m.UPPER}; the LEFT glove stays at the chin; {m.UPCONTACT}. Opponent {m.GHIGH}."
JAB = f"The main character throws a LEFT jab: the left arm fully extended STRAIGHT and horizontal, shoulder, elbow and glove in one line, glove touching the opponent's high guard; the right glove stays at the chin. Opponent {m.GHIGH}."
SH = {
 "V2": ("Medium close up on the contact at the opponent's right side ribs, both torsos in frame.", HOOKA),
 "V3": ("Medium shot from behind the main character's left shoulder, three quarter.", HOOKA),
 "V9": ("Wide three quarter view from behind the main character.", HOOKA),
 "V15": ("Medium high angle looking slightly down.", HOOKA),
 "V20": ("Over the shoulder of the main character toward the opponent's face.", JAB),
 "V21": ("Low worm's eye angle looking up at the contact.", HOOKA + " This is a PUNCH with the arm; both feet stay on the ground, NO knee strike, NO kick."),
 "V23": ("Rear three quarter view, behind and to the side of the main character.", HOOKA),
 "V24": ("Low side view.", SHOV),
 "V33": ("Dutch tilt (camera rolled about 12 degrees), mid swing just before contact. Both faces blank with NO mouth.", HOOKA.replace(m.CONTACT, "the glove a few centimetres from the opponent's right lower ribs, about to land")),
 "V34": ("Low angle close up on the contact.", HOOKA + " Fully redraw in flat 2D comic illustration; nothing may look like a 3D mannequin or a plastic render."),
 "V53": ("High rear three quarter view.", HOOKA),
 "V70": ("Three quarter view from behind the main character.", SHOV),
 "V79": ("Low side view, main character alone at a heavy bag.", "The main character throws a RIGHT shovel uppercut into the heavy bag at rib height: " + m.UPPER + "; the LEFT glove stays at the chin; the bag compresses upward around the glove."),
 "V84": ("Side view, eye level.", HOOKA + " The hooking elbow is a sharp 90 degree right angle, never an open angle."),
 "V86": ("Medium three quarter view.", HOOKA),
 "V88": ("Low three quarter view from behind the main character.", SHOV),
 "V94": ("Medium shot, eye level, three quarter.", HOOKA + " The hooking elbow is a sharp 90 degree right angle, never an open angle."),
}
LAY = ("LAYOUT (copy it from the FIRST image, do not change it): exactly TWO people in the whole image. The main character (black shirt, navy shorts) is on the RIGHT half of the image, seen from behind or the side, facing LEFT. "
       "The opponent (red top, black shorts) is on the LEFT half, facing the camera and the main character, and is taller and broader. Their bodies overlap exactly as in the first image. ")
SOLO = "LAYOUT (copy it from the FIRST image): exactly ONE person, the main character on the RIGHT half facing LEFT; the heavy bag on the LEFT half. "
LAYR = ("LAYOUT (copy it from the FIRST image, do not change it): exactly TWO people in the whole image. The main character (black shirt, navy shorts) is on the LEFT, crouched low, facing RIGHT, seen from their right side so the punching RIGHT arm is nearest the camera. "
        "The opponent (red top, black shorts) is on the RIGHT facing LEFT, taller and broader. Their bodies overlap exactly as in the first image. ")
SOLOR = "LAYOUT (copy it from the FIRST image): exactly ONE person, the main character crouched low facing RIGHT, seen from their right side so the punching RIGHT arm is nearest the camera. ADD one heavy bag on the RIGHT, its surface touching the rising right glove. NO opponent, NO second person. "
def scene(v):
    cam, act = SH[v]
    if v == "V79":
        cast = m.HERO + " " + m.BAG + " Draw ONLY the main character, exactly once, and the bag. Draw the bag where the opponent would be."
        once = ""
    else:
        cast = m.HERO + " " + m.OPP; once = m.ONCE["ho"]
    p = " ".join([m.STYLE, "CAMERA: " + cam, (SOLOR if v == "V79" else LAY), "ACTION: " + act, cast, once, m.NOFX, "Plain flat sage green background #C4D6C4 with a thin ground line. Barefoot. Wide 16:9 frame."])
    return {"id": v, "prompt": " ".join(p.split())}
ap = argparse.ArgumentParser(); ap.add_argument("--poses", required=True); ap.add_argument("--out", required=True); ap.add_argument("--only", default=""); ap.add_argument("--model", default="gemini-3.1-flash-image")
a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
run = bench.eleven(a.model, {"quality": "high"} if a.model.startswith("gpt") else {"resolution": "2K"})
for v in (a.only.split(",") if a.only else SH):
    dst = out / f"{v}.png"
    if dst.exists(): continue
    t0 = time.time()
    try:
        img, info = run(scene(v), bench.REFS, Path(a.poses) / f"{v}.png"); dst.write_bytes(img); err = None
    except Exception as e:
        info, err = {}, repr(e)[:300]
    rec = {"id": v, "ok": err is None, "s": round(time.time() - t0, 1), "err": err, "credits": (info.get("response") or {}).get("credits_used")}
    open(out / "runs.jsonl", "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec))
    if err and "40" in err: break
