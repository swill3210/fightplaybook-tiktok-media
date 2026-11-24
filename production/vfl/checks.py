"""Inexpensive programmatic screeners (no API calls, no tokens).

Each returns a list of (code, level, note) where level is FAIL (hard, no AI needed) or FLAG (send to the inspector
with this hint). A clean result is NEVER an approval: combat anatomy and technique always need the visual inspector.
"""
import subprocess, json
import numpy as np
from PIL import Image
import vfl_lib as L


def _arr(path, w=480):
    im = Image.open(path).convert("RGB")
    im = im.resize((w, round(im.height * w / im.width)))
    return np.asarray(im).astype(np.int16)


def bg_colour(a):
    k = max(2, a.shape[0] // 40)
    corners = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3)])
    return np.median(corners, axis=0)


def fg_mask(a, bg, tol=38):
    return np.abs(a - bg).sum(axis=2) > tol


def known_defect(path, reg, thr=22):
    """FAIL if the image is (a re-encode or light rescale of) a documented defective original."""
    h = L.dhash(path)
    out = []
    for iid, v in reg["instances"].items():
        o = v.get("original") or {}
        if o.get("dhash") and L.hamming(h, o["dhash"]) <= thr:
            out.append((v["class"][4:], "FAIL", f"matches known defect {iid} ({v['title'][:50]})"))
    return out[:3]


def edge_contact(a, bg):
    """FLAG bodies touching the top or side edges (heads cut, limbs sliced). Bottom exits are allowed."""
    m = fg_mask(a, bg)
    h, w = m.shape
    e = max(2, w // 160)
    res = []
    top = m[:e].mean()
    left, right = m[:, :e].mean(), m[:, -e:].mean()
    if top > 0.04:
        res.append(("G01", "FLAG", f"subject touches the top edge ({top:.0%} of it)"))
    for side, v in (("left", left), ("right", right)):
        if v > 0.12:
            res.append(("G01", "FLAG", f"subject touches the {side} edge ({v:.0%} of it)"))
    return res


def skin_drift(a, bg):
    """FLAG tan or peach patches (skin must be charcoal). Ignores pixels near the background colour."""
    rgb = a.astype(np.float32) / 255
    mx, mn = rgb.max(2), rgb.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    tan = (r > g) & (g > b) & (sat > 0.22) & (sat < 0.65) & (mx > 0.45) & ((r - g) < 0.25) & ((g - b) > 0.05)
    tan &= np.abs(a - bg).sum(2) > 60
    frac = tan.mean()
    return [("E03", "FLAG", f"tan or peach pixels {frac:.1%}")] if frac > 0.004 else []


def screen_still(path, reg=None):
    reg = reg or L.load()
    a = _arr(path)
    bg = bg_colour(a)
    return known_defect(path, reg) + edge_contact(a, bg) + skin_drift(a, bg)


# ---------------- render level ----------------
def _frames(video, fps=10, w=192):
    h = None
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", video],
                       capture_output=True, text=True)
    s = json.loads(p.stdout)["streams"][0]
    h = round(s["height"] * w / s["width"])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    n = len(raw) // (w * h * 3)
    return np.frombuffer(raw[: n * w * h * 3], np.uint8).reshape(n, h, w, 3).astype(np.int16), fps


def screen_render(video, exempt=(), fps=10):
    """Hard FAILs: flash frames (R11), mostly empty frames, freezes over 1 s. exempt: list of (t0, t1) seconds."""
    f, fps = _frames(video, fps)
    luma = f.mean(axis=(1, 2, 3))
    bg = np.median(np.concatenate([f[:, :3, :3].reshape(-1, 3), f[:, :3, -3:].reshape(-1, 3)]), axis=0)
    out = []
    def ex(t):
        return any(a <= t <= b for a, b in exempt)
    for i in range(1, len(f) - 1):
        t = i / fps
        if ex(t):
            continue
        if luma[i] - max(luma[i - 1], luma[i + 1]) > 35 and luma[i] > 170:
            out.append((round(t, 1), "F04", "FAIL", "flash frame"))
        empty = (np.abs(f[i] - bg).sum(2) < 30).mean()
        if empty > 0.97:
            out.append((round(t, 1), "H02", "FAIL", f"frame {empty:.0%} background"))
    still = 0
    for i in range(1, len(f)):
        d = np.abs(f[i] - f[i - 1]).mean()
        still = still + 1 if d < 0.15 else 0
        if still == int(fps * 1.0) and not ex(i / fps):
            out.append((round(i / fps, 1), "H02", "FAIL", "frozen over 1 s"))
    return out


def edge_frames(video, times):
    """Screen specific render frames (shot mid points, transitions) for crops introduced by camera moves."""
    res = []
    for t in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", "scale=480:-1",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if not raw:
            continue
        a = np.frombuffer(raw, np.uint8).reshape(-1, 480, 3).astype(np.int16)
        for code, lvl, note in edge_contact(a, bg_colour(a)):
            res.append((t, code, lvl, note))
    return res
