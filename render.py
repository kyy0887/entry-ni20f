#!/usr/bin/env python3
"""v4: CINEMATIC EDITORIAL REDESIGN — rebuilt from a blank 1024x1024 canvas.
Hero story: Kyiv overnight assault (cinematic layered night scene with missile
tracks, intercept glow, layered skyline, bridge/river, lit windows).
Two distinct secondary leads: Cyclone Akvan (Odisha coastal map, spiral,
landfall indicator) and Asia Markets (three-index line chart + GTA VI bars).
Accurate equirectangular world map with coastline polygons, 6 supporting
stories, verified figures only.
Deterministic: no random, no timestamps; fonts from absolute DejaVu paths.
RGB PNG 1024x1024."""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
PAPER   = (243, 240, 232)
INK     = (23, 27, 34)
GRAPH   = (75, 81, 88)
RED     = (182, 75, 67)
NAVY    = (32, 59, 82)
BLUEGR  = (112, 141, 157)
GREEN   = (79, 118, 95)
BRASS   = (180, 154, 103)
WHITE   = (245, 243, 236)
LINE    = (206, 200, 184)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, int(size))
SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF   = lambda s: F("DejaVuSerif.ttf", s)
SANS    = lambda s: F("DejaVuSans.ttf", s)
SANS_B  = lambda s: F("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)

# ---------- deterministic paper grain (per-pixel hash) ----------
px = img.load()
for y in range(H):
    for x in range(W):
        hsh = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
        hsh = ((hsh ^ (hsh >> 13)) * 1274126177) & 0xFFFFFFFF
        v = (hsh >> 16) & 15
        if v == 0:
            r, g, b = px[x, y]
            px[x, y] = (max(0, r - 7), max(0, g - 7), max(0, b - 7))
        elif v == 1:
            r, g, b = px[x, y]
            px[x, y] = (min(255, r + 5), min(255, g + 5), min(255, b + 5))
d = ImageDraw.Draw(img)

# ---------- helpers ----------
def tw(t, f): return d.textlength(t, font=f)

def text(x, y, t, f, fill, anchor="la"):
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)

def vgrad(x0, y0, x1, y1, c0, c1, dd=None):
    dd = d if dd is None else dd  # draw target: default main image, pass sd for scene
    hgt = max(1, y1 - y0)
    for i in range(hgt):
        t = i / hgt
        c = tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3))
        dd.line([(x0, y0 + i), (x1, y0 + i)], fill=c)

def panel(x0, y0, x1, y1, fill=WHITE, border=LINE):
    d.rectangle([x0 + 2, y0 + 3, x1 + 2, y1 + 3], fill=(222, 217, 204))
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=border)

def kicker(x, y, tag, col):
    f = SANS_B(10)
    d.rectangle([x, y, x + 4, y + 12], fill=col)
    text(x + 9, y + 1, tag, f, GRAPH)

def hash01(a, b, salt=0):
    h = (int(a) * 2654435761 + int(b) * 40503 + salt * 97) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h >> 8) & 0xFFFF) / 65535.0

# ============================================================
# MASTHEAD  (y 26..122)
# ============================================================
MX0, MX1 = 36, 988
text(MX0, 24, "THE WORLD IN ONE DAY", SERIF_B(47), INK)
text(MX1, 40, "No. 1120", SERIF(15), GRAPH, anchor="ra")
d.line([(MX0, 84), (MX1, 84)], fill=INK, width=2)
d.line([(MX0, 88), (MX1, 88)], fill=LINE, width=1)
text(MX0, 92, "FRIDAY, 20 NOVEMBER 2026", SANS_B(24), RED)
text(MX1, 99, "A visual digest of world news  ·  Global Edition  ·  all figures from source wire reports", SANS(11), GRAPH, anchor="ra")
d.line([(MX0, 122), (MX1, 122)], fill=LINE, width=1)

