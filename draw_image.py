#!/usr/bin/env python3
"""Draw the 18 November 2026 front page: 1024x1024, PIL + DejaVu only."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
PANEL = (255, 253, 245)
RULE = (18, 18, 18)
ACCENT = (158, 27, 34)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---- masthead ----
d.rectangle([0, 0, W, 4], fill=ACCENT)
title = "WEDNESDAY 18 NOVEMBER 2026"
tf = font(BOLD, 46)
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
sf = font(REG, 22)
sub = "Six stories that defined the day \u2014 from the Gulf to Shenzhen to Alaska"
sw = d.textlength(sub, font=sf)
d.text(((W - sw) / 2, 92), sub, font=sf, fill=(60, 60, 60))
d.line([32, 132, W - 32, 132], fill=RULE, width=3)
d.line([32, 138, W - 32, 138], fill=RULE, width=1)

# ---- icons ----
def icon_burst(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(24, 42, 74))
    cx, cy, r1, r2 = x + s / 2, y + s / 2, s * 0.42, s * 0.18
    pts = []
    for i in range(16):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(245, 166, 34))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(158, 27, 34))


def icon_flags(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(240, 236, 224))
    # China flag
    d.rectangle([x + 8, y + 14, x + s / 2 - 2, y + s - 14], fill=(222, 41, 16))
    d.ellipse([x + 14, y + 20, x + 20, y + 26], fill=(255, 222, 0))
    d.ellipse([x + 26, y + 20, x + 30, y + 24], fill=(255, 222, 0))
    # Russia flag
    d.rectangle([x + s / 2 + 2, y + 14, x + s - 8, y + s - 14], outline=(120, 120, 120))
    d.rectangle([x + s / 2 + 2, y + 14, x + s - 8, y + 14 + (s - 28) // 3], fill=(255, 255, 255))
    d.rectangle([x + s / 2 + 2, y + 14 + (s - 28) // 3, x + s - 8, y + 14 + 2 * (s - 28) // 3], fill=(0, 57, 166))
    d.rectangle([x + s / 2 + 2, y + 14 + 2 * (s - 28) // 3, x + s - 8, y + s - 14], fill=(213, 0, 50))


def icon_bridge(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 244))
    d.line([x + 6, y + s - 22, x + s - 6, y + s - 22], fill=(40, 40, 40), width=4)
    # left deck + tower, gap, right deck
    d.rectangle([x + 10, y + 18, x + 16, y + s - 22], fill=(40, 40, 40))
    d.rectangle([x + s - 16, y + 18, x + s - 10, y + s - 22], fill=(40, 40, 40))
    d.line([x + 13, y + 18, x + s / 2 - 14, y + s - 22], fill=(40, 40, 40), width=2)
    d.line([x + s / 2 + 14, y + s - 22, x + s - 13, y + 18], fill=(40, 40, 40), width=2)
    # falling span piece
    d.polygon([(x + s / 2 - 12, y + s - 34), (x + s / 2 + 12, y + s - 34),
               (x + s / 2 + 6, y + s - 12), (x + s / 2 - 6, y + s - 12)], fill=(158, 27, 34))


def icon_ballot(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(24, 42, 74))
    d.rectangle([x + 16, y + 34, x + s - 16, y + s - 12], fill=(255, 255, 255))
    d.rectangle([x + 16, y + 34, x + s - 16, y + 44], fill=(158, 27, 34))
    d.line([x + 26, y + s - 30, x + 36, y + s - 20], fill=(24, 42, 74), width=5)
    d.line([x + 36, y + s - 20, x + s - 26, y + s - 44], fill=(24, 42, 74), width=5)
    d.text((x + 8, y + 6), "56\u201344", font=font(BOLD, 18), fill=(255, 255, 255))


def icon_plane(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(52, 52, 52))
    # side-view plane, nose down-right, with a small flame at the nose
    d.polygon([(x + 12, y + 40), (x + 52, y + 28), (x + 64, y + 34),
               (x + 60, y + 40), (x + 26, y + 50)], fill=(220, 220, 220))
    d.polygon([(x + 20, y + 34), (x + 30, y + 18), (x + 36, y + 30)], fill=(180, 180, 180))
    d.polygon([(x + 34, y + 44), (x + 48, y + 58), (x + 42, y + 62), (x + 28, y + 50)], fill=(180, 180, 180))
    d.polygon([(x + 60, y + 36), (x + 72, y + 48), (x + 64, y + 52), (x + 56, y + 42)], fill=(245, 166, 34))


def icon_virus(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 244, 228))
    cx, cy = x + s / 2, y + s / 2
    for i in range(10):
        a = math.pi * 2 * i / 10
        d.line([cx + 20 * math.cos(a), cy + 20 * math.sin(a),
                cx + 30 * math.cos(a), cy + 30 * math.sin(a)], fill=(46, 125, 50), width=4)
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(76, 175, 80))
    d.ellipse([cx - 12, cy - 6, cx - 2, cy + 4], fill=(27, 94, 32))
    d.ellipse([cx + 4, cy + 2, cx + 12, cy + 10], fill=(27, 94, 32))
    d.ellipse([cx - 4, cy - 16, cx + 4, cy - 8], fill=(27, 94, 32))


ICONS = [icon_burst, icon_flags, icon_bridge, icon_ballot, icon_plane, icon_virus]

STORIES = [
    ("IRAN STRIKES KUWAIT AND BAHRAIN",
     "Tehran hits a US air base in Kuwait and targets in Bahrain, hours after the US struck Qeshm Island."),
    ("XI AND PUTIN MEET IN SHENZHEN",
     "China and Russia coordinate a day before their summit with Trump; Xi denounces protectionism."),
    ("KERCH BRIDGE SPAN FALLS",
     "A road span drops into the strait after a second day of Ukrainian strikes on the Crimea link."),
    ("PELTOLA WINS ALASKA; SENATE 56\u201344",
     "Democrat Mary Peltola unseats Dan Sullivan, giving Democrats the US Senate majority."),
    ("RUSSIAN MILITARY PLANE CRASHES",
     "All 19 aboard die as a transport aircraft comes down in Siberia's Kemerovo region."),
    ("EBOLA CASES MORE THAN DOUBLE",
     "DR Congo outbreak passes 11,000 cases and 5,400 deaths, the UN says; children hit hardest."),
]

# ---- grid ----
GX, GY, GW, GH, GAP = 32, 152, 473, 252, 14
hf = font(BOLD, 25)
bf = font(REG, 19)
for i, (head, body) in enumerate(STORIES):
    col, row = i % 2, i // 2
    px = GX + col * (GW + GAP)
    py = GY + row * (GH + GAP)
    d.rectangle([px, py, px + GW, py + GH], fill=PANEL, outline=RULE, width=2)
    ICONS[i](px + 14, py + 14, 76)
    hl = wrap(d, head, hf, GW - 14 - 76 - 14 - 14)
    draw_text_block(d, px + 104, py + 14, hl[:2], hf, leading=30)
    bl = wrap(d, body, bf, GW - 28)
    draw_text_block(d, px + 14, py + 104, bl[:3], bf, leading=25)
    d.line([px + 14, py + GH - 26, px + GW - 14, py + GH - 26], fill=(190, 184, 168), width=1)
    tag = ["GULF WAR", "DIPLOMACY", "UKRAINE", "US POLITICS", "DISASTER", "HEALTH"][i]
    d.text((px + 14, py + GH - 22), tag, font=font(BOLD, 14), fill=ACCENT)

# ---- footer ----
ff = font(REG, 15)
foot = "Sources: Reuters, AP, AFP, Just Security, NPR, UN \u2014 18 November 2026"
fw = d.textlength(foot, font=ff)
d.text(((W - fw) / 2, 992), foot, font=ff, fill=(90, 90, 90))

img.save("/home/hatch/workspace/makefun/news-image-20261118-repo/entry.png")
print("saved", img.size)
