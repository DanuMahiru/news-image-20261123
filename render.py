#!/usr/bin/env python3
"""The Monday Globe v2 — draws entry.png, a one-page newspaper front that
sums up the world news of Monday 23 November 2026.

Written fresh for v2 (new layout, new illustration style). Deterministic:
no network, no clock, no randomness. Pillow only.
Run: python3 render.py  ->  writes entry.png (1024x1024) next to this file.

v2 layout (a substantial redesign of v1's 2x2 grid):
  red rule + centred serif masthead + red date band ("SECOND EDITION")
  -> dark navy 6-cell numbers strip -> segmented region bar
  -> FOUR LEADS IN ONE ROW, poster-style art panels on top, text below
  -> "MORE FROM MONDAY": 10 secondaries in two columns of five, each
     with a tinted icon tile and a numbered circle
  -> bottom split, sides SWAPPED vs v1: "ALSO ON MONDAY" list on the
     LEFT, "WHERE IT HAPPENED" dotted map on the RIGHT (15 pins now)
  -> DATE CHECK box -> HOW WE CHECKED footer legend.
Every story carries a verification badge (CONFIRMED / OFFICIAL /
REPORTED / CLAIM); region counts are computed from the story tags.
"""
import math
import os
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (22, 20, 18)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (13, 110, 100)
OCHRE = (176, 120, 24)
BLUE = (36, 84, 130)
GOLD = (212, 168, 60)
GREY = (105, 100, 88)
PANEL = (255, 253, 247)
DOT = (148, 143, 126)
TINT = {
    "blue": (214, 228, 240),
    "red": (244, 214, 210),
    "teal": (205, 232, 226),
    "ochre": (245, 228, 196),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BADGE_FILL = {
    "CONFIRMED": TEAL,
    "OFFICIAL": BLUE,
    "REPORTED": OCHRE,
    "CLAIM": RED,
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ stories
# region: EUROPE / MIDEAST / AFRICA / ASIA / AMERICAS / WORLD
# badge:  CONFIRMED = two independent reports or official market data
#         OFFICIAL  = a named official source
#         REPORTED  = one reputable report
#         CLAIM     = one side's claim, not independently verified
# v2 changes vs v1: lead 1 and 3 bodies tightened with new Monday detail
# (EU fossil-fuel rejection; Trump intervened, $954bn added); ALSO 22
# upgraded REPORTED -> CONFIRMED (AP + CBS), 23 sourced to Reuters,
# 25 replaced (Saudi/Khartoum, weak source) with the Belgium strike,
# 29 replaced (US drills in Japan, weak source) with the Megaspeed
# blacklist. Region counts move: EUROPE 17, MIDEAST 3, AFRICA 3,
# ASIA 4, AMERICAS 3, WORLD 5 = 35.
LEADS = [
    dict(n=1, tag="CLIMATE", region="WORLD", badge="CONFIRMED",
         title="COP31 AFTERMATH",
         body="The blame game starts a day after the talks collapse \u2014 "
              "the first COP failure since 2009. The EU rejected a text "
              "with no fossil-fuel language; Pacific islands say they "
              "were \u201clet down on all sides\u201d.",
         src="Reuters", kind="globe", tint="blue", deep=NAVY),
    dict(n=2, tag="LIBYA", region="AFRICA", badge="CLAIM",
         title="UKRAINE SINKS THE MERKURY",
         body="Zelenskyy says seven Ukrainian naval drones sank the "
              "Russian corvette at Benghazi and hit the cargo ship "
              "Angara. A Ka-27 helicopter aboard was also destroyed.",
         src="AP / SBU", kind="ship", tint="red", deep=RED),
    dict(n=3, tag="MARKETS", region="AMERICAS", badge="CONFIRMED",
         title="HUANG IS BACK",
         body="Nvidia\u2019s board votes unanimously to bring back "
              "co-founder Jensen Huang, 11 days after he quit \u2014 "
              "after Trump intervened. Shares close up 31.5% \u2014 their "
              "best day since 2003 \u2014 adding $954bn.",
         src="Reuters / AP / CNN", kind="chip", tint="teal", deep=TEAL),
    dict(n=4, tag="INDONESIA", region="ASIA", badge="OFFICIAL",
         title="INDONESIA FIRE: 24 DEAD",
         body="Indonesia confirms 24 dead in the Cikande candy-factory "
              "fire; about 30 workers are still missing. Rescuers "
              "search unstable wreckage; DNA tests will identify victims.",
         src="Reuters", kind="flame", tint="ochre", deep=OCHRE),
]

SECONDARIES = [
    dict(n=5, tag="UKRAINE", region="EUROPE", badge="OFFICIAL",
         title="Dymer toll rises to 11",
         body="Toll hits 11, incl. an 11-year-old girl. A boy, 7, was "
              "pulled alive after 14 hours under the rubble.",
         src="Reuters", kind="blast"),
    dict(n=6, tag="IRAN", region="MIDEAST", badge="OFFICIAL",
         title="Iran vows \u201call available means\u201d",
         body="Tehran will use \u201call available means\u201d against "
              "the US blockade, its foreign ministry says.",
         src="ABC / Al Jazeera", kind="sea"),
    dict(n=7, tag="EU", region="EUROPE", badge="OFFICIAL",
         title="EU unveils 22nd sanctions",
         body="Von der Leyen: ~60 banks cut from SWIFT, 70+ shadow-fleet "
              "ships listed, crypto crackdown.",
         src="EU Commission", kind="flag"),
    dict(n=8, tag="ARMENIA", region="EUROPE", badge="OFFICIAL",
         title="Armenia drops claim",
         body="Pashinyan publishes a draft charter dropping the Karabakh "
              "claim; he vows to quit if it fails.",
         src="Reuters / AP", kind="flag"),
    dict(n=9, tag="NEPAL", region="ASIA", badge="OFFICIAL",
         title="India pledges $1.6bn to Nepal",
         body="Modi offers Nepal 240bn rupees \u2014 $377m in grants, "
              "$1.24bn in credit \u2014 after August\u2019s floods.",
         src="Al Jazeera", kind="globe"),
    dict(n=10, tag="DR CONGO", region="AFRICA", badge="OFFICIAL",
         title="Ebola toll: 11,762 cases",
         body="UN: 11,762 cases and 5,775 deaths in DR Congo; Ituri is "
              "still the epicentre of the outbreak.",
         src="UN News / WHO", kind="cross"),
    dict(n=11, tag="MARKETS", region="WORLD", badge="CONFIRMED",
         title="Bitcoin holds $61,000",
         body="Bitcoin closes at $61,327, up from Saturday\u2019s $55,130 "
              "low; Ether trades near $1,722.",
         src="Finnhub", kind="coin"),
    dict(n=12, tag="FOOTBALL", region="EUROPE", badge="CONFIRMED",
         title="Brentford 4\u20130 Everton",
         body="Lewis-Potter scores twice as Brentford rout 10-man Everton "
              "4\u20130 at the Gtech on Monday night.",
         src="TNT Sports", kind="ball"),
    dict(n=13, tag="SPACE", region="WORLD", badge="OFFICIAL",
         title="BepiColombo safe in orbit",
         body="ESA: the probe is safe in a stable Mercury orbit; its burn "
              "reached 77% of the planned change.",
         src="ESA", kind="rocket"),
    dict(n=14, tag="RUSSIA", region="EUROPE", badge="OFFICIAL",
         title="Murmansk governor detained",
         body="Governor Andrei Chibis is held over alleged embezzlement of "
              "39m roubles of budget funds.",
         src="Reuters", kind="flag"),
]

# (number, text, region, badge)
ALSO = [
    (15, "UN urges probe into Libya ship attacks", "AFRICA", "OFFICIAL"),
    (16, "Rutte: Russia\u2019s war machine at full capacity", "EUROPE", "OFFICIAL"),
    (17, "Ukraine peace talks eyed before Christmas", "EUROPE", "REPORTED"),
    (18, "Kremlin warns of Baltic escalation", "EUROPE", "REPORTED"),
    (19, "Ukraine hit 16 Iskander and S-400 launchers", "EUROPE", "CLAIM"),
    (20, "Russia launches 153 drones; Ukraine downs 134", "EUROPE", "OFFICIAL"),
    (21, "Zelenskyy asks US to free up paid-for Patriots", "EUROPE", "REPORTED"),
    (22, "Democrats win 258 House seats, most since 1992", "AMERICAS", "CONFIRMED"),
    (23, "Bangladesh will jail ex-PM Hasina if she returns", "ASIA", "REPORTED"),
    (24, "Houthi attacks kill 2, wound 8 in Taiz, Yemen", "MIDEAST", "REPORTED"),
    (25, "Belgium strike grounds flights; 404 cancelled", "EUROPE", "CONFIRMED"),
    (26, "US sanctions Iranian exchange houses, Dubai firms", "MIDEAST", "OFFICIAL"),
    (27, "Guterres calls for global AI rules within a year", "WORLD", "OFFICIAL"),
    (28, "Asian chip stocks slide: Kospi -3.3%, Nikkei -5.1%", "ASIA", "CONFIRMED"),
    (29, "US blacklists Megaspeed in Nvidia chip scandal", "AMERICAS", "CONFIRMED"),
    (30, "Oil falls 3.5% to $86.78; gold rises 4.2%", "WORLD", "CONFIRMED"),
    (31, "Euro Stoxx 50 gains 2.2%; dollar index up 0.65%", "EUROPE", "CONFIRMED"),
    (32, "NATO sends early-warning planes to Poland", "EUROPE", "REPORTED"),
    (33, "Estonia readies for more strikes on Russian ships", "EUROPE", "OFFICIAL"),
    (34, "Ukraine hits Russian drone unit in Rylsk", "EUROPE", "CLAIM"),
    (35, "Novoshakhtinsk refinery hit; plant halts work", "EUROPE", "CLAIM"),
]

# (big number, label, story number it illustrates)
NUMBERS = [
    ("7", "naval drones \u00b7 \u21162", 2),
    ("31.5%", "Nvidia shares up \u00b7 \u21163", 3),
    ("24", "factory-fire dead \u00b7 \u21164", 4),
    ("11", "killed in Dymer \u00b7 \u21165", 5),
    ("5,775", "Ebola deaths \u00b7 \u211610", 10),
    ("$61,327", "Bitcoin close \u00b7 \u211611", 11),
]

REGION_ORDER = ["EUROPE", "MIDEAST", "AFRICA", "ASIA", "AMERICAS", "WORLD"]
REGION_COLS = [RED, BLUE, TEAL, OCHRE, (90, 90, 90), (120, 110, 95)]
REGION_SHORT = {"AMERICAS": "AMER"}

DATE_CHECK = ("DATE CHECK \u2014 NOT MONDAY: COP31 collapse (Sun) \u00b7 "
              "Merkury blast (Sun) \u00b7 Factory fire breaks out (Sat) \u00b7 "
              "Dymer strike (Sun) \u00b7 Sparta II hit (Sat) \u00b7 BepiColombo "
              "glitch (Sun) \u00b7 Thailand chemicals ban (Sat) \u00b7 "
              "Netanyahu\u2013Eisenkot talks (Sun) \u00b7 Poland missile ID "
              "(Sun) \u00b7 Shenzhen summit (Thu)")

LEGEND = ("HOW WE CHECKED: CONFIRMED = two independent reports \u00b7 "
          "OFFICIAL = named official source \u00b7 REPORTED = one reputable "
          "report \u00b7 CLAIM = one side\u2019s claim, unverified. "
          "Full sources: RESEARCH.md.")

# Dotted world map: land spans per row, cols 0..63, rows 0..23.
# lon -180..180 -> col, lat 90..-60 -> row. Hand-drawn, stylised.
MAP_ROWS = [
    [],
    [(8, 20), (22, 30)],
    [(4, 20), (23, 30), (40, 62)],
    [(3, 21), (24, 29), (38, 63)],
    [(2, 20), (30, 39), (40, 63)],
    [(2, 19), (30, 38), (41, 63)],
    [(3, 18), (30, 39), (41, 62)],
    [(4, 17), (30, 40), (42, 60)],
    [(5, 16), (31, 40), (43, 58)],
    [(6, 15), (32, 41), (44, 57)],
    [(7, 14), (33, 42), (45, 56)],
    [(8, 13), (34, 41), (46, 55)],
    [(9, 13), (18, 24), (35, 41), (47, 54)],
    [(18, 25), (36, 40), (48, 53)],
    [(19, 25), (37, 40), (49, 52)],
    [(20, 25), (37, 40), (50, 52)],
    [(20, 24), (38, 40), (51, 58)],
    [(21, 24), (38, 39), (52, 58)],
    [(21, 23), (39, 40), (52, 58)],
    [(22, 23), (39, 39), (53, 57)],
    [(22, 23), (54, 56)],
    [(22, 23)],
    [(22, 23)],
    [],
]

PINS = [  # (story no, lon, lat, dx, dy) — dx/dy nudge the label circle
    # off the true point (thin leader line) where pins would merge.
    # v2: pin 25 moves Khartoum -> Brussels (Belgium strike, story 25);
    # pin 29 added for Singapore (Megaspeed blacklist).
    (1, 30.7, 36.9, 0, 10), (2, 20.1, 32.1, -14, 0),
    (3, -121.95, 37.35, 0, 0), (4, 106.2, -6.1, 0, 0),
    (5, 30.3, 50.8, 0, 0), (6, 56.3, 26.5, 0, 0),
    (7, 4.35, 50.85, -20, 14), (8, 44.5, 40.2, 0, 0),
    (9, 77.2, 28.6, 0, 0), (10, 30.0, 1.5, 0, 0),
    (12, -0.13, 51.5, 0, 0), (13, 8.65, 49.87, 26, -18),
    (14, 33.07, 68.97, 0, -16), (25, 4.35, 50.85, -30, -8),
    (29, 103.85, 1.35, 10, -12),
]


# ------------------------------------------------------------- illustration
def draw_lead_art(d, kind, x, y, w, h, tint, deep):
    """Poster-style art panel: flat tint background, one big bold motif
    in the deep colour + white + a gold accent. Very different from v1's
    thin line icons: filled shapes, high contrast, motif fills the panel.
    """
    d.rectangle([x, y, x + w, y + h], fill=TINT[tint])
    cx, cy = x + w // 2, y + h // 2 + 4
    if kind == "globe":
        r = 40
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                  outline=deep, width=4)
        d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                  outline=deep, width=3)
        d.line([cx - r, cy, cx + r, cy], fill=deep, width=3)
        d.line([cx - r + 6, cy + r - 6, cx + r - 6, cy - r + 6],
               fill=RED, width=9)
    elif kind == "ship":
        d.polygon([(cx - 52, cy + 8), (cx + 52, cy + 8),
                   (cx + 38, cy + 34), (cx - 38, cy + 34)], fill=deep)
        d.rectangle([cx - 26, cy - 14, cx + 14, cy + 8], fill=deep)
        d.rectangle([cx - 4, cy - 38, cx + 4, cy - 14], fill=deep)
        d.rectangle([cx - 26, cy - 22, cx + 14, cy - 14], fill=(255, 255, 255))
        pts = []
        for i in range(12):
            r = 22 if i % 2 == 0 else 10
            a = math.radians(i * 30)
            pts.append((cx + 34 + r * math.cos(a), cy - 30 + r * math.sin(a)))
        d.polygon(pts, fill=GOLD)
        d.ellipse([cx + 26, cy - 38, cx + 42, cy - 22], fill=(255, 220, 120))
        for yy in (cy + 42, cy + 48):
            d.arc([cx - 52, yy - 8, cx - 18, yy + 8], 180, 360,
                  fill=(255, 255, 255), width=3)
            d.arc([cx - 18, yy - 8, cx + 16, yy + 8], 180, 360,
                  fill=(255, 255, 255), width=3)
    elif kind == "chip":
        d.rounded_rectangle([cx - 36, cy - 36, cx + 36, cy + 36], radius=8,
                            fill=deep)
        for px in (-36, 36):
            for py in (-18, 0, 18):
                d.rectangle([cx + px - 8, cy + py - 3,
                             cx + px + 8, cy + py + 3], fill=deep)
        f = font(SANS_B, 40)
        t = "N"
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 26), t, font=f, fill=(255, 255, 255))
        # big gold up-arrow rising off the chip's top-right corner
        d.rectangle([cx + 40, cy - 18, cx + 48, cy + 8], fill=GOLD)
        d.polygon([(cx + 32, cy - 14), (cx + 56, cy - 14), (cx + 44, cy - 34)],
                  fill=GOLD)
    elif kind == "flame":
        # asymmetric teardrop flame, leaning tip, wide base
        d.polygon([(cx - 6, cy - 46), (cx + 30, cy - 6), (cx + 32, cy + 12),
                   (cx + 20, cy + 34), (cx + 2, cy + 30),
                   (cx - 14, cy + 34), (cx - 30, cy + 2),
                   (cx - 24, cy - 20)], fill=deep)
        d.polygon([(cx + 2, cy - 16), (cx + 16, cy + 8),
                   (cx + 4, cy + 28), (cx - 12, cy + 8)], fill=(255, 220, 120))


