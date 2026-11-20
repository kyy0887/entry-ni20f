"""v2 broadsheet world-news poster, 20 Nov 2026, 1024x1024, deterministic (Pillow)."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
NAVY = (13, 22, 42)
NAVY2 = (22, 34, 62)
GOLD = (212, 175, 55)
WHITE = (236, 240, 248)
GREY = (150, 160, 180)
RED = (214, 69, 65)
BLUE = (90, 140, 220)
GREEN = (80, 180, 120)
ORANGE = (235, 150, 60)
CYAN = (90, 190, 200)
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def F(size, bold=True):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(13 + 8 * t), int(22 + 10 * t), int(42 + 14 * t)))

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

# ---------------- data ----------------
DATA = {
    "EUROPE": [
        ("Russian overnight assault: 80 cruise + 20 ballistic missiles, 3 bridges hit in Kyiv, 9 dead; 82 missiles and 380 drones downed", "Reuters/AP"),
        ("UK and EU set to agree 'reset' easing food trade and youth mobility; divisions persist", "Reuters"),
        ("US envoys floated NATO membership for Ukraine in exchange for ceded territory", "WSJ"),
        ("Merz: new Ukraine talks including Europe 'soon'; urges Kyiv reforms for investment", "DW"),
        ("Russian military transport aircraft crashed in Siberia, 19 dead", "CNN"),
        ("Sanchez and Feijoo clash in TV debate before 29 Nov Spain election; Sanchez admits 'mistakes'", "POLITICO"),
    ],
    "ASIA": [
        ("Cyclone Akvan landfall near Gopalpur, Odisha: 70-90 kmph winds, 300,000+ evacuated, 47 trains cancelled", "PTI/The Hindu"),
        ("Taiwan stocks -6.2%, worst week since 1991; KOSPI -5.2%", "24/7 Wall St."),
        ("Xi and Prabowo launch China-Indonesia economic partnership talks, South China Sea cooperation", "Xinhua"),
        ("Taiwan tracks 9 Chinese ships, 8 aircraft and 4 balloons; deploys missile systems", "Taiwan News"),
        ("Modi inaugurates first SCO Civilisational Dialogue Forum in New Delhi", "DD India"),
        ("Pakistan beat Sri Lanka by 8 wickets at Rawalpindi, 2-0 series, first WTC win", "ESPNcricinfo"),
    ],
    "MIDDLE EAST": [
        ("Trump pushes decision on renewed Iran strikes into 2027: 'we've got time'; Tehran denies chemical weapons claim", "CBS/J.Post"),
        ("Houthi missile damaged Riyadh's tallest skyscraper, HQ of Saudi PIF", "Al Jazeera/WSJ"),
        ("Third tanker hit a naval mine in the eastern Strait of Hormuz", "IRNA"),
        ("Oil rose Friday on supply fears but set for third straight weekly decline", "Reuters"),
        ("Gaza: 22,000+ children killed since October 2023, per Palestinian Foreign Ministry", "Anadolu"),
        ("Israeli incursion in central Gaza displaces more families as winter nears", "Gaza Herald"),
    ],
    "AMERICAS": [
        ("Democrats nominate Hakeem Jeffries for Speaker; progressives dissent on healthcare, Gaza, ICE", "Democracy Now"),
        ("Anthropic closed first trading day at $97.17, $1.27T valuation; IPO raised $93.5B", "CNBC"),
        ("US spot bitcoin ETFs saw $582M daily net outflow; November total nears $3.5B", "The Block"),
        ("DHS Secretary Mullin questioned over deaths of immigrants in ICE custody", "Democracy Now"),
    ],
    "AFRICA": [
        ("COP31 Africa Group demands grants not loans; climate funding gap put at $190 billion", "DW/Nation"),
        ("AU urges African nations to boost domestic health budgets and medicine production", "Channel Africa"),
        ("COP31 finance talks drag into final day in Antalya", "Reuters"),
    ],
    "OCEANIA": [
        ("Australia's ASX 200 fell 1.6% to 8,592.60 in the AI-led selloff", "AP"),
        ("Adelaide Strikers beat Melbourne Renegades by five wickets in final-over WBBL finish", "cricket.com.au"),
    ],
    "GLOBAL": [
        ("Nikkei 225 -5.1% to 56,436.65; Asian shares headed for worst week since 2020 as AI rout deepened", "Reuters"),
        ("GTA VI took $2.36bn in under 24 hours, 24.5M copies, 75% on PlayStation", "Sensor Tower/The Verge"),
        ("COP31 final day: draft omits 'fossil fuels', deadlock persists; 'worst COP ever' warning", "AP/Euronews"),
        ("UNICEF: measles spreading where disease was under control; US lost elimination status", "UNICEF/PAHO"),
        ("NIH-backed study of 1M+ people identifies endometriosis pathways", "NIH"),
        ("Galectin-3 in brain immune cells may accelerate Alzheimer's damage", "Lund Univ."),
        ("Google gives Gemini computer-use on Mac to paid subscribers", "TechCrunch"),
        ("OpenAI models cut AMD GPU design time, up to 14% PPA gain", "OpenAI/AMD"),
    ],
}
REGION_COLOR = {
    "EUROPE": BLUE, "ASIA": RED, "MIDDLE EAST": ORANGE, "AMERICAS": GREEN,
    "AFRICA": CYAN, "OCEANIA": GOLD, "GLOBAL": (200, 170, 230),
}
TOTAL_ITEMS = sum(len(v) for v in DATA.values())

# ---------------- header (y 0..96) ----------------
d.rectangle([0, 0, W, 96], fill=NAVY2)
d.text((30, 14), "THE WORLD IN ONE DAY", font=F(38), fill=WHITE)
d.text((31, 15), "THE WORLD IN ONE DAY", font=F(38), fill=GOLD)
d.text((32, 62), "Friday, 20 November 2026 (UTC)", font=F(15, False), fill=GREY)
# edition badge
bb = d.textlength("2026-1120", font=F(16))
d.rounded_rectangle([W - 30 - bb - 20, 26, W - 30, 58], 8, outline=GOLD, width=2)
d.text((W - 40, 42), "2026-1120", font=F(16), fill=GOLD, anchor="rm")
d.rectangle([0, 96, W, 98], fill=GOLD)

# ---------------- fact band (y 98..140) ----------------
facts = [("3 bridges struck in Kyiv", RED), ("300,000+ evacuated in Odisha", ORANGE),
         ("Nikkei -5.1%", BLUE), ("$2.36bn GTA VI in 24h", GREEN)]
f_fact = F(12)
fx = 24
fw = (W - 48) / 4
for i, (txt, col) in enumerate(facts):
    d.rectangle([fx, 106, fx + 4, 132], fill=col)
    d.text((fx + 12, 119), txt, font=f_fact, fill=WHITE, anchor="lm")
    fx += fw
d.rectangle([0, 140, W, 142], fill=(45, 62, 100))

# ---------------- dot-matrix world map (y 142..300) ----------------
MASK = [
"                                                                                                ",
"           ##      ##                                                        ##      ######    ",
"          ######    ##                                                      ###### ########    ",
"         ########   #            #      ##          ###          #          ##################  ",
"         ##########            ######  #### ##    #######  ##    #         #################### ",
"          ########       #    ########  ####### ############   ##          #################### ",
"      #########          ##  ##########  ######## ########## ###          ##################    ",
"      #############       ##############################  ######           ################     ",
"       ###############    ###############################   ######          ######  ####        ",
"        ##############  #################################################  #####  ####          ",
"        ############# ################  ############ #####################  ###### ###          ",
"         ##########  ############### ####  ######## ## ###################  ##########          ",
"          ########   ###############  ####  ######## ### ################  #########            ",
"           ######    ##############    ##    ######  ######## ##########    #######             ",
"            ###      ########## ##            ####  ####### ## ########      ###  ##            ",
"            # #      ###########               ##   ########    ######       ##                 ",
"             #        ##########              #    #########     ####        #                  ",
"             ##        ########              ##    ########      ##                             ",
"              #         ###### ##           ##     ###### #                                     ",
"                        ######  ##         #      ######   #                                    ",
"                        ######   #          #     ######                                        ",
"                        ######              #     #####                                         ",
"                         ####                    ## #                                           ",
"                         ###                    ####                                            ",
"                         ##                    #####                                           ",
"                          #                    ####                                             ",
"                        ##                      #   ##                                         ",
"                        #                           #                                           ",
"                                                                                                ",
]
# map panel
d.rounded_rectangle([8, 146, W - 8, 296], 10, fill=(16, 26, 50), outline=(45, 62, 100), width=1)
mx0, my0 = 30, 156
cols, rows = len(MASK[0]), len(MASK)
cw = (W - 60) / cols
ch = 130 / rows
dot_r = max(1.0, min(cw, ch) * 0.28)
for r_, row in enumerate(MASK):
    for c_, ch_ in enumerate(row):
        if ch_ == "#":
            x = mx0 + c_ * cw
            y = my0 + r_ * ch
            d.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=(70, 100, 160))
# markers: (col, row, label, color) approximate positions within mask grid
MARKERS = [
    (46, 3, "Kyiv", RED, 1), (36, 10, "Odisha", ORANGE, 1), (47, 9, "Riyadh", GOLD, -1),
    (76, 5, "Shenzhen", CYAN, -1), (43, 5, "Antalya", BLUE, -1), (20, 5, "Silicon Valley", GREEN, 1),
    (28, 16, "Brasilia", (200, 170, 230), -1), (25, 12, "Lagos", WHITE, 1),
]
for c_, r_, label, col, side in MARKERS:
    x = mx0 + c_ * cw
    y = my0 + r_ * ch
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=col)
    lw = d.textlength(label, font=F(11))
    lx = x + 8 if side > 0 else x - 8 - lw
    if lx < 14:
        lx = 14
    if lx + lw > W - 14:
        lx = W - 14 - lw
    d.text((lx, y - 1), label, font=F(11), fill=col, anchor="lm")

# ---------------- body: 7 region columns (y 300..930) ----------------
TOP, BOT = 300, 930
MG = 12
GUT = 10
COLW = (W - 2 * MG - 6 * GUT) / 7
TITLE_SIZE = 12
SRC_SIZE = 9

def render_columns(size, src_size, lh_mult=1.12, draw=False):
    """Measure (or draw) all columns; return True if everything fits."""
    f_title = F(size)
    f_src = F(src_size, False)
    f_head = F(14)
    ok = True
    for i, (region, items) in enumerate(DATA.items()):
        x = MG + i * (COLW + GUT)
        w_ = COLW
        tw = w_ - 8
        col = REGION_COLOR[region]
        y = TOP
        if draw:
            d.rectangle([x, y, x + w_, y + 24], fill=NAVY2)
            d.rectangle([x, y, x + w_, y + 3], fill=col)
            d.text((x + w_ / 2, y + 14), region, font=f_head, fill=WHITE, anchor="mm")
        y += 32
        for title, src in items:
            lines = wrap(title, f_title, tw)
            ih = len(lines) * int(size * lh_mult) + 4 + src_size + 10
            if y + ih > BOT:
                ok = False
                break
            if draw:
                yy = y + 6
                d.rectangle([x + 1, yy + 3, x + 5, yy + 3 + size], fill=col)
                for ln in lines:
                    d.text((x + 10, yy), ln, font=f_title, fill=WHITE)
                    yy += int(size * lh_mult)
                yy += 3
                d.text((x + 10, yy), "- " + src, font=f_src, fill=GREY)
                yy += src_size + 4
            y = y + ih + 8
        if not ok:
            break
    return ok

# measure first (no drawing), then draw only with the chosen size
size = 12
while size >= 9:
    if render_columns(size, 9):
        break
    size -= 1
render_columns(size, 9, draw=True)

# column separators
for i in range(1, 7):
    x = MG + i * COLW + (i - 1) * GUT + GUT / 2
    d.line([(x, TOP + 28), (x, BOT)], fill=(35, 50, 85), width=1)

# ---------------- footer (y 930..1024) ----------------
d.rectangle([0, 930, W, 932], fill=GOLD)
d.text((W / 2, 944), "Sources: Reuters - AP - AFP - BBC - Al Jazeera - WSJ - Bloomberg - Xinhua - Euronews - DW - The Hindu - CNN - CNBC - UNICEF - NIH",
       font=F(11, False), fill=GREY, anchor="ma")
d.text((W / 2, 966), "Compiled 20 Nov 2026 - all items dated 20 November 2026 (UTC)",
       font=F(10, False), fill=(110, 125, 150), anchor="ma")
d.text((W / 2, 986), f"EDITION 2026-1120  |  {TOTAL_ITEMS} sourced items across 7 regions",
       font=F(13), fill=GOLD, anchor="ma")

out = "/home/agentuser/makefun/entry-ni20f/entry.png"
img.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(out, optimize=True)
import json
print(json.dumps({"items": TOTAL_ITEMS, "size": os.path.getsize(out)}))