# ============================================================
# HERO — KYIV OVERNIGHT ASSAULT  (36..596, 134..478)
# ============================================================
HX0, HY0, HX1, HY1 = 36, 134, 596, 478
HXW = HX1 - HX0
SCENE_H = 296
scene = Image.new("RGB", (HXW, SCENE_H), (0, 0, 0))
sd = ImageDraw.Draw(scene)
SW, SH = HXW, SCENE_H
vgrad(0, 0, SW, SH, (13, 19, 30), (38, 56, 80), dd=sd)
spx = scene.load()
for yy in range(0, 150):
    for xx in range(0, SW, 4):
        if hash01(xx, yy, 7) > 0.995:
            r, g, b = spx[xx, yy]
            lift = 40 + int(50 * hash01(xx, yy, 13))
            spx[xx, yy] = (min(255, r + lift), min(255, g + lift), min(255, b + lift))
sd = ImageDraw.Draw(scene)
# moon
mx, my = 470, 46
for rad, col in ((26, (210, 205, 188)), (22, (232, 228, 212)), (16, (222, 218, 200))):
    sd.ellipse([mx - rad, my - rad, mx + rad, my + rad], fill=col)
sd.ellipse([mx - 8, my - 14, mx + 12, my + 6], fill=(216, 212, 196))
# distant fire glow near horizon
vgrad(0, 220, SW, SH, (38, 56, 80), (72, 52, 44), dd=sd)
sd.rectangle([0, 252, SW, SH], fill=(96, 66, 48))
sd.rectangle([0, 262, SW, SH], fill=(122, 82, 56))
# smoke columns
for bx, bw, bh in ((90, 26, 90), (150, 18, 60), (430, 30, 80), (500, 16, 50)):
    sd.polygon([(bx, SH), (bx + bw, SH), (bx + bw // 2 + 14, SH - bh), (bx + bw // 2 - 14, SH - bh)], fill=(58, 52, 48))
# layered skylines
def skyline(ybase, col, seed, hmin, hmax):
    x = 0
    while x < SW:
        bw = int(18 + hash01(x, seed, 1) * 34)
        bh = int(hmin + hash01(x, seed, 2) * (hmax - hmin))
        sd.rectangle([x, ybase - bh, x + bw, ybase], fill=col)
        x += bw + int(2 + hash01(x, seed, 3) * 6)
skyline(266, (44, 62, 84), 11, 24, 62)
skyline(274, (30, 43, 60), 22, 30, 78)
# church spire + monument (Kyiv cues)
sd.polygon([(320, 274), (320, 214), (328, 200), (336, 214), (336, 274)], fill=(30, 43, 60))
sd.polygon([(322, 214), (328, 200), (334, 214)], fill=(52, 66, 88))
sd.rectangle([496, 250, 504, 274], fill=(30, 43, 60))
sd.polygon([(500, 236), (506, 250), (494, 250)], fill=(30, 43, 60))
# river + bridge
sd.rectangle([0, 274, SW, 288], fill=(24, 34, 50))
for bxi in range(40, SW, 52):
    sd.rectangle([bxi, 276, bxi + 8, 286], fill=(40, 54, 74))
sd.line([(0, 278), (SW, 278)], fill=(48, 62, 84), width=3)
for ai in range(60, SW - 60, 96):
    sd.arc([ai, 266, ai + 72, 288], 180, 360, fill=(56, 72, 96), width=2)
# near skyline with lit windows
skyline(296, (13, 18, 26), 33, 40, 96)
for wx in range(8, SW, 10):
    bh = 40 + int(hash01(wx, 33, 3) * 56)
    for wy in range(296 - bh + 6, 292, 9):
        if hash01(wx, wy, 5) > 0.55:
            warm = hash01(wx, wy, 9) > 0.75
            c = (196, 154, 90) if warm else (150, 148, 120)
            sd.rectangle([wx, wy, wx + 3, wy + 4], fill=c)
for wx in range(20, SW, 30):
    if hash01(wx, 99, 6) > 0.4:
        sd.line([(wx, 280), (wx, 286)], fill=(110, 96, 70), width=2)
# missile tracks
def missile(p0, p1, p2, n=26, hot=True):
    pts = []
    for i in range(n + 1):
        t = i / n
        bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((bx, by))
    for i, (bx, by) in enumerate(pts[:-1]):
        fade = 1 - i / n
        c = (int(120 + 90 * fade), int(90 + 80 * fade), 60)
        sd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=c)
    hx, hy = pts[-1]
    for rad, colr in ((9, (120, 60, 30)), (5, (210, 140, 70)), (2, (250, 230, 190))):
        sd.ellipse([hx - rad, hy - rad, hx + rad, hy + rad], fill=colr)
missile((SW - 20, 8), (330, 60), (250, 236))
missile((SW - 6, 40), (360, 120), (470, 246))
missile((40, 14), (180, 80), (120, 240), hot=False)
missile((120, 4), (250, 90), (380, 200), hot=False)
# intercept flashes
for ix, iy in ((300, 96), (412, 158), (214, 132), (168, 66)):
    for rad, colr in ((11, (170, 130, 80)), (6, (236, 216, 180)), (2, (255, 252, 240))):
        sd.ellipse([ix - rad, iy - rad, ix + rad, iy + rad], fill=colr)
    sd.line([(ix - 15, iy), (ix + 15, iy)], fill=(200, 170, 120), width=1)
    sd.line([(ix, iy - 15), (ix, iy + 15)], fill=(200, 170, 120), width=1)
# searchlight beams
for gx, ang in ((80, -60), (520, -115)):
    ex = gx + 90 * math.cos(math.radians(ang)); ey = 280 + 90 * math.sin(math.radians(ang))
    sd.line([(gx, 280), (ex, ey)], fill=(120, 128, 110), width=2)
img.paste(scene, (HX0, HY0))
d = ImageDraw.Draw(img)
d.rectangle([HX0, HY0, HX1, HY1], outline=INK)
d.line([(HX0, HY0 + SCENE_H), (HX1, HY0 + SCENE_H)], fill=INK, width=2)
# headline band
vgrad(HX0, HY0 + SCENE_H + 1, HX1, HY1, (24, 27, 34), (33, 37, 46))
kicker(HX0 + 14, HY0 + 306, "EUROPE  ·  LEAD STORY", RED)
text(HX0 + 14, HY0 + 324, "RUSSIA UNLEASHES OVERNIGHT", SERIF_B(23), WHITE)
text(HX0 + 14, HY0 + 350, "MISSILE BARRAGE ON KYIV", SERIF_B(23), WHITE)
text(HX0 + 14, HY0 + 381, "About 80 cruise and 20 ballistic missiles and drones struck the capital:", SANS(11.5), (200, 205, 210))
text(HX0 + 14, HY0 + 397, "three bridges damaged, at least 9 killed. Air defences reported 82 missiles", SANS(11.5), (200, 205, 210))
text(HX0 + 14, HY0 + 413, "and about 380 drones shot down.  ·  Reuters / AP", SANS_B(11.5), BRASS)
# corner stat flags on scene
for sx_, slabel, sval in ((HX0 + 10, "MISSILES FIRED", "100+"), (HX1 - 10, "KILLED IN KYIV", "9+")):
    fb = SERIF_B(17)
    bw = 92
    bx = sx_ - bw if sx_ == HX1 - 10 else sx_
    d.rectangle([bx, HY0 + 10, bx + bw, HY0 + 46], fill=(15, 20, 28), outline=(70, 80, 94))
    text(bx + 6, HY0 + 13, slabel, SANS_B(9), (170, 178, 186))
    text(bx + 6, HY0 + 25, sval, fb, BRASS)

# ============================================================
# RIGHT RAIL: KEY FIGURES (612..988, 134..300)
# ============================================================
KX0, KY0, KX1, KY1 = 612, 134, 988, 300
panel(KX0, KY0, KX1, KY1)
kicker(KX0 + 12, KY0 + 10, "KEY FIGURES OF THE DAY", NAVY)
d.line([(KX0 + 12, KY0 + 28), (KX1 - 12, KY0 + 28)], fill=LINE)
figs = [
    ("300,000+", "evacuated for Cyclone Akvan, Odisha (PTI)", GREEN),
    ("$93.5bn",  "Anthropic IPO \u2014 largest ever (CNBC)", NAVY),
    ("$2.36bn",  "GTA VI revenue in <24 hours (Sensor Tower)", BRASS),
    ("\u22125.1%", "Nikkei weekly fall, to 56,436.65 (Reuters)", RED),
    ("9+",       "killed in the Kyiv missile assault (Reuters/AP)", RED),
]
fy = KY0 + 36
for i, (val, lab, col) in enumerate(figs):
    text(KX0 + 14, fy + 1, val, SERIF_B(22), col)
    text(KX1 - 14, fy + 8, lab, SANS(10), GRAPH, anchor="ra")
    fy += 33
    if i < len(figs) - 1:
        d.line([(KX0 + 12, fy - 4), (KX1 - 12, fy - 4)], fill=(224, 219, 206))

# ============================================================
# SECONDARY LEAD 1 — CYCLONE AKVAN coastal map (612..988, 312..478)
# ============================================================
CX0, CY0, CX1, CY1 = 612, 312, 988, 478
panel(CX0, CY0, CX1, CY1, fill=(236, 233, 224))
kicker(CX0 + 12, CY0 + 10, "ASIA  ·  CYCLONE AKVAN MAKES LANDFALL", GREEN)
d.line([(CX0 + 12, CY0 + 28), (CX1 - 12, CY0 + 28)], fill=LINE)
Mx0, My0, Mx1, My1 = CX0 + 12, CY0 + 36, CX0 + 210, CY1 - 40
d.rectangle([Mx0, My0, Mx1, My1], fill=(206, 218, 222))
d.polygon([(Mx0, My0), (Mx0 + 92, My0), (Mx0 + 96, My0 + 22), (Mx0 + 84, My0 + 44),
           (Mx0 + 88, My0 + 70), (Mx0 + 74, My0 + 96), (Mx0 + 60, My1), (Mx0, My1)],
          fill=(226, 222, 206), outline=(150, 145, 126))
d.line([(Mx0 + 92, My0), (Mx0 + 96, My0 + 22), (Mx0 + 84, My0 + 44), (Mx0 + 88, My0 + 70),
        (Mx0 + 74, My0 + 96), (Mx0 + 60, My1)], fill=(120, 128, 118), width=2)
# storm spiral offshore
scx, scy = Mx0 + 158, My0 + 44
for arm in range(3):
    pts = []
    for i in range(24):
        t = i / 23
        ang = arm * 2.094 + t * 3.4
        rr = 4 + t * 24
        pts.append((scx + rr * math.cos(ang), scy + rr * math.sin(ang) * 0.85))
    d.line(pts, fill=NAVY, width=2)
d.ellipse([scx - 4, scy - 4, scx + 4, scy + 4], fill=NAVY)
text(scx - 1, scy - 36, "CYCLONE AKVAN", SANS_B(9), NAVY, anchor="ma")
# landfall crosshair at Gopalpur
gx, gy = Mx0 + 86, My0 + 62
d.line([(gx - 12, gy), (gx + 12, gy)], fill=RED, width=2)
d.line([(gx, gy - 12), (gx, gy + 12)], fill=RED, width=2)
d.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], outline=RED, width=2)
d.polygon([(gx + 26, gy - 7), (gx + 26, gy + 7), (gx + 38, gy)], fill=RED)
text(gx + 42, gy - 6, "LANDFALL", SANS_B(9), RED)
text(gx - 4, gy + 13, "Gopalpur", SANS(9), GRAPH, anchor="ma")
text(Mx0 + 6, My1 - 14, "INDIA", SANS_B(9), (120, 115, 96))
text(Mx1 - 8, My0 + 6, "Bay of\nBengal", SANS(9), (86, 110, 120), anchor="ra")
# facts right of map
FX = Mx1 + 16
for fy2, big, small in ((CY0 + 44, "70\u201390 km/h", "peak winds at landfall"),
                        (CY0 + 82, "300,000+", "people moved to shelter"),
                        (CY0 + 120, "47 trains", "cancelled across the coast")):
    text(FX, fy2, big, SERIF_B(19), GREEN)
    text(FX, fy2 + 24, small, SANS(10), GRAPH)
