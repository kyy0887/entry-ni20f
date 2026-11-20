#!/usr/bin/env python3
"""v3: PREMIUM EDITORIAL INFOGRAPHIC — 'The World In One Day' newspaper style.
Deterministic: no random, no timestamps. Fonts from absolute DejaVu paths.
RGB 1024x1024 paper-cream broadsheet."""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
PAPER = (244, 240, 229)
CARD = (250, 247, 240)
INK = (23, 23, 23)
RED = (182, 66, 60)
NAVY = (24, 50, 74)
BLUE = (84, 123, 145)
GREEN = (71, 119, 92)
GOLD = (179, 148, 87)
GREY = (110, 106, 96)
LIGHT = (214, 208, 192)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, int(size))

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- deterministic paper grain (per-pixel hash pattern) ----------
px = img.load()
for y in range(H):
    for x in range(W):
        hsh = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
        hsh = ((hsh ^ (hsh >> 13)) * 1274126177) & 0xFFFFFFFF
        v = (hsh >> 16) & 7
        if v == 0:
            r, g, b = px[x, y]
            px[x, y] = (r - 6, g - 6, b - 6) if r >= 6 else (0, 0, 0)
        elif v == 7:
            r, g, b = px[x, y]
            px[x, y] = (min(255, r + 4), min(255, g + 4), min(255, b + 4))
d = ImageDraw.Draw(img)

# ---------- helpers ----------
def tw(txt, font):
    return d.textlength(txt, font=font)

def wrap(txt, font, maxw):
    words = txt.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def fit_lines(txt, mkfont, size, maxw, maxlines, minsize=7):
    s = size
    while s >= minsize:
        f = mkfont(s)
        lines = wrap(txt, f, maxw)
        if len(lines) <= maxlines:
            return f, lines
        s -= 1
    return mkfont(minsize), wrap(txt, mkfont(minsize), maxw)

boxes = []
def mark(x0, y0, x1, y1, tag):
    boxes.append((x0, y0, x1, y1, tag))

def overlaps():
    bad = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 4 and oy > 4:
                bad.append((a[4], b[4]))
    return bad

def text_at(x, y, txt, font, fill=INK, anchor="la", tag=None):
    if tag:
        w_ = tw(txt, font)
        if anchor == "ma":
            x0 = x - w_ / 2
        elif anchor == "ra":
            x0 = x - w_
        else:
            x0 = x
        mark(x0, y, x0 + w_, y + font.size + 3, tag)
    d.text((x, y), txt, font=font, fill=fill, anchor=anchor)

def para(x, y, txt, mkfont, size, maxw, maxlines, fill=INK, tag=None):
    f, lines = fit_lines(txt, mkfont, size, maxw, maxlines)
    for ln in lines:
        text_at(x, y, ln, f, fill, tag=tag)
        y += int(f.size * 1.3)
    return y

def hline(y, x0=40, x1=W - 40, w_=1, fill=INK):
    d.rectangle([x0, y, x1, y + w_ - 1], fill=fill)

M = 40