def draw_mini(d, kind, x, y, s, tint, deep):
    """Small filled pictogram (deep colour on a tinted tile) for secondaries."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=5, fill=TINT[tint])
    cx, cy = x + s // 2, y + s // 2
    w = deep
    if kind == "globe":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                  outline=w, width=2)
        d.line([cx - r, cy, cx + r, cy], fill=w, width=2)
    elif kind == "sea":
        for yy in (-0.2, 0.15):
            yyv = cy + yy * s
            d.arc([cx - s * 0.32, yyv - s * 0.12, cx - s * 0.02, yyv + s * 0.12],
                  180, 360, fill=w, width=3)
            d.arc([cx - s * 0.02, yyv - s * 0.12, cx + s * 0.32, yyv + s * 0.12],
                  180, 360, fill=w, width=3)
        d.polygon([(cx - s * 0.28, cy - s * 0.12), (cx + s * 0.28, cy - s * 0.12),
                   (cx + s * 0.16, cy - s * 0.3), (cx - s * 0.16, cy - s * 0.3)],
                  fill=w)
    elif kind == "blast":
        pts = []
        for i in range(12):
            r = s * 0.36 if i % 2 == 0 else s * 0.17
            a = math.radians(i * 30)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=w)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
    elif kind == "flag":
        d.rectangle([cx - s * 0.3, cy - s * 0.34, cx - s * 0.24, cy + s * 0.34],
                    fill=w)
        d.polygon([(cx - s * 0.24, cy - s * 0.34), (cx + s * 0.32, cy - s * 0.22),
                   (cx + s * 0.32, cy - s * 0.08), (cx - s * 0.24, cy - s * 0.14)],
                  fill=w)
    elif kind == "cross":
        d.rectangle([cx - s * 0.09, cy - s * 0.32, cx + s * 0.09, cy + s * 0.32],
                    fill=w)
        d.rectangle([cx - s * 0.32, cy - s * 0.09, cx + s * 0.32, cy + s * 0.09],
                    fill=w)
    elif kind == "coin":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        f = font(SANS_B, 15)
        d.text((cx - 5, cy - 10), "B", font=f, fill=w)
    elif kind == "ball":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        d.polygon([(cx, cy - r * 0.45), (cx + r * 0.43, cy - r * 0.14),
                   (cx + r * 0.26, cy + r * 0.36), (cx - r * 0.26, cy + r * 0.36),
                   (cx - r * 0.43, cy - r * 0.14)], fill=w)
    elif kind == "rocket":
        d.polygon([(cx, cy - s * 0.36), (cx + s * 0.16, cy - s * 0.04),
                   (cx + s * 0.16, cy + s * 0.22), (cx, cy + s * 0.36),
                   (cx - s * 0.16, cy + s * 0.22), (cx - s * 0.16, cy - s * 0.04)],
                  fill=w)
        d.ellipse([cx - s * 0.07, cy - s * 0.2, cx + s * 0.07, cy - s * 0.05],
                  fill=PAPER)


# tile tint per secondary kind (matches the lead palette family)
KIND_TINT = {"blast": "red", "sea": "blue", "flag": "red", "globe": "blue",
             "cross": "red", "coin": "teal", "ball": "blue", "rocket": "blue"}
KIND_DEEP = {"blast": RED, "sea": BLUE, "flag": RED, "globe": NAVY,
             "cross": RED, "coin": TEAL, "ball": BLUE, "rocket": NAVY}


def num_circle(d, x, y, n, diam=30):
    """Red numbered circle."""
    d.ellipse([x, y, x + diam, y + diam], fill=RED)
    f = font(SANS_B, 16 if n < 10 else 14)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (diam - tw) / 2, y + (diam - 16) / 2 - 1), t, font=f,
           fill=(255, 255, 255))


def pill_width(d, label):
    """Width a verification pill would take, without drawing it."""
    f = font(SANS_B, 9)
    return d.textlength(label, font=f) + 14


def badge_pill(d, x, y, label, fill):
    """Small coloured verification pill; returns its width."""
    f = font(SANS_B, 9)
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 16], radius=8, fill=fill)
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def fit_check(d):
    """Fail loudly if any text would be cut — nothing is truncated."""
    # leads: title <= 2 lines, body <= 5 lines, source fits on one line
    for st in LEADS:
        assert len(wrap(d, st["title"], font(SANS_B, 15), 224)) <= 2, \
            f"lead {st['n']} title wraps"
        lines = wrap(d, st["body"], font(SANS, 10), 224)
        assert len(lines) <= 5, f"lead {st['n']} body needs {len(lines)} lines"
        assert d.textlength("Source: " + st["src"], font=font(SANS, 10)) <= 224, \
            f"lead {st['n']} source too long"
    # secondaries: title+tag fits beside the badge pill, body <= 2 lines
    for st in SECONDARIES:
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']}"
        pill_w = d.textlength(st["badge"], font=font(SANS_B, 9)) + 14
        assert d.textlength(title, font=font(SANS_B, 12)) + pill_w + 10 <= 432, \
            f"secondary {st['n']} title too long"
        suffix = " \u2014 " + st["src"]
        lines = wrap(d, st["body"], font(SANS, 11), 432)
        assert len(lines) <= 2, f"secondary {st['n']} body needs {len(lines)} lines"
        assert d.textlength(lines[-1] + suffix, font=font(SANS, 11)) <= 432, \
            f"secondary {st['n']} body+src too long"
    # ALSO list: one line each in the left bottom column
    for n, item, _r, badge in ALSO:
        line = f"{n}. {item} \u00b7 {badge}"
        w = (d.textlength(f"{n}. {item}", font=font(SANS, 10))
             + d.textlength(" \u00b7 " + badge, font=font(SANS_B, 9)))
        assert w <= 470, f"ALSO {n} too long: {line}"
    # numbers strip labels fit their cell
    for _num, lab, _n in NUMBERS:
        assert d.textlength(lab, font=font(SANS, 10)) <= 152, \
            f"numbers label too long: {lab}"
    dc = wrap(d, DATE_CHECK, font(SANS_B, 11), 960)
    assert len(dc) <= 2, f"DATE CHECK needs {len(dc)} lines"
    assert d.textlength(LEGEND, font=font(SANS, 9)) <= 984, "legend too long"
    # map pins: every pair of label circles at least 17px apart
    def proj(lon, lat):
        return (510 + (lon + 180) / 360 * 494,
                742 + (90 - lat) / 150 * 216)
    centres = []
    for _n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        centres.append((px + dx, py + dy))
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            dx = centres[i][0] - centres[j][0]
            dy = centres[i][1] - centres[j][1]
            assert dx * dx + dy * dy >= 17 * 17, \
                f"pins {PINS[i][0]} and {PINS[j][0]} too close"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 20

    # sanity: 35 stories, region counts computed from the tags
    all_stories = list(LEADS) + list(SECONDARIES) + [
        dict(n=n, region=r) for n, _t, r, _b in ALSO]
    assert len(all_stories) == 35, len(all_stories)
    counts = Counter(s["region"] for s in all_stories)
    assert sum(counts.values()) == 35
    regions = [(name, counts[name]) for name in REGION_ORDER]

    fit_check(d)

    # ---- red top rule + masthead --------------------------------------
    d.rectangle([0, 0, W, 6], fill=RED)
    title = "THE MONDAY GLOBE"
    f_title = font(SERIF, 50)
    d.text((W / 2, 14), title, font=f_title, fill=INK, anchor="ma")
    d.line([MX, 68, W - MX, 68], fill=INK, width=2)
    d.line([MX, 72, W - MX, 72], fill=INK, width=1)

    # ---- red date band -------------------------------------------------
    d.rectangle([MX, 76, W - MX, 104], fill=RED)
    d.text((MX + 12, 90), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 20),
           fill=(255, 255, 255), anchor="lm")
    d.text((W - MX - 12, 90), "SECOND EDITION \u00b7 35 STORIES",
           font=font(SANS_B, 12), fill=(255, 255, 255), anchor="rm")

    # ---- dark navy numbers strip ---------------------------------------
    d.rectangle([MX, 110, W - MX, 162], fill=NAVY)
    cell_w = (W - 2 * MX) / 6
    for i, (num, lab, _n) in enumerate(NUMBERS):
        cx = MX + cell_w * (i + 0.5)
        if i:
            d.line([MX + cell_w * i, 114, MX + cell_w * i, 158],
                   fill=(70, 90, 120), width=1)
        d.text((cx, 126), num, font=font(SANS_B, 26),
               fill=(255, 255, 255), anchor="mm")
        d.text((cx, 148), lab, font=font(SANS, 10), fill=GOLD, anchor="mm")

    # ---- region bar ------------------------------------------------------
    x = MX
    total_w = W - 2 * MX
    for (name, count), col in zip(regions, REGION_COLS):
        seg = total_w * count / 35
        d.rectangle([x, 166, x + seg, 186], fill=col)
        label = f"{REGION_SHORT.get(name, name)} {count}"
        d.text((x + seg / 2, 176), label, font=font(SANS_B, 11),
               fill=(255, 255, 255), anchor="mm")
        x += seg

    # ---- four leads in one row ------------------------------------------
    col_w, gap = 240, 8
    for i, st in enumerate(LEADS):
        x0 = MX + i * (col_w + gap)
        # poster art panel on top, text below
        draw_lead_art(d, st["kind"], x0, 192, col_w, 106,
                      st["tint"], st["deep"])
        num_circle(d, x0 - 2, 190, st["n"], diam=30)
        # tag + verification pill
        d.text((x0, 306), f"{st['tag']} \u00b7 {st['region']}",
               font=font(SANS_B, 10), fill=RED)
        pw = pill_width(d, st["badge"])
        badge_pill(d, x0 + col_w - pw, 302, st["badge"],
                   BADGE_FILL[st["badge"]])
        # title (up to 2 lines), body (up to 5), source
        y = 322
        for line in wrap(d, st["title"], font(SANS_B, 15), col_w):
            d.text((x0, y), line, font=font(SANS_B, 15), fill=INK)
            y += 19
        y = 362
        for line in wrap(d, st["body"], font(SANS, 10), col_w):
            d.text((x0, y), line, font=font(SANS, 10), fill=INK)
            y += 13
        d.text((x0, 430), "Source: " + st["src"], font=font(SANS, 10),
               fill=GREY)
        d.line([x0, 448, x0 + col_w, 448], fill=(200, 195, 180), width=1)

    # ---- secondaries header ----------------------------------------------
    d.text((MX, 456), "MORE FROM MONDAY", font=font(SANS_B, 14), fill=INK)
    d.text((W - MX, 460), "10 MORE STORIES \u00b7 \u2116 5\u201314",
           font=font(SANS, 10), fill=GREY, anchor="ra")
    d.line([MX, 474, W - MX, 474], fill=INK, width=1)

    # ---- secondaries: two columns of five --------------------------------
    for i, st in enumerate(SECONDARIES):
        col, row = divmod(i, 5)
        x0 = MX + col * 496
        y0 = 478 + row * 48
        draw_mini(d, st["kind"], x0, y0 + 4, 36,
                  KIND_TINT[st["kind"]], KIND_DEEP[st["kind"]])
        num_circle(d, x0 + 24, y0 + 26, st["n"], diam=22)
        tx = x0 + 56
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']}"
        d.text((tx, y0 + 2), title, font=font(SANS_B, 12), fill=INK)
        pw = pill_width(d, st["badge"])
        badge_pill(d, x0 + 488 - pw, y0 + 2, st["badge"],
                   BADGE_FILL[st["badge"]])
        lines = wrap(d, st["body"], font(SANS, 11), 432)
        suffix = " \u2014 " + st["src"]
        for li, line in enumerate(lines):
            yy = y0 + 19 + li * 14
            if li == len(lines) - 1:
                d.text((tx, yy), line, font=font(SANS, 11), fill=INK)
                sw = d.textlength(line, font=font(SANS, 11))
                d.text((tx + sw, yy), suffix, font=font(SANS, 11), fill=GREY)
            else:
                d.text((tx, yy), line, font=font(SANS, 11), fill=INK)

    # ---- bottom split: ALSO (left) / map (right) -------------------------
    d.text((MX, 722), "ALSO ON MONDAY", font=font(SANS_B, 14), fill=RED)
    d.text((510, 722), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=RED)
    d.text((W - MX, 726), "pins match the stories above",
           font=font(SANS, 9), fill=GREY, anchor="ra")
    d.line([MX, 740, 496, 740], fill=INK, width=1)
    d.line([510, 740, W - MX, 740], fill=INK, width=1)

    for i, (n, item, _r, badge) in enumerate(ALSO):
        y = 744 + i * 10.3
        d.text((MX, y), f"{n}. {item}", font=font(SANS, 10), fill=INK)
        tw = d.textlength(f"{n}. {item}", font=font(SANS, 10))
        d.text((MX + tw, y), " \u00b7 " + badge, font=font(SANS_B, 9),
               fill=BADGE_FILL[badge])

    # dotted world map
    map_x, map_y, map_w, map_h = 510, 744, 494, 214
    cw, ch = map_w / 64, map_h / 24
    for r, spans in enumerate(MAP_ROWS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                px = map_x + (c + 0.5) * cw
                py = map_y + (r + 0.5) * ch
                d.ellipse([px - 2.2, py - 2.2, px + 2.2, py + 2.2], fill=DOT)

    def proj(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (90 - lat) / 150 * map_h)

    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 5), t, font=f, fill=(255, 255, 255))

    # ---- DATE CHECK box ----------------------------------------------------
    d.rectangle([MX, 964, W - MX, 994], outline=RED, width=2, fill=PANEL)
    dc_lines = wrap(d, DATE_CHECK, font(SANS_B, 11), 960)
    for i, line in enumerate(dc_lines):
        d.text((MX + 12, 968 + i * 14), line, font=font(SANS_B, 11), fill=INK)

    # ---- footer legend ------------------------------------------------------
    d.text((W / 2, 1000), LEGEND, font=font(SANS, 9), fill=GREY, anchor="ma")

    img.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
