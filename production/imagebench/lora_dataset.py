#!/usr/bin/env python3
"""Build a character LoRA training set from Sean's APPROVED art only.

Sources: the four views of main_character_reference.jpg, plus hero only stills that passed
Grok's v4 zoomed QA in the liver project. Each image gets a caption with the trigger word.
Output: a zip ready for a hosted FLUX LoRA trainer (no GPU here). Keep the zip private.

usage: python3 lora_dataset.py --out DIR
"""
import argparse, json, zipfile
from pathlib import Path
from PIL import Image

H = Path("/home/user/the-fight-playbook-claude-handoff")
LIVER = H / "VIDEO-PROJECTS/target-the-liver-in-boxing/edit"
TRIGGER = "tfphero"
LOOK = ("dark charcoal gray bald muscular faceless fighter with only two small slanted white eyes, black sleeveless shirt with red side stripes, "
        "navy shorts with red trim, black MMA gloves with red wrist straps, barefoot, clean 2D comic illustration, thin black outlines, flat colors, flat sage background")
# hero only stills from the v4 cut (all passed the final anatomy QA)
SOLO = {"V8": "extreme close up of the face", "V11": "standing in guard holding up fingers", "V18": "close up of the face and gloves",
        "V58": "close up of the face", "V77": "close up of the face", "V90": "standing showing three fingers",
        "V98": "close up of the upper body", "V103": "front view in guard", "V104": "front view in guard, medium shot",
        "V105": "full body in guard, wide shot", "V106": "front view in guard", "V107": "front view in guard",
        "V42": "punching a heavy bag", "V62": "hooking a heavy bag", "V79": "low stance at a heavy bag", "V81": "in stance next to a heavy bag",
        "V99": "jabbing a heavy bag", "V100": "in guard beside a heavy bag"}

ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); a = ap.parse_args()
out = Path(a.out); img_dir = out / "images"; img_dir.mkdir(parents=True, exist_ok=True)
sel = json.load(open(LIVER / "work/sel.json"))
items = []
ref = Image.open(H / "CHARACTERS/main_character_reference.jpg").convert("RGB"); w, h = ref.size
# find each figure by its dark pixels (no neighbour slivers, which would teach ghost figures)
import numpy as np
g = np.asarray(ref.convert("L")).astype(int)[: int(h * 0.86)]
cols = (g < 110).sum(axis=0) > 6
runs, x = [], 0
while x < w:
    if cols[x]:
        x0 = x
        while x < w and cols[x]: x += 1
        if x - x0 > w * 0.04: runs.append((x0, x))
    x += 1
assert len(runs) == 4, f"expected 4 figures, found {len(runs)}"
for (x0, x1), view in zip(runs, ["front view", "right side view", "left side view", "back view"]):
    rows = np.where((g[:, x0:x1] < 110).sum(axis=1) > 2)[0]
    y0, y1 = rows.min(), rows.max(); cx = (x0 + x1) // 2; half = max(x1 - x0, (y1 - y0) // 2) // 2 + 30
    box = (max(0, cx - half), max(0, y0 - 30), min(w, cx + half), min(int(h * 0.86), y1 + 30))
    others = [r for r in runs if r != (x0, x1) and r[1] > box[0] and r[0] < box[2]]
    if others:  # clamp the box so no other figure enters it
        box = (max(box[0], max([r[1] for r in others if r[1] <= x0] or [box[0]]) + 4), box[1], min(box[2], min([r[0] for r in others if r[0] >= x1] or [box[2]]) - 4), box[3])
    items.append((ref.crop(box), f"{TRIGGER}, {view}, full body standing, {LOOK}"))
for sid, desc in SOLO.items():
    p = LIVER / "stills" / f"{sel.get(sid, sid)}.png"
    if p.exists(): items.append((Image.open(p).convert("RGB"), f"{TRIGGER}, {desc}, {LOOK}"))
with zipfile.ZipFile(out / "tfphero_lora.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for k, (im, cap) in enumerate(items):
        name = f"{k:02d}"; im.save(img_dir / f"{name}.png"); (img_dir / f"{name}.txt").write_text(cap)
        z.write(img_dir / f"{name}.png", f"{name}.png"); z.write(img_dir / f"{name}.txt", f"{name}.txt")
print(len(items), "images ->", out / "tfphero_lora.zip")
