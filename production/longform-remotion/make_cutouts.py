# character cut out + clean plate per approved base layer (flat background keyed out); plate keeps ground line and shadows
import json, numpy as np
from pathlib import Path
from PIL import Image, ImageFilter
P = Path("public/layers"); out = []
for f in sorted(P.glob("*_base.png")):
    im = Image.open(f).convert("RGB"); a = np.asarray(im).astype(np.int16)
    border = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    d = np.abs(a - bg).sum(axis=2)
    m = (d > 60).astype(np.uint8) * 255  # characters are dark or saturated against sage; shadows (small d) stay in the plate
    mi = Image.fromarray(m).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA"); rgba.putalpha(mi); rgba.save(str(f).replace("_base", "_cut"))
    plate = np.where(m[..., None] > 0, bg, a).astype(np.uint8); Image.fromarray(plate).save(str(f).replace("_base", "_plate"))
    ys = np.where(m.any(axis=1))[0]; feet = int(ys.max()) if len(ys) else a.shape[0]
    out.append((f.name.split("_")[0], feet, bg.tolist()))
json.dump({k: {"feet": ft, "bg": bg} for k, ft, bg in out}, open("public/cutinfo.json", "w"))
print(len(out), "cutouts")