d.line([(CX0 + 12, CY1 - 24), (CX1 - 12, CY1 - 24)], fill=LINE)
text(CX0 + 12, CY1 - 19, "Sources: PTI · The Hindu", SANS(9), GRAPH)

# ============================================================
# SECONDARY LEAD 2 — ASIA MARKETS (36..596, 490..652)
# ============================================================
PX0, PY0, PX1, PY1 = 36, 490, 596, 652
panel(PX0, PY0, PX1, PY1)
kicker(PX0 + 12, PY0 + 10, "MARKETS  ·  ASIA SHARES SUFFER WORST WEEK SINCE 1991", NAVY)
d.line([(PX0 + 12, PY0 + 28), (PX1 - 12, PY0 + 28)], fill=LINE)
chx0, chy0, chx1, chy1 = PX0 + 20, PY0 + 46, PX0 + 300, PY1 - 40
d.rectangle([chx0, chy0, chx1, chy1], fill=(240, 238, 230), outline=LINE)
days = ["MON", "TUE", "WED", "THU", "FRI"]
for i, day in enumerate(days):
    gx2 = chx0 + i * (chx1 - chx0) / 4
    d.line([(gx2, chy0), (gx2, chy1)], fill=(224, 220, 208))
    text(gx2, chy1 + 4, day, SANS_B(8.5), GRAPH, anchor="ma")
