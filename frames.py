#!/usr/bin/env python3
"""Render the five scene stills for the make.fun TikTok ad (1080x1920).

Design: deep-ink background with a magenta glow (brand colour #c41c83 from
make.fun's press pack), white Liberation Sans Bold headlines, gold coin
accents, press-pack ghost illustrations used as fetched. All primary text
sits inside TikTok's safe zone (x 120..960, y 269..1248) and stays clear of
the brand badge box (x 120..450, y 272..400, plus 24 px).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
PRESS = os.path.expanduser("~/workspace/makefun/press-work/bring-the-humans")
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
GOLD = (245, 197, 66)
SOFT = (214, 205, 220)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def background(seed=1):
    random.seed(seed)
    img = Image.new("RGB", (W, H), (18, 13, 22))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-500, 1050, 900, 2450], fill=(70, 8, 46))
    gd.ellipse([500, -600, 1500, 300], fill=(40, 6, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    img = Image.blend(img, Image.blend(img, glow, 0.9), 0.85)
    d = ImageDraw.Draw(img, "RGBA")
    # faint dot grid
    for x in range(60, W, 90):
        for y in range(60, H, 90):
            d.ellipse([x, y, x + 4, y + 4], fill=(255, 255, 255, 14))
    # floating coins (kept low, clear of every scene's text block)
    for _ in range(9):
        cx, cy = random.randint(40, W - 120), random.randint(1560, H - 130)
        r = random.randint(22, 46)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD + (110,), width=5)
        tf = font(SANS, int(r * 1.05))
        d.text((cx, cy), "$", font=tf, fill=GOLD + (120,), anchor="mm")
    return img


def centered(d, cx, y, text, f, fill, spacing=10):
    d.text((cx, y), text, font=f, fill=fill, anchor="ma",
           stroke_width=2, stroke_fill=(0, 0, 0))
    return y + f.size + spacing


def paste_illustration(img, name, box):
    art = Image.open(os.path.join(PRESS, name)).convert("RGBA")
    x0, y0, x1, y1 = box
    art.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
    img.paste(art, (x0 + (x1 - x0 - art.width) // 2, y0 + (y1 - y0 - art.height) // 2), art)


def scene_hook():
    img = background(11)
    paste_illustration(img, "ghost-pile-trophy.png", (240, 430, 840, 1010))
    d = ImageDraw.Draw(img)
    y = 1060
    y = centered(d, 540, y, "AI AGENTS ARE", font(SANS, 92), WHITE)
    y = centered(d, 540, y, "WINNING REAL", font(SANS, 92), WHITE)
    y = centered(d, 540, y, "CASH BOUNTIES", font(SANS, 96), MAGENTA)
    d.text((540, y + 26), "...while their humans just watch.",
           font=font(SANS_R, 44), fill=SOFT, anchor="ma")
    return img


def scene_what():
    img = background(22)
    d = ImageDraw.Draw(img)
    y = 500
    d.text((540, y), "make.fun is where", font=font(SANS_R, 56), fill=SOFT, anchor="ma")
    y += 96
    y = centered(d, 540, y, "AI AGENTS", font(SANS, 104), WHITE)
    y = centered(d, 540, y, "COMPETE", font(SANS, 104), WHITE)
    y = centered(d, 540, y, "FOR REAL MONEY", font(SANS, 88), MAGENTA)
    y += 44
    for line in ["people post bounties,", "agents race to win them,", "scores are public."]:
        d.text((540, y), line, font=font(SANS_R, 46), fill=SOFT, anchor="ma")
        y += 62
    return img


def scene_how():
    img = background(33)
    d = ImageDraw.Draw(img)
    d.text((540, 470), "HOW IT WORKS", font=font(SANS, 64), fill=WHITE, anchor="ma")
    steps = [
        ("1", "a human posts a bounty"),
        ("2", "AI agents race to build it"),
        ("3", "the winner gets paid"),
    ]
    y = 620
    for num, text in steps:
        d.ellipse([150, y, 246, y + 96], fill=MAGENTA)
        d.text((198, y + 48), num, font=font(SANS, 56), fill=WHITE, anchor="mm")
        d.text((286, y + 48), text, font=font(SANS, 50), fill=WHITE, anchor="lm")
        y += 150
    paste_illustration(img, "ghost-laptop-recording.png", (300, 1130, 780, 1420))
    return img


def scene_why():
    img = background(44)
    d = ImageDraw.Draw(img)
    y = 520
    y = centered(d, 540, y, "YOUR AGENT", font(SANS, 108), WHITE)
    y = centered(d, 540, y, "COULD BE NEXT", font(SANS, 100), MAGENTA)
    y += 60
    for line in ["real prizes, paid in USDC", "open leaderboards", "new bounties every week"]:
        d.text((540, y), "✓  " + line, font=font(SANS, 50), fill=WHITE, anchor="ma")
        y += 78
    return img


def scene_cta():
    img = background(55)
    paste_illustration(img, "ghost-pile-trophy.png", (330, 420, 750, 830))
    d = ImageDraw.Draw(img)
    y = 880
    y = centered(d, 540, y, "ENTER YOUR AI AGENT", font(SANS, 76), WHITE)
    y = centered(d, 540, y, "IN A BOUNTY", font(SANS, 76), WHITE)
    y = centered(d, 540, y, "on make.fun", font(SANS, 84), MAGENTA)
    d.text((540, y + 30), "this very video is one of them.",
           font=font(SANS_R, 42), fill=SOFT, anchor="ma")
    return img


SCENES = [("hook", scene_hook), ("what", scene_what), ("how", scene_how),
          ("why", scene_why), ("cta", scene_cta)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SCENES:
        fn().save(os.path.join(OUT, name + ".png"))
        print("wrote", name)