# =====================================================================
# A. MASTHEAD (0..122)
# =====================================================================
text_at(W // 2, 10, "THE WORLD IN ONE DAY", SANS_B(12), GOLD, "ma", "mast-kicker")
text_at(W // 2, 26, "FRIDAY 20 NOVEMBER 2026", SERIF_B(42), INK, "ma", "mast-date")
text_at(W // 2, 80, "No. 1120  ·  Global Edition  ·  All items dated 20 November 2026 (UTC)", SANS(10), GREY, "ma", "mast-ed")
ed = ("Moscow unleashes roughly one hundred missiles on Kyiv as Cyclone Akvan drives 300,000 "
      "from India's coast; Asian markets log their worst week since 1991 while GTA VI takes $2.36bn in a day.")
f_ed, lns_ed = fit_lines(ed, SANS, 10, W - 2 * M, 2)
yy = 92
for ln in lns_ed:
    text_at(W // 2, yy, ln, f_ed, NAVY, "ma", "mast-edit")
    yy += 14
hline(118, M, W - M, 2)
hline(121, M, W - M, 1)

# =====================================================================
# B. KEY STATISTICS (124..192)
# =====================================================================
stats = [
    ("9+", "killed in Kyiv assault", RED),
    ("300K+", "evacuated, Odisha", GREEN),
    ("$2.36bn", "GTA VI day one", NAVY),
    ("-5.1%", "Nikkei to 56,436", BLUE),
    ("$93.5bn", "Anthropic IPO raised", GOLD),
]
colw = (W - 2 * M) / 5
for i, (num, cap, col) in enumerate(stats):
    cx = M + colw * (i + 0.5)
    fnum = SERIF_B(26 if len(num) <= 6 else 22)
    text_at(cx, 132, num, fnum, col, "ma", f"stat{i}n")
    text_at(cx, 166, cap, SANS(9), GREY, "ma", f"stat{i}c")
    if i:
        d.line([M + colw * i, 134, M + colw * i, 180], fill=LIGHT, width=1)

# =====================================================================
# C. REGION STRIP (192..232)
# =====================================================================
hline(190)
regions = [("EUROPE", 6, RED), ("ASIA-PACIFIC", 6, NAVY), ("MIDDLE EAST", 6, GREEN),
           ("AMERICAS", 4, BLUE), ("AFRICA", 3, GOLD), ("OCEANIA", 2, GREY), ("GLOBAL", 5, INK)]
rw = (W - 2 * M) / len(regions)
for i, (nm, n, col) in enumerate(regions):
    cx = M + rw * (i + 0.5)
    d.rectangle([cx - 3, 198, cx + 3, 204], fill=col)
    text_at(cx, 207, nm, SANS_B(9), col, "ma", f"reg{i}")
    text_at(cx, 219, f"{n} stories", SANS(8), GREY, "ma", f"reg{i}n")

# =====================================================================
# D. THREE LEAD STORIES (238..534)
# =====================================================================
py0 = 238
ph = 296
pw = (W - 2 * M - 2 * 10) / 3

def lead_frame(i, label, col):
    x0 = M + i * (pw + 10)
    d.rectangle([x0, py0, x0 + pw, py0 + ph], outline=INK, width=1)
    d.rectangle([x0, py0, x0 + pw, py0 + 16], fill=col)
    text_at(x0 + 8, py0 + 2, label, SANS_B(9), PAPER, "la", f"lead{i}lbl")
    return x0

def lead_text(x0, hy, head, sup, srctxt, srccol, tags):
    f_h, lns = fit_lines(head, SERIF_B, 15, pw - 14, 3)
    for ln in lns:
        text_at(x0 + 7, hy, ln, f_h, INK, tag=f"{tags}h{hy}")
        hy += int(f_h.size * 1.2)
    f_s, lns2 = fit_lines(sup, SANS, 9, pw - 14, 4)
    for ln in lns2:
        text_at(x0 + 7, hy + 6, ln, f_s, GREY, tag=f"{tags}s")
        hy += int(f_s.size * 1.3)
    text_at(x0 + 7, py0 + ph - 14, srctxt, SANS_B(8), srccol, "la", f"{tags}src")
    return hy

# ---- LEAD 1: RUSSIA-UKRAINE ----
x0 = lead_frame(0, "CONFLICT — KYIV", RED)
iy0 = py0 + 22
d.rectangle([x0 + 6, iy0, x0 + pw - 6, iy0 + 94], fill=(30, 34, 48))
sx = x0 + 6
sky = [(0, 38, 20), (22, 26, 34), (40, 44, 26), (58, 20, 40), (74, 34, 22), (100, 28, 30),
       (128, 40, 24), (150, 22, 38), (172, 30, 28), (196, 24, 34)]
for ox, hh, ww in sky:
    d.rectangle([sx + ox, iy0 + 94 - hh, sx + ox + ww, iy0 + 94], fill=(14, 16, 26))
d.pieslice([sx + 104, iy0 + 42, sx + 124, iy0 + 68], 180, 360, fill=(14, 16, 26))
d.rectangle([sx + 108, iy0 + 60, sx + 120, iy0 + 68], fill=(14, 16, 26))
d.polygon([(sx + 112, iy0 + 36), (sx + 114, iy0 + 44), (sx + 110, iy0 + 44)], fill=(14, 16, 26))
for xs, xe, yc in [(4, 60, 14), (24, 88, 30), (60, 116, 10), (10, 130, 44)]:
    d.line([sx + xs, iy0 + yc, sx + xe, iy0 + 58], fill=RED, width=2)
    d.ellipse([sx + xe - 3, iy0 + 55, sx + xe + 3, iy0 + 61], fill=RED)
for bx, by in [(70, 22), (110, 36), (40, 48)]:
    d.ellipse([sx + bx - 4, iy0 + by - 4, sx + bx + 4, iy0 + by + 4], outline=(240, 200, 120), width=1)
    d.line([sx + bx - 6, iy0 + by, sx + bx + 6, iy0 + by], fill=(240, 200, 120), width=1)
    d.line([sx + bx, iy0 + by - 6, sx + bx, iy0 + by + 6], fill=(240, 200, 120), width=1)
text_at(x0 + pw / 2, iy0 + 98, "82 missiles + 380 drones shot down", SANS_B(10), RED, "ma", "l1burst")
lead_text(x0, iy0 + 114,
          "Russia fires ~100 missiles overnight; 3 Kyiv bridges hit",
          "At least nine killed and dozens wounded as air defences engage a wave of cruise and ballistic missiles aimed at the capital.",
          "Reuters / AP", RED, "l1")

# ---- LEAD 2: CYCLONE AKVAN ----
x0 = lead_frame(1, "WEATHER — ODISHA, INDIA", GREEN)
iy0 = py0 + 22
d.rectangle([x0 + 6, iy0, x0 + pw - 6, iy0 + 94], fill=(223, 231, 233))
d.rectangle([x0 + 6, iy0 + 60, x0 + pw - 6, iy0 + 94], fill=(140, 175, 190))
d.polygon([(x0 + 6, iy0 + 94), (x0 + 6, iy0 + 38), (x0 + 30, iy0 + 32), (x0 + 58, iy0 + 50),
           (x0 + 86, iy0 + 58), (x0 + 120, iy0 + 70), (x0 + pw - 6, iy0 + 82), (x0 + pw - 6, iy0 + 94)],
          fill=(214, 205, 180))
coast = [(x0 + 30, iy0 + 32), (x0 + 58, iy0 + 50), (x0 + 86, iy0 + 58), (x0 + 120, iy0 + 70), (x0 + pw - 6, iy0 + 82)]
d.line(coast, fill=GREEN, width=2)
scx, scy, r0 = x0 + pw - 34, iy0 + 26, 26
for a in range(0, 540, 10):
    rr = 4 + a / 540 * r0
    aa = math.radians(a)
    px_, py_ = scx + rr * math.cos(aa), scy + rr * 0.8 * math.sin(aa)
    d.ellipse([px_ - 2, py_ - 2, px_ + 2, py_ + 2], fill=NAVY)
d.ellipse([scx - 5, scy - 5, scx + 5, scy + 5], fill=RED)
lx = x0 + 96
d.line([lx, iy0 + 58, lx, iy0 + 40], fill=RED, width=2)
d.polygon([(lx - 5, iy0 + 40), (lx + 5, iy0 + 40), (lx, iy0 + 33)], fill=RED)
text_at(lx, iy0 + 20, "Gopalpur", SANS_B(9), RED, "ma", "l2land")
text_at(x0 + pw - 70, iy0 + 84, "Bay of Bengal", SANS(8), (45, 75, 90), "la", "l2sea")
for k in range(3):
    yy0 = iy0 + 8 + k * 6
    d.line([x0 + 14, yy0, x0 + 44 + k * 8, yy0], fill=BLUE, width=1)
text_at(x0 + pw / 2, iy0 + 98, "70–90 km/h winds · 47 trains cancelled", SANS_B(10), GREEN, "ma", "l2burst")
lead_text(x0, iy0 + 114,
          "Cyclone Akvan makes landfall at Gopalpur; 300,000+ moved to safety",
          "Authorities evacuate coastal districts of Odisha ahead of the storm's arrival with 47 train services cancelled.",
          "Reuters / PTI / The Hindu", GREEN, "l2")

# ---- LEAD 3: MARKETS / GTA VI ----
x0 = lead_frame(2, "MARKETS — ASIA", NAVY)
iy0 = py0 + 22
d.rectangle([x0 + 6, iy0, x0 + pw - 6, iy0 + 94], fill=(236, 233, 222))
for gx in range(1, 5):
    gx_x = x0 + 6 + gx * (pw - 12) / 5
    d.line([gx_x, iy0 + 4, gx_x, iy0 + 86], fill=LIGHT, width=1)
for gy in range(1, 4):
    gy_y = iy0 + 4 + gy * 82 / 4
    d.line([x0 + 6, gy_y, x0 + pw - 6, gy_y], fill=LIGHT, width=1)
def path(pts, col):
    for k in range(len(pts) - 1):
        d.line([x0 + 8 + pts[k][0] * (pw - 16) / 100, iy0 + 4 + pts[k][1] * 82 / 100,
                x0 + 8 + pts[k + 1][0] * (pw - 16) / 100, iy0 + 4 + pts[k + 1][1] * 82 / 100], fill=col, width=2)
path([(0, 18), (15, 26), (30, 24), (45, 40), (60, 52), (75, 68), (100, 84)], RED)
path([(0, 22), (15, 30), (30, 34), (45, 44), (60, 58), (75, 64), (100, 78)], NAVY)
path([(0, 26), (15, 32), (30, 40), (45, 46), (60, 56), (75, 62), (100, 72)], BLUE)
for px_, py_, col in [(100, 84, RED), (100, 78, NAVY), (100, 72, BLUE)]:
    d.ellipse([x0 + 8 + px_ * (pw - 16) / 100 - 3, iy0 + 4 + py_ * 82 / 100 - 3,
               x0 + 8 + px_ * (pw - 16) / 100 + 3, iy0 + 4 + py_ * 82 / 100 + 3], fill=col)
bx = x0 + 14
for k, (hh, col) in enumerate([(12, GOLD), (26, GOLD), (44, RED)]):
    d.rectangle([bx + k * 16, iy0 + 90 - hh, bx + k * 16 + 10, iy0 + 90], fill=col)
text_at(x0 + 12, iy0 + 2, "3rd straight weekly decline", SANS(8), GREY, "la", "l3note")
text_at(x0 + pw / 2, iy0 + 98, "GTA VI: $2.36bn in 24h · 24.5m copies", SANS_B(10), NAVY, "ma", "l3burst")
lead_text(x0, iy0 + 114,
          "Asian equities log worst week since 1991 as GTA VI smashes launch records",
          "Taiwan -6.2%, KOSPI -5.2%, Nikkei -5.1% to 56,436.65; 75% of GTA VI sales on PlayStation.",
          "Reuters / Sensor Tower / CNBC", NAVY, "l3")

# =====================================================================
# E. SUPPORTING GRID (542..786): 9 cards, 3x3
# =====================================================================
gy0 = 542
cw = (W - 2 * M - 2 * 8) / 3
chh = 78
cards = [
    ("UK-EU RESET", "BRUSSELS", RED, "flag",
     "UK and EU agree 'reset' deal", "Eases food trade and youth mobility", "Reuters"),
    ("NATO CARD", "WASHINGTON", NAVY, "table",
     "US envoys float NATO path for Ukraine", "Membership discussed vs ceded territory", "WSJ"),
    ("SIBERIA CRASH", "SIBERIA", GREY, "plane",
     "Russian transport plane down", "19 killed in military crash", "CNN"),
    ("RIYADH STRIKE", "RIYADH", GREEN, "tower",
     "Houthi missile damages tallest tower", "HQ of PIF Saudi hit", "Al Jazeera/WSJ"),
    ("HORMUZ MINES", "STRAIT OF HORMUZ", BLUE, "tanker",
     "Third tanker strikes mine", "Shipping risk mounts in the strait", "IRNA"),
    ("SPEAKER BID", "WASHINGTON", RED, "gavel",
     "Democrats nominate Jeffries", "Party picks its candidate for Speaker", "Democracy Now"),
    ("ANTHROPIC IPO", "NEW YORK", GOLD, "chip",
     "Anthropic closes debut at $97.17", "Valuation $1.27tn, $93.5bn raised", "CNBC"),
    ("BITCOIN ETF", "US MARKETS", NAVY, "coin",
     "Bitcoin ETF outflow hits $582m", "November nears $3.5bn total", "The Block"),
    ("COP31 DEADLOCK", "ANTALYA", GREEN, "globe",
     "COP31 draft omits fossil fuels", "Africa Group demands grants, $190bn gap", "AP/DW"),
]

def icon(kind, x, y, col):
    if kind == "flag":
        d.line([x, y, x, y + 26], fill=INK, width=2)
        d.polygon([(x, y + 2), (x + 22, y + 6), (x, y + 12)], fill=RED)
        d.line([x + 11, y + 3, x + 11, y + 11], fill=(240, 238, 228), width=2)
    elif kind == "table":
        d.polygon([(x + 12, y), (x + 22, y + 10), (x + 12, y + 20), (x + 2, y + 10)], outline=col, width=2)
        d.ellipse([x + 2, y + 2, x + 8, y + 8], fill=RED)
        d.ellipse([x + 16, y + 2, x + 22, y + 8], fill=NAVY)
        d.ellipse([x + 9, y + 14, x + 15, y + 20], fill=GOLD)
    elif kind == "plane":
        d.line([x + 2, y + 24, x + 26, y + 4], fill=col, width=2)
        d.polygon([(x + 26, y + 4), (x + 34, y + 2), (x + 30, y + 9)], fill=col)
        d.line([x + 14, y + 13, x + 22, y + 24], fill=col, width=2)
        d.ellipse([x + 4, y + 22, x + 10, y + 28], outline=col, width=1)
        d.line([x + 5, y + 27, x + 9, y + 31], fill=GREY, width=1)
    elif kind == "tower":
        d.polygon([(x + 12, y), (x + 16, y + 28), (x + 8, y + 28)], fill=col)
        d.line([x + 4, y + 12, x + 20, y + 12], fill=col, width=1)
        d.line([x + 6, y + 19, x + 18, y + 19], fill=col, width=1)
        d.ellipse([x + 9, y + 4, x + 15, y + 10], outline=RED, width=2)
    elif kind == "tanker":
        d.polygon([(x, y + 16), (x + 30, y + 16), (x + 26, y + 24), (x + 4, y + 24)], fill=col)
        d.rectangle([x + 6, y + 6, x + 24, y + 16], fill=col)
        d.rectangle([x + 10, y + 2, x + 14, y + 6], fill=INK)
        d.line([x + 3, y + 28, x + 27, y + 28], fill=BLUE, width=2)
        d.ellipse([x + 18, y - 2, x + 24, y + 4], outline=RED, width=1)
    elif kind == "gavel":
        d.line([x + 2, y + 26, x + 24, y + 26], fill=INK, width=2)
        d.polygon([(x + 8, y + 26), (x + 18, y + 26), (x + 16, y + 12), (x + 10, y + 12)], fill=col)
        d.rectangle([x + 16, y + 2, x + 26, y + 8], fill=col)
    elif kind == "chip":
        d.rectangle([x + 4, y + 4, x + 24, y + 24], fill=col)
        d.rectangle([x + 9, y + 9, x + 19, y + 19], fill=CARD)
        for k in range(4):
            d.line([x + 2, y + 7 + k * 5, x + 4, y + 7 + k * 5], fill=INK, width=1)
            d.line([x + 24, y + 7 + k * 5, x + 26, y + 7 + k * 5], fill=INK, width=1)
            d.line([x + 7 + k * 5, y + 2, x + 7 + k * 5, y + 4], fill=INK, width=1)
    elif kind == "coin":
        d.ellipse([x + 4, y + 2, x + 22, y + 20], fill=GOLD)
        d.text((x + 13, y + 10), "$", font=SANS_B(11), fill=(60, 48, 20), anchor="mm")
        d.line([x + 2, y + 12, x + 30, y + 26], fill=RED, width=2)
        d.polygon([(x + 28, y + 20), (x + 32, y + 28), (x + 24, y + 26)], fill=RED)
    elif kind == "globe":
        d.ellipse([x, y, x + 26, y + 26], outline=col, width=2)
        d.ellipse([x + 6, y, x + 20, y + 26], outline=col, width=1)
        d.line([x, y + 13, x + 26, y + 13], fill=col, width=1)
        d.line([x + 4, y + 6, x + 22, y + 6], fill=col, width=1)
        d.line([x + 4, y + 20, x + 22, y + 20], fill=col, width=1)
        d.line([x, y + 28, x + 12, y + 32], fill=INK, width=2)
        d.line([x + 14, y + 28, x + 26, y + 32], fill=INK, width=2)

for i, (cat, loc, col, ic, head, det, src) in enumerate(cards):
    r, c = divmod(i, 3)
    x0 = M + c * (cw + 8)
    y0 = gy0 + r * (chh + 6)
    d.rectangle([x0, y0, x0 + cw, y0 + chh], outline=LIGHT, width=1, fill=CARD)
    d.rectangle([x0, y0, x0 + 4, y0 + chh], fill=col)
    icon(ic, x0 + cw - 36, y0 + 6, col)
    text_at(x0 + 9, y0 + 4, cat, SANS_B(9), col, "la", f"card{i}cat")
    text_at(x0 + 9, y0 + 15, loc, SANS(7), GREY, "la", f"card{i}loc")
    f_h, lns = fit_lines(head, SERIF_B, 11, cw - 48, 2)
    yy = y0 + 27
    for ln in lns:
        text_at(x0 + 9, yy, ln, f_h, INK, tag=f"card{i}h")
        yy += int(f_h.size * 1.15)
    f_s, lns2 = fit_lines(det, SANS, 8, cw - 18, 2)
    for ln in lns2:
        text_at(x0 + 9, yy + 2, ln, f_s, GREY, tag=f"card{i}d")
        yy += int(f_s.size * 1.25)
    text_at(x0 + 9, y0 + chh - 12, src, SANS_B(7), col, "la", f"card{i}s")
hline(786, M, W - M, 1)

# =====================================================================
# F. WORLD MAP 'WHERE IT HAPPENED' (788..902)
# =====================================================================
text_at(M, 788, "WHERE IT HAPPENED", SANS_B(12), INK, "la", "mapt")
text_at(M + 152, 793, "Ten places that made the front page", SANS(8.5), GREY, "la", "mapsub")
d.line([M, 803, W - M, 803], fill=LIGHT, width=1)

mask = [
"....................................................................",
".....LL.............HHHHHHHHHHH..........BBBBBBBB....................",
"....LLAAA..AAAA....HHHHHHHHHHHHHH......BBBBBBBBBBBB...KKKKK.........",
"...LLAAAAAAAAAAAA.HHHHHHHHHHHHHHHH..BBBBBBBBBBBBBBBB.BKKKKKKK.......",
"....AAAAAAAAAAAA.HHHHHHHHHHHHHHHHBBBBBBBBBBBBBBBBBBBBKKKKKKKKK......",
".....AAAAAAAAA....HHHHHHHHHHHHHBBBBBBBBBBBBBBBBBBBBKKKKKKKKKKK......",
"......CCAAAA......HHHHHHHHHHHBBBBBBBBBBBBBBBBBBBKKKKKKKKKKKKK.......",
"......CCCA.........HHHHHHHH..BBBBBBBBBBBBBBBBBBBKKKKKKKKKKK.........",
".......CC...................BBBBBBBBBBBBBBBBBB.KKKKKKKKK............",
"........C...................BBBBBBBBBBBBBBBBB....KKKKK....FFF.......",
"........C....................BBBBBBBBBBBBBB..............FFFFFF......",
".........C...................BBBBBBBBBBBB................FFFFFFF.....",
"..........CC..................BBBBBBBBBB......D..........FFFFFF......",
"...........C...................BBBBBBB....................FFFF.......",
"............CC.................BBBB.B......................FF........",
".............C.................BB..........................F.........",
"..............CC...............B......................................",
"...............C........GG............................................",
"........................GGGG..........................................",
"........................GGGG..........................................",
".........................GG...........................................",
]
CXM, CYM = 5.6, 4.55
MX, MY = M + 10, 807
for r, row in enumerate(mask):
    for c, ch in enumerate(row):
        if ch != ".":
            cx = MX + c * CXM
            cy = MY + r * CYM
            d.ellipse([cx, cy, cx + 3.6, cy + 3.6], fill=(158, 152, 136))

# markers: (num, col, row, label, colour, side)
markers = [
    # Europe/Middle East cluster spread out to avoid collisions
    (1, 20.5, 5.2, "Kyiv", RED, 1),          # Eastern Europe, label right
    (4, 23.5, 6.2, "Hormuz", BLUE, 1),       # Gulf, label right over Iran
    (3, 21.0, 8.6, "Riyadh", RED, -1),       # Arabia, label left over Africa
    (2, 23.5, 12.4, "Odisha", GREEN, 1),     # India east coast
    (5, 50.0, 4.4, "Shenzhen", NAVY, 1),     # South China
    (6, 17.0, 6.6, "Antalya", GOLD, -1),     # Anatolia, label left over Med.
    (7, 11.0, 3.4, "New York", RED, -1),     # US east coast
    (8, 54.0, 15.4, "Canberra", GREEN, -1),  # SE Australia
    (9, 11.0, 11.6, "Lagos", GOLD, 1),       # West Africa coast
    (10, 10.0, 15.6, "Brasília", BLUE, -1),  # Brazil
]

for num, gx, gy, name, col, side in markers:
    cx = MX + gx * CXM
    cy = MY + gy * CYM
    d.rectangle([cx - 5.5, cy - 5.5, cx + 5.5, cy + 5.5], fill=col, outline=PAPER, width=1)
    d.text((cx, cy - 1), str(num), font=SANS_B(7.5), fill=PAPER, anchor="mm")
    if num == 1:
        text_at(cx, cy - 15, name, SANS(7.5), INK, "ma", f"mk{num}")
        d.line([cx, cy - 9, cx, cy - 5], fill=col, width=1)
    elif side > 0:
        d.line([cx + 5, cy, cx + 10, cy], fill=col, width=1)
        text_at(cx + 12, cy - 6, name, SANS(7.5), INK, "la", f"mk{num}")
    else:
        d.line([cx - 5, cy, cx - 10, cy], fill=col, width=1)
        text_at(cx - 12, cy - 6, name, SANS(7.5), INK, "ra", f"mk{num}")

# legend: two columns on the right of the map
lx0 = 662
text_at(lx0, 806, "LEGEND", SANS_B(9), INK, "la", "legt")
legend = [("1", RED, "Kyiv missile assault"), ("2", GREEN, "Cyclone Akvan landfall"),
          ("3", RED, "Riyadh tower strike"), ("4", BLUE, "Hormuz mine strike"),
          ("5", NAVY, "GTA VI / Asian selloff"), ("6", GOLD, "COP31 Antalya"),
          ("7", RED, "Jeffries / Anthropic IPO"), ("8", GREEN, "ASX slide, WBBL final"),
          ("9", GOLD, "COP31 Africa Group"), ("10", BLUE, "Americas markets")]
for k, (n, col, lb) in enumerate(legend):
    cc, rr = divmod(k, 5)
    yy = 818 + rr * 13
    lx = lx0 + cc * 172
    d.rectangle([lx, yy, lx + 10, yy + 9], fill=col)
    d.text((lx + 5, yy + 4), n, font=SANS_B(7), fill=PAPER, anchor="mm")
    text_at(lx + 15, yy + 1, lb, SANS(7.5), INK, "la", f"leg{k}")
d.line([lx0 - 10, 812, lx0 - 10, 880], fill=LIGHT, width=1)

# =====================================================================
# G. 'ALSO ON FRIDAY' (906..990): 3 columns x 7 briefs = 20
# =====================================================================
text_at(M, 906, "ALSO ON FRIDAY", SANS_B(11), INK, "la", "alsot")
text_at(M + 118, 910, "Twenty more dispatches from the same edition", SANS(8), GREY, "la", "alsosub")
d.line([M, 920, W - M, 920], fill=LIGHT, width=1)
briefs = [
    ("BERLIN", "Merz: Ukraine talks with Europe 'soon' (DW)"),
    ("MADRID", "Sanchez and Feijoo clash in TV debate (POLITICO)"),
    ("JAKARTA", "Xi and Prabowo open China-Indonesia talks (Xinhua)"),
    ("TAIPEI", "9 ships, 8 aircraft, 4 balloons tracked (Taiwan News)"),
    ("NEW DELHI", "Modi opens SCO Civilisational Dialogue (DD India)"),
    ("GALLE", "Pakistan seal 2-0 Test series over Sri Lanka (ESPNcricinfo)"),
    ("WASHINGTON", "Trump defers Iran strike decision to 2027 (CBS)"),
    ("LONDON", "Oil up Friday but third weekly fall (Reuters)"),
    ("GAZA", "22,000+ children killed since Oct 2023 (Anadolu)"),
    ("GAZA", "Central incursion displaces more families (Gaza Herald)"),
    ("WASHINGTON", "Mullin pressed on ICE custody deaths (Democracy Now)"),
    ("NAIROBI", "Africa Group wants grants not loans (DW)"),
    ("ADDIS ABABA", "AU urges higher domestic health budgets (Channel Africa)"),
    ("SYDNEY", "ASX 200 down 1.6% to 8,592.60 (AP)"),
    ("ADELAIDE", "Strikers win WBBL final by five wickets (cricket.com.au)"),
    ("ATLANTA", "US loses measles elimination status (UNICEF/PAHO)"),
    ("BETHESDA", "Endometriosis pathways mapped in 1M+ people (NIH)"),
    ("LUND", "Galectin-3 speeds Alzheimer's damage (Lund Univ.)"),
    ("CUPERTINO", "Gemini gets computer-use on Mac (TechCrunch)"),
    ("SANTA CLARA", "OpenAI models speed AMD chip design, +14% PPA (OpenAI/AMD)"),
]
NB_COLS = 3
nbcw = (W - 2 * M - 2 * 10) / NB_COLS
percol = 7
# pick font size so every line fits its column
def brief_line(n, loc, txt):
    return f"{n}. {loc} \u2014 {txt}"

bfont = None
for sz in [8.5, 8.4, 8.3, 8.2, 8.1, 8.0, 7.9, 7.8, 7.7, 7.6, 7.5, 7.4, 7.3, 7.2, 7.1, 7.0, 6.9]:
    f = SANS(sz)
    worst = max(tw(brief_line(21 + i, b[0], b[1]), f) for i, b in enumerate(briefs))
    avail = min(nbcw - 8, colw2_avail if False else nbcw - 8)
    if worst <= nbcw - 8:
        bfont = f
        break
if bfont is None:
    bfont = SANS(6.8)
for i, (loc, txt) in enumerate(briefs):
    cc, rr = divmod(i, percol)
    bx = M + cc * (nbcw + 10)
    yy = 926 + rr * 9
    n = 21 + i
    d.text((bx, yy), f"{n}.", font=SANS_B(7.5), fill=RED)
    nw = tw(f"{n}.", SANS_B(7.5))
    text_at(bx + nw + 3, yy, f"{loc} \u2014 {txt}", bfont, INK, "la", f"bf{n}")
for cc in range(1, NB_COLS):
    d.line([M + cc * (nbcw + 10) - 5, 924, M + cc * (nbcw + 10) - 5, 986], fill=LIGHT, width=1)

# =====================================================================
# H. FOOTER (990..1024)
# =====================================================================
hline(990, M, W - M, 1)
text_at(W // 2, 994, "DATE CHECK: All stories occurred or were first reported on Friday, November 20, 2026 (UTC)",
        SANS_B(8), NAVY, "ma", "foot1")
text_at(W // 2, 1006,
        "Sources: Reuters - AP - AFP - BBC - Al Jazeera - WSJ - Bloomberg - CNBC - Xinhua - DW - The Hindu - POLITICO - NIH - UNICEF",
        SANS(8), GREY, "ma", "foot2")
hline(1020, M, W - M, 1)

# ---------- QA ----------
ov = overlaps()
print("OVERLAPS:", ov if ov else "none")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print("entry.png bytes:", os.path.getsize(out))