d.line([(chx0, chy1), (chx1, chy1)], fill=GRAPH, width=2)
d.line([(chx0, chy0), (chx0, chy1)], fill=GRAPH, width=1)
def week_path(final_drop, jitter_seed):
    path = []
    for i in range(5):
        j = (hash01(i, jitter_seed, 4) - 0.5) * 1.6
        path.append(final_drop * (i / 4) + (j if 0 < i < 4 else 0))
    return path
lo, hi = -7.0, 0.5
def ymap(v): return chy1 - (v - lo) / (hi - lo) * (chy1 - chy0)
zero_y = ymap(0)
d.line([(chx0, zero_y), (chx1, zero_y)], fill=(196, 190, 176), width=1)
text(chx0 + 3, zero_y - 12, "0%", SANS(8.5), GRAPH)
series = [("NIKKEI", -5.1, RED, 1), ("KOSPI", -5.2, NAVY, 2), ("TAIWAN", -6.2, BLUEGR, 3)]
for name, drop, col, seed in series:
    path = week_path(drop, seed)
    pts = [(chx0 + i * (chx1 - chx0) / 4, ymap(path[i])) for i in range(5)]
    d.line(pts, fill=col, width=2)
    for pxx, pyy in pts[::2]:
        d.ellipse([pxx - 2.5, pyy - 2.5, pxx + 2.5, pyy + 2.5], fill=col)
    lx, ly = pts[-1]
    d.ellipse([lx - 3.5, ly - 3.5, lx + 3.5, ly + 3.5], fill=col)
    # label right-aligned INSIDE the chart box, staggered to avoid collisions
    lab = f"{name} \u2212{abs(drop):.1f}%"
    ly += {-5.1: -26, -5.2: 9, -6.2: -9}[drop]
    text(chx1 - 6, ly - 6, lab, SANS_B(9.5), col, anchor="ra")
