#!/usr/bin/env python3
"""Make grey placeholder pictures for a draft issue (needs Pillow).

    placeholders.py DIR NAME:WxH [NAME:WxH ...]

Each is a soft, grainy black-and-white field with PLACEHOLDER in the
corner, so a draft shows the layout without anyone mistaking it for a
real picture. Replace them with the real files before printing."""
import random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

out = sys.argv[1]
for i, spec in enumerate(sys.argv[2:]):
    name, size = spec.split(":")
    w, h = (int(v) for v in size.split("x"))
    rnd = random.Random(name)
    img = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    top, bot = rnd.randint(150, 230), rnd.randint(30, 110)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=int(top + (bot - top) * y / h))
    for _ in range(14):
        x, y, r = rnd.randint(0, w), rnd.randint(0, h), rnd.randint(w // 14, w // 4)
        d.ellipse([x - r, y - r, x + r, y + r], fill=rnd.randint(20, 235))
    img = img.filter(ImageFilter.GaussianBlur(w / 40))
    noise = Image.effect_noise((w, h), 28).convert("L")
    img = Image.blend(img, noise, 0.12)
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", max(12, w // 45))
    except OSError:
        f = ImageFont.load_default()
    d.text((w // 40, h - w // 40 - w // 45), "PLACEHOLDER  " + name.upper(), fill=255, font=f)
    img.save("%s/%s.jpg" % (out, name), quality=85)
    print("%s/%s.jpg" % (out, name))
