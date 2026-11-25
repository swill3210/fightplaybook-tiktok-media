#!/usr/bin/env python3
"""Liver v4 fix pass (Sean's review of v3, 2026-11-25). Runs after build_timeline.py, prep_fixed.py and relines.py,
before make_cutouts.py. No generative image model is used (MASTER_RULES 9): every replacement is an existing still
that passed review, reframed in code, plus drawn diagrams.

Root causes fixed here
* Generation: the v1 to v3 prompts asked for the glove "buried" and the tank top "compressing around the glove".
  Every still with a glove under or swallowed by clothing is replaced (REPL below).
* Camera crop: contact crops cut heads off (V2) or showed a glove with no owner (V12, V25, V50). Replacements keep
  both heads or the whole punching arm in frame.
* Overlays: fixed screen slots covered the demo. occ.json gives the compositor a per shot character occupancy grid
  so every overlay goes to the emptiest allowed slot (Graphics.tsx pickSlot).
* Recap board: crops around the glove cut heads; the board now crops each card to the characters' bounding box.
"""
import json, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

R = Path(__file__).parent; P = R / "public"; L = P / "layers"
W, H = 1920, 1080; SAGE = (196, 214, 196)
TL = json.load(open(P / "timeline.json")); S = {s["id"]: s for s in TL["shots"]}
ED = Path("/home/user/the-fight-playbook-claude-handoff/VIDEO-PROJECTS/target-the-liver-in-boxing/edit")

def box_for(c, z):
    w, h = W / z, H / z; x0 = min(max(c[0] - w / 2, 0), W - w); y0 = min(max(c[1] - h / 2, 0), H - h)
    return (x0, y0, x0 + w, y0 + h)

# 1. stray Dutch floor line in V69 ran from both feet to the frame edges (edge contact + reads as a stray line)
im = Image.open(L / "V69_base.png").convert("RGB"); d = ImageDraw.Draw(im)
d.line([(1508, 810), (1925, 672)], fill=SAGE, width=16); d.line([(300, 1090), (470, 1046)], fill=SAGE, width=16)
im.save(L / "V69_base.png")

# 2. replacements: shot -> (source still, zoom centre or None, zoom, new glove or "src", why)
REPL = {
    "V2":  ("V33", None, 1, "src", "crop of V86 cut both heads; text over the punch"),
    "V12": ("V45", None, 1, None, "straight arm into the hip; arm ownership unclear"),
    "V24": ("V80", None, 1, "src", "shovel glove under the shirt hem"),
    "V25": ("V94", (760, 440), 1.5, "src", "glove sunk into the shirt; no visible owner"),
    "V35": ("V15", None, 1, "src", "money moment: glove swallowed by a cloth swirl"),
    "V50": ("V47", None, 1, None, "chest close up with an ownerless glove at the edge"),
    "V54": ("V21", (820, 420), 1.4, "src", "glove sunk into a cloth swirl"),
    "V57": ("V48", None, 1, None, "rear arm ownership unclear"),
    "V70": ("V66", None, 1, None, "shovel glove under the shirt"),
    "V71": ("V65", (950, 500), 1.3, None, "shovel glove under the shirt"),
    "V72": ("V69", (1080, 560), 1.4, None, "shovel glove under the shirt"),
    "V76": ("V82", None, 1, None, "shovel glove under the shirt hem"),
    "V79": ("V68", None, 1, None, "shovel glove under the shirt"),
    "V88": ("V64", None, 1, None, "shovel glove under the shirt hem"),
    "V89": ("V61", None, 1, "src", "cloth spiral around the glove; heads cropped"),
    "V95": ("V38", None, 1, "src", "glove sunk into the shirt; card over the demo"),
}
ANGLE = {"V12": "medium side", "V25": "close up contact ribs", "V54": "close up contact ribs", "V71": "medium side",
         "V72": "Dutch tilt", "V76": "behind the opponent", "V79": "front three quarter", "V88": "wide establishing",
         "V89": "low side", "V95": "medium side", "V2": "wide rear three quarter", "V24": "extreme close up bag",
         "V35": "extreme close up ribs", "V50": "front three quarter", "V57": "front three quarter", "V70": "medium side"}
for sid, (src, c, z, glove, why) in REPL.items():
    s = S[sid]; srcs = S[src]; stem = f"{sid}x"
    base = Image.open(L / f"{src}_base.png").convert("RGB"); lines = L / f"{src}_lines.png"
    g = list(srcs["glove"]) if (glove == "src" and srcs["glove"]) else None
    if c:
        b = box_for(c, z); base = base.crop(tuple(map(round, b))).resize((W, H), Image.LANCZOS)
        if g: g[0], g[1] = round((g[0] - b[0]) * z), round((g[1] - b[1]) * z)
        lines = None  # speed lines would scale up; the glove push and impact still play
    base.save(L / f"{stem}_base.png"); s["layers"] = {"base": f"layers/{stem}_base.png"}
    if lines is not None and lines.exists() and g:
        shutil.copy2(lines, L / f"{stem}_lines.png"); s["layers"]["lines"] = f"layers/{stem}_lines.png"
    s["glove"] = g; s["phase_frames"] = 0; s["angle"] = ANGLE[sid]; s["replaced"] = {"from": src, "why": why}
    s.pop("bz", None)
S["V2"]["text"] = ["THE LIVER SHOT"]  # was ONE PUNCH / FOLDS ANYONE (overclaim)
S["V2"]["frame"] = [0.8, 170]            # both heads clear the headline
S["V35"]["flags"] = ["MONEY MOMENT part 2", "slow motion hard zoom in code"]

# 3. Grok's old straight arm V94 for the correct vs incorrect card (missing from the export)
Image.open(ED / "stills/V94_r14.png").convert("RGB").resize((W, H), Image.LANCZOS).save(L / "ref_V94_old_straightarm.png")

# 4. hero side per shot (whip pan only when it changes); hero is on screen right in these
TL["hero_right"] = sorted(set(["V3", "V9", "V15", "V20", "V21", "V23", "V33", "V34", "V53", "V84", "V86", "V94",
                               "V2", "V25", "V35", "V54", "V12", "V88"]))

# 5. recap board crops: each card shows both characters whole (bounding box of the character mask)
def bbox(stem):
    a = np.asarray(Image.open(L / f"{stem}_base.png").convert("RGB")).astype(int)
    m = np.abs(a - np.array(SAGE)).sum(axis=2) > 60; ys, xs = np.where(m)
    return [int(np.percentile(xs, 0.5)), int(np.percentile(ys, 0.5)), int(np.percentile(xs, 99.5)), int(np.percentile(ys, 99.5))]
TL["board"] = [{"src": f"layers/{k}_base.png", "box": bbox(k)} for k in ("V84", "V53", "V64")]

json.dump(TL, open(P / "timeline.json", "w"), indent=1)
print("replaced", len(REPL), "shots; board", TL["board"])