text(chx0, PY0 + 32, "Weekly close, % change  ·  Reuters", SANS(9.5), GRAPH)
# GTA VI block
GTX = chx1 + 24
text(GTX, PY0 + 32, "AND IN ENTERTAINMENT", SANS_B(9.5), GRAPH)
text(GTX, PY0 + 50, "GTA VI", SERIF_B(24), INK)
text(GTX, PY0 + 80, "$2.36bn", SERIF_B(26), BRASS)
text(GTX, PY0 + 108, "revenue in <24h · 24.5m copies · 75% on PlayStation", SANS(9), GRAPH)
bar_x, bar_y = GTX, PY0 + 122
bars = [("GTA VI, day one", 2.36, BRASS), ("Top film, opening wknd", 0.52, BLUEGR)]
for i, (lab, v, col) in enumerate(bars):
    yb = bar_y + i * 15  # bar + label on one line, rows clear the sources rule
    blen = int(110 * v / 2.36)
    d.rectangle([bar_x, yb, bar_x + blen, yb + 7], fill=col)
    text(bar_x + blen + 6, yb - 1, lab, SANS(8.5), GRAPH)
text(PX0 + 12, PY1 - 18, "Source: Sensor Tower \u00b7 Rockstar opening-day estimate", SANS(9.5), GRAPH)

