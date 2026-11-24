# Speed line layers + glove points for stills replaced on 2026-11-24 (Grok's own speed_lines helper, house style).
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, "/home/user/fp-longform/grok_src/edit")
import build as V1
L = Path("/home/user/fp-longform/public/layers")
# measured on the new stills (1920x1080); hero faces LEFT, so hooks travel left and lines trail right (+1)
G = {"V2": [980, 480, 1, 85], "V3": [720, 470, 1], "V9": [690, 450, 1], "V15": [800, 470, 1], "V20": [770, 480, 1, 70],
     "V21": [800, 420, 1], "V23": [690, 450, 1, 60], "V24": [900, 360, "up", 60], "V33": [720, 510, 1], "V34": [940, 450, 1],
     "V53": [690, 460, 1, 60], "V70": [970, 440, "up", 50], "V79": [963, 746, "up", 50], "V84": [810, 460, 1, 70],
     "V86": [700, 460, 1], "V88": [900, 360, "up", 50], "V94": [730, 464, 1]}
def diff_layer(a, b):
    A = np.asarray(a.convert("RGB")).astype(int); B = np.asarray(b.convert("RGB"))
    m = (np.abs(A - B.astype(int)).max(axis=2) > 0)
    out = np.zeros((a.size[1], a.size[0], 4), np.uint8); out[..., :3] = B; out[..., 3] = m * 255
    return Image.fromarray(out, "RGBA")
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(G)
for v in only:
    base = Image.open(L / f"{v}_base.png").convert("RGB")
    wl, n = V1.lines(base.copy(), G[v])
    diff_layer(base, wl).save(L / f"{v}_lines.png"); print(v, n)
json.dump(G, open("/home/user/fp-longform/glove_fix.json", "w"))
