"""Head close ups vs reference crops: python3 compare_head.py RENDER_DIR OUT.jpg"""
import sys
from PIL import Image
REF = "/home/user/fightplaybook-tiktok-media/.claude/skills/fight-playbook-rules/main_character_reference.jpg"
r = Image.open(REF).convert("RGB")
refs = [r.crop((150, 0, 280, 130)), r.crop((430, 0, 560, 130))]
d = sys.argv[1]
outs = [Image.open(f"{d}/face_{n}.png").convert("RGB").crop((0, 110, 700, 810)) for n in ("front", "right", "threequarter")]
c = Image.new("RGB", (1500, 300), "white")
for i, im in enumerate([refs[0], outs[0], refs[1], outs[1], outs[2]]):
    c.paste(im.resize((300, 300)), (i * 300, 0))
c.save(sys.argv[2], quality=88)