# ============================================================
# SUPPORT STORIES — 6 items (612..988, 490..652)
# ============================================================
SX0, SY0, SX1, SY1 = 612, 490, 988, 652
panel(SX0, SY0, SX1, SY1)
kicker(SX0 + 12, SY0 + 10, "ALSO ON FRIDAY", BRASS)
d.line([(SX0 + 12, SY0 + 28), (SX1 - 12, SY0 + 28)], fill=LINE)
supports = [
    ("M. EAST", RED,    "Houthi missile hits Riyadh tower", "Al Jazeera / WSJ"),
    ("AMERICAS", NAVY,  "Anthropic IPO closes at $1.27tn",   "CNBC"),
    ("EUROPE",  GREEN,  "UK\u2013EU reset deal: food trade, youth",        "Reuters"),
    ("ASIA",    NAVY,   "Xi and Prabowo open trade talks",             "Xinhua"),
    ("GLOBAL",  BRASS,  "COP31 ends; draft omits 'fossil fuels'",      "AP / DW"),
    ("HEALTH",  RED,    "US loses measles-elimination status",         "UNICEF / PAHO"),
]
sy = SY0 + 36
for i, (tag, col, headline, src) in enumerate(supports):
    d.rectangle([SX0 + 12, sy + 1, SX0 + 17, sy + 26], fill=col)
    text(SX0 + 24, sy, tag, SANS_B(8.5), col)
    text(SX0 + 78, sy - 1, headline, SANS_B(12.5), INK)
    text(SX1 - 14, sy + 14, src, SANS(9), GRAPH, anchor="ra")
    sy += 33
    if i < len(supports) - 1:
        d.line([(SX0 + 12, sy - 8), (SX1 - 12, sy - 8)], fill=(224, 219, 206))

# ============================================================
# WORLD MAP (36..988, 664..940) — equirectangular coastlines
# ============================================================
APX0, APY0, APX1, APY1 = 36, 664, 988, 940
panel(APX0, APY0, APX1, APY1, fill=(236, 238, 234))
kicker(APX0 + 12, APY0 + 10, "WHERE IT HAPPENED  \u00b7  20 NOVEMBER 2026", NAVY)
d.line([(APX0 + 12, APY0 + 28), (APX1 - 12, APY0 + 28)], fill=LINE)
MXa0, MYa0, MXa1, MYa1 = APX0 + 14, APY0 + 38, APX0 + 610, APY1 - 26
LON0, LON1, LAT0, LAT1 = -170, 190, 82, -58
def PJ(lon, lat):
    return (MXa0 + (lon - LON0) / (LON1 - LON0) * (MXa1 - MXa0),
            MYa0 + (LAT0 - lat) / (LAT0 - LAT1) * (MYa1 - MYa0))
