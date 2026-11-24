"""Side by side: reference sheet views (top) vs our render (bottom), each figure scaled to the same height.
Run: python3 compare_ref.py RENDER_DIR OUT.jpg"""
import sys
from PIL import Image, ImageOps
REF = "/home/user/fightplaybook-tiktok-media/.claude/skills/fight-playbook-rules/main_character_reference.jpg"
BOXES = {"front": (40, 0, 380, 640), "right": (390, 0, 620, 640), "left": (670, 0, 900, 640), "back": (910, 0, 1240, 640)}

def fig(im, bg_thresh=60):
    g = ImageOps.grayscale(im); bg = g.getpixel((2, 2))
    mask = g.point(lambda p: 255 if abs(p - bg) > bg_thresh else 0)
    b = mask.getbbox(); return im.crop(b) if b else im

def main(d, out, H=600):
    ref = Image.open(REF).convert("RGB"); cols = []
    for n, box in BOXES.items():
        a = fig(ref.crop(box)); b = fig(Image.open(f"{d}/body_{n}.png").convert("RGB"))
        a = a.resize((int(a.width * H / a.height), H)); b = b.resize((int(b.width * H / b.height), H))
        w = max(a.width, b.width) + 20; c = Image.new("RGB", (w, 2 * H + 30), "white")
        c.paste(a, ((w - a.width) // 2, 5)); c.paste(b, ((w - b.width) // 2, H + 25)); cols.append(c)
    W = sum(c.width for c in cols); s = Image.new("RGB", (W, cols[0].height), "white"); x = 0
    for c in cols: s.paste(c, (x, 0)); x += c.width
    s.save(out, quality=88)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
