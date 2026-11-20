"""Deterministic world-news poster, 20 Nov 2026, 1024x1024, dark navy."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
NAVY = (13, 22, 42)
NAVY2 = (22, 34, 62)
GOLD = (212, 175, 55)
WHITE = (236, 240, 248)
GREY = (150, 160, 180)
RED = (214, 69, 65)
BLUE = (90, 140, 220)
GREEN = (80, 180, 120)

B = "DejaVuSans-Bold.ttf"
R = "DejaVuSans.ttf"
import os
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=True):
    return ImageFont.truetype(os.path.join(FONT_DIR, B if bold else R), size)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# subtle vertical gradient
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(13 + 10 * t), int(22 + 12 * t), int(42 + 18 * t)))

# ---------- header ----------
d.rectangle([0, 0, W, 118], fill=NAVY2)
d.rectangle([0, 118, W, 122], fill=GOLD)

# globe icon (vector-ish simple)
cx, cy, r = 62, 60, 34
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=GOLD, width=2)
d.line([(cx - r, cy), (cx + r, cy)], fill=GOLD, width=2)
d.line([(cx - r * 0.85, cy - 16), (cx + r * 0.85, cy - 16)], fill=GOLD, width=2)
d.line([(cx - r * 0.85, cy + 16), (cx + r * 0.85, cy + 16)], fill=GOLD, width=2)

d.text((110, 26), "DUNIA HARI INI", font=F(40), fill=GOLD)
d.text((110, 74), "Jumat, 20 November 2026  -  Ringkasan Berita Global", font=F(20, False), fill=GREY)
d.text((W - 20, 40), "No. 2026-1130", font=F(18, False), fill=GREY, anchor="ra")

# ---------- 3-column layout ----------
# headline cards zone: y 140..600 ; briefs zone y 620..940 ; footer 940..1024
M = 24
GUT = 16
COLW = (W - 2 * M - 2 * GUT) // 3  # 314

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def draw_lines(x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def card(x, y, w_, h_, tag, tagcolor, title, body, nbadge=None):
    d.rounded_rectangle([x, y, x + w_, y + h_], 10, fill=NAVY2, outline=(45, 62, 100), width=1)
    d.rectangle([x, y, x + 4, y + h_], fill=tagcolor)
    yy = y + 12
    if nbadge:
        d.ellipse([x + 14, yy, x + 40, yy + 26], fill=tagcolor)
        d.text((x + 27, yy + 13), str(nbadge), font=F(16), fill=(10, 16, 30), anchor="mm")
        d.text((x + 50, yy + 3), tag.upper(), font=F(15), fill=tagcolor)
        yy += 32
    else:
        d.text((x + 14, yy), tag.upper(), font=F(15), fill=tagcolor)
        yy += 24
    yy = draw_lines(x + 14, yy + 2, wrap(title, F(20), w_ - 28), F(20), WHITE, 25)
    yy = draw_lines(x + 14, yy + 6, wrap(body, F(15, False), w_ - 28), F(15, False), GREY, 20)
    return yy

cards = [
    (1, "DIPLOMASI", RED,
     "Trump-Xi-Putin: KTT Trilateral Shenzhen",
     "Ketiga pemimpin menandatangani 'Declaration toward Peace'. Dialog risiko nuklir dibuka, tapi tidak ada gencatan senjata Ukraina."),
    (2, "KEADILAN", GOLD,
     "ICJ: Myanmar melakukan genosida Rohingya (9-6)",
     "Mahkamah Internasional pertama kali memutus sebuah negara melakukan genosida. Vonis historis dengan mayoritas 9 banding 6."),
    (3, "TEKNOLOGI", GREEN,
     "IPO Anthropic rekor $107 miliar",
     "Saham melesat +17% di hari pertama, kapitalisasi sempat mendekati $2 triliun - IPO terbesar dalam sejarah."),
    (4, "ENTERTAINMENT", BLUE,
     "GTA VI rilis, Metacritic 99/100",
     "Permainan paling ditunggu dekade ini akhirnya keluar dan langsung jadi salah satu skor tertinggi sepanjang masa."),
]

# top row: card 1 full width left-right split? -> row1: card1 (2/3) + card2 (1/3); row2: card3 + card4 side by side
def h_needed(c, w_):
    n, tag, col, t, body = c
    lh_t = len(wrap(t, F(20), w_ - 28)) * 25
    lh_b = len(wrap(body, F(15, False), w_ - 28)) * 20
    return 12 + 32 + 2 + lh_t + 6 + lh_b + 14

y0 = 140
row1_y = y0
w12 = (W - 2 * M - GUT) // 2
rh1 = max(h_needed(cards[0], w12), h_needed(cards[1], w12))

def put(c, x, y, w_, h_):
    card(x, y, w_, h_, c[1], c[2], c[3], c[4], nbadge=c[0])

put(cards[0], M, row1_y, w12, rh1)
put(cards[1], M + w12 + GUT, row1_y, w12, rh1)

row2_y = row1_y + rh1 + GUT
rh2 = max(h_needed(cards[2], w12), h_needed(cards[3], w12))
put(cards[2], M, row2_y, w12, rh2)
put(cards[3], M + w12 + GUT, row2_y, w12, rh2)

# ---------- briefs: 3 columns ----------
by = row2_y + rh2 + GUT
d.text((M, by + 6), "BRIEFS", font=F(22), fill=GOLD)
d.line([(M + 90, by + 18), (W - M, by + 18)], fill=(45, 62, 100), width=1)
by += 36

briefs = [
    ("CRIMEA", RED,
     "Jembatan Crimea diserang lagi. Lalu lintas dihentikan sementara, dua pilar rusak."),
    ("TURKI", GOLD,
     "Drone tempur Kizilelma resmi masuk dinas Angkatan Udara Turki - drone jet tempur pertama di kelasnya."),
    ("EKONOMI", GREEN,
     "IMF: utang global mendekati 100% GDP, level tertinggi sejak era pasca-perang."),
    ("CUACA", BLUE,
     "Cyclone Akvan menerjang pantai timur India; ratusan ribu warga dievakuasi."),
]
bh = 96
for i, (tag, col, txt) in enumerate(briefs):
    cx_ = M + (i % 2) * (w12 + GUT)
    cy_ = by + (i // 2) * (bh + GUT)
    d.rounded_rectangle([cx_, cy_, cx_ + w12, cy_ + bh], 8, fill=NAVY2, outline=(45, 62, 100))
    d.rectangle([cx_, cy_, cx_ + 4, cy_ + bh], fill=col)
    d.text((cx_ + 14, cy_ + 8), tag, font=F(14), fill=col)
    draw_lines(cx_ + 14, cy_ + 30, wrap(txt, F(15, False), w12 - 28), F(15, False), WHITE, 19)

# ---------- footer ----------
fy = H - 84
d.rectangle([0, fy, W, H], fill=NAVY2)
d.rectangle([0, fy, W, fy + 3], fill=GOLD)
# small icon row: flag-ish triangles + sun + waves
ix = M
# wave
for k in range(3):
    d.arc([ix + k * 16, fy + 34, ix + 16 + k * 16, fy + 50], 200, 340, fill=BLUE, width=3)
ix += 60
# bolt (energy)
d.polygon([(ix, fy + 20), (ix + 12, fy + 20), (ix + 6, fy + 34), (ix + 14, fy + 34), (ix - 2, fy + 56), (ix + 4, fy + 38), (ix - 4, fy + 38)], fill=GOLD)
ix += 34
# scales (justice): triangle + lines
d.polygon([(ix + 12, fy + 18), (ix, fy + 40), (ix + 24, fy + 40)], outline=GOLD, width=2)
d.line([(ix + 12, fy + 40), (ix + 12, fy + 52)], fill=GOLD, width=2)
d.line([(ix, fy + 52), (ix + 24, fy + 52)], fill=GOLD, width=2)
ix += 40
# rocket triangle
d.polygon([(ix, fy + 52), (ix + 12, fy + 18), (ix + 24, fy + 52)], fill=RED)

d.text((W - M, fy + 26), "Disusun otomatis oleh My AI Companion  -  sumber: laporan wire global", font=F(15, False), fill=GREY, anchor="ra")
d.text((M, fy + 52), "WORLD NEWS BULLETIN - 20/11/2026", font=F(16), fill=GOLD)

img.save("entry.png")
print("saved entry.png", img.size)
