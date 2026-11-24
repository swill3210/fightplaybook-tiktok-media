"""Head comparison at the same figure scale: sheet (top row) vs render (bottom row) for front, right and (render only) 3/4.
python3 compare_head2.py RENDER_DIR OUT.jpg"""
import sys
from PIL import Image, ImageOps
import compare_ref as CR
def headcrop(im, frac=0.24):
    g = ImageOps.grayscale(im); bg = g.getpixel((2, 2)); bb = g.point(lambda p: 255 if abs(p - bg) > 60 else 0).getbbox()
    x0, y0, x1, y1 = bb; h = y1 - y0; cx = (x0 + x1) // 2; s = int(frac * h)
    return im.crop((cx - s // 2 - s // 4, y0 - 5, cx + s // 2 + s // 4, y0 + s)).resize((450, 600))
ref = Image.open(CR.REF).convert("RGB"); d = sys.argv[1]
top = [headcrop(ref.crop(CR.BOXES[v])) for v in ("front", "right")]
bot = [headcrop(Image.open(f"{d}/body_{v}.png").convert("RGB")) for v in ("front", "right", "threequarter")]
c = Image.new("RGB", (1350, 1200), "white")
for i, im in enumerate(top): c.paste(im, (i * 450, 0))
for i, im in enumerate(bot): c.paste(im, (i * 450, 600))
c.save(sys.argv[2], quality=90)