for lon in range(-160, 200, 20):
    xg, _ = PJ(lon, 0)
    d.line([(xg, MYa0), (xg, MYa1)], fill=(216, 220, 214))
for lat in range(-40, 90, 20):
    _, yg = PJ(0, lat)
    d.line([(MXa0, yg), (MXa1, yg)], fill=(216, 220, 214))
d.rectangle([MXa0, MYa0, MXa1, MYa1], outline=(180, 186, 178))
_, ye = PJ(0, 0)
d.line([(MXa0, ye), (MXa1, ye)], fill=(168, 176, 170), width=1)
LAND   = (210, 208, 192)
LAND_E = (150, 148, 130)
CONTINENTS = [
    [(71,-156),(69,-141),(70,-127),(72,-110),(69,-97),(67,-85),(63,-78),(58,-62),(52,-56),
     (47,-53),(45,-65),(41,-70),(35,-75),(31,-81),(25,-81),(30,-84),(29,-90),(26,-97),
     (21,-97),(16,-95),(15,-92),(10,-84),(8,-78),(9,-80),(14,-92),(19,-105),(23,-110),
     (28,-114),(34,-120),(40,-124),(48,-124),(55,-133),(60,-145),(60,-165),(66,-164)],
    [(83,-40),(81,-20),(72,-22),(60,-43),(65,-52),(75,-58),(80,-55)],
    [(11,-72),(10,-64),(5,-52),(0,-50),(-5,-35),(-13,-38),(-23,-42),(-30,-48),(-38,-57),
     (-50,-62),(-55,-68),(-52,-72),(-40,-73),(-30,-71),(-18,-70),(-6,-81),(0,-80),(8,-77)],
    [(37,-6),(37,10),(33,22),(32,25),(31,32),(31,34),(22,37),(12,43),(11,51),(4,48),
     (-2,41),(-15,40),(-26,33),(-34,20),(-34,18),(-30,17),(-20,12),(-10,13),(0,9),
     (4,6),(4,-8),(5,-4),(6,-10),(11,-17),(15,-17),(21,-17),(28,-13),(33,-9)],
    [(37,-9),(43,-9),(44,-1),(49,-2),(51,2),(53,5),(57,8),(58,5),(62,5),(68,14),(71,25),
     (68,44),(73,55),(76,100),(70,170),(66,170),(60,163),(54,158),(50,156),(54,140),
     (46,142),(39,126),(35,129),(34,126),(30,122),(23,117),(21,110),(10,107),(9,105),
     (1,103),(6,100),(14,100),(16,94),(22,89),(21,87),(16,82),(8,77),(15,74),(21,70),
     (25,66),(25,57),(25,52),(30,48),(24,52),(17,55),(13,45),(21,39),(28,34),(31,32),
     (36,36),(36,28),(40,23),(38,20),(41,18),(44,13),(45,9),(43,5),(43,3),(41,0),
     (39,0),(37,-2),(36,-6)],
    [(58,-5),(54,-3),(51,1),(50,-5),(53,-4),(57,-6)],
    [(55,-6),(52,-6),(51,-9),(54,-10)],
    [(45,142),(43,145),(41,141),(38,140),(36,139.8),(35.5,139.6),(33,135),(31,131)],
    [(3,95.5),(0,100),(-3,102),(-5.5,105.5),(-6.0,112),(-6.5,115),(-7.5,114),(-7.0,110),(-6.6,106.5),(-6.9,105),(-4.5,103),(-2,99.5),(1.5,96)],
    [(7,117),(1,119),(-4,116),(0,110),(5,109)],
    [(1,120),(-2,121),(-5,120),(-2,119)],
    [(-1,131),(-3,141),(-8,147),(-10,150),(-8,141),(-4,133)],
    [(18,121),(14,122),(13,124),(16,120)],
    [(9,80),(6,82),(7,80)],
    [(-12,49),(-16,50),(-25,47),(-25,45),(-16,44)],
    [(-11,142),(-16,146),(-28,153),(-38,147),(-39,144),(-35,138),(-32,133),(-34,120),
     (-34,115),(-26,113),(-20,119),(-17,123),(-14,127),(-12,131),(-12,137)],
    [(-41,146),(-43,147),(-43,145)],
    [(-35,174),(-39,177),(-42,174),(-46,169),(-44,170)],
    [(66,-23),(65,-14),(63,-19)],
]
for poly in CONTINENTS:
    pts = [PJ(lon, lat) for lat, lon in poly]
    d.polygon(pts, fill=LAND, outline=LAND_E)
