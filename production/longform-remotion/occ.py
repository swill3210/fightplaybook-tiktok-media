# per shot character occupancy (48x27 grid of 40 px cells, digit = tenths covered) in screen space, for overlay placement
import json, numpy as np
from PIL import Image
P = "public"; TL = json.load(open(f"{P}/timeline.json")); out = {}
for s in TL["shots"]:
    if not s["layers"].get("base"): continue
    a = np.asarray(Image.open(f"{P}/{s['layers']['base']}").convert("RGB")).astype(int)
    b = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    m = (np.abs(a - np.median(b, axis=0)).sum(axis=2) > 60).astype(np.float32)
    if s.get("frame"):  # translateY(dy) scale(z) about the centre
        z, dy = s["frame"]; im = Image.fromarray((m * 255).astype(np.uint8)); w, h = round(1920 * z), round(1080 * z)
        c = Image.new("L", (1920, 1080), 0); c.paste(im.resize((w, h)), ((1920 - w) // 2, (1080 - h) // 2 + dy)); m = np.asarray(c) / 255.0
    g = m.reshape(27, 40, 48, 40).mean(axis=(1, 3))
    g = np.maximum(g, np.pad(g, 1, mode="edge")[1:-1, 2:]) ; g = np.maximum(g, np.pad(g, 1, mode="edge")[1:-1, :-2])  # 1 cell margin left/right
    g = np.maximum(g, np.pad(g, 1, mode="edge")[2:, 1:-1]); g = np.maximum(g, np.pad(g, 1, mode="edge")[:-2, 1:-1])
    out[s["id"]] = ["".join(str(min(9, int(v * 10 + 0.5))) for v in row) for row in g]
json.dump(out, open(f"{P}/occ.json", "w")); print(len(out), "occupancy grids")