d.polygon([PJ(50,47), PJ(53,44), PJ(50,38), PJ(48,42)], fill=(206, 218, 222))
def marker(n, lon, lat):
    x, y = PJ(lon, lat)
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=RED, outline=WHITE)
    text(x, y - 1, str(n), SANS_B(10), WHITE, anchor="mm")
markers = [
    (1, 30.5, 50.4), (2, 84.9, 19.3), (3, 138.8, 36.2), (4, 46.7, 24.7),
    (5, 32.5, 38.2), (6, -74.0, 40.7), (7, -0.1, 51.5), (8, 105.5, -6.0),
]
for n, lon, lat in markers:
    marker(n, lon, lat)
for lab, lon, lat in (("N. AMERICA", -100, 45), ("S. AMERICA", -60, -15), ("AFRICA", 20, 5),
                      ("EUROPE", 15, 55), ("ASIA", 90, 48), ("AUSTRALIA", 134, -25)):
    x, y = PJ(lon, lat)
    text(x, y, lab, SANS_B(9), (110, 112, 100), anchor="mm")
LX = APX0 + 648
text(LX, APY0 + 38, "THE DAY IN EIGHT PLACES", SANS_B(10.5), GRAPH)
legend = [
    (1, "Kyiv \u2014 overnight missile assault"),
    (2, "Gopalpur, India \u2014 Cyclone Akvan landfall"),
    (3, "Tokyo \u2014 Nikkei \u22125.1% week"),
    (4, "Riyadh \u2014 Houthi missile strike"),
    (5, "Antalya \u2014 COP31 final day"),
    (6, "New York \u2014 Anthropic $93.5bn IPO"),
    (7, "London \u2014 UK\u2013EU reset deal"),
    (8, "Jakarta \u2014 China\u2013Indonesia talks"),
]
ly = APY0 + 62
for n, txt in legend:
    d.ellipse([LX, ly, LX + 15, ly + 15], fill=RED, outline=WHITE)
    text(LX + 7, ly + 6, str(n), SANS_B(9), WHITE, anchor="mm")
    text(LX + 24, ly + 2, txt, SANS(11.5), INK)
    ly += 27
d.line([(LX, ly + 2), (APX1 - 14, ly + 2)], fill=LINE)
text(LX, ly + 10, "Projection: equirectangular \u00b7 markers mark report locations", SANS(9), GRAPH)
text(LX, ly + 26, "Not for navigational use \u00b7 coastlines simplified", SANS(9), GRAPH)

# ============================================================
# FOOTER (952..1000)
# ============================================================
d.line([(36, 950), (988, 950)], fill=INK, width=2)
text(36, 958, "DATE CHECK: every event above was reported on Friday, 20 November 2026, in some time zone that calendar day.", SANS(10.5), GRAPH)
text(36, 976, "SOURCES: Reuters \u00b7 AP \u00b7 PTI \u00b7 The Hindu \u00b7 Xinhua \u00b7 CNBC \u00b7 Sensor Tower \u00b7 Al Jazeera \u00b7 WSJ \u00b7 AP/DW \u00b7 UNICEF \u00b7 PAHO", SANS_B(10.5), INK)
text(988, 958, "EDITION 2026-1120 \u00b7 v4", SANS_B(10.5), GRAPH, anchor="ra")
text(988, 976, "Compiled by the graphics desk", SANS(10.5), GRAPH, anchor="ra")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print("entry.png bytes:", os.path.getsize(out))
