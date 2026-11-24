#!/usr/bin/env python3
"""The Monday Globe — draws entry.png, a one-page newspaper front that
sums up the world news of Monday 23 November 2026.

Deterministic: no network, no clock, no randomness. Pillow only.
Run: python3 render.py  ->  writes entry.png (1024x1024) next to this file.

Layout (the proven news-21 v2 / news-22 formula): huge date masthead,
6-cell numbers strip, region bar, 4 large illustrated leads, 10
illustrated secondaries, "WHERE IT HAPPENED" dotted map with numbered
pins, "ALSO ON MONDAY" list, DATE CHECK box. New in this edition:
every story carries a verification badge (CONFIRMED / OFFICIAL /
REPORTED / CLAIM) with a HOW WE CHECKED legend in the footer, and
the region bar counts are computed from the story tags in code.
"""
import os
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (25, 23, 19)
RED = (164, 31, 36)
BLUE = (29, 78, 122)
TEAL = (15, 118, 110)
OCHRE = (178, 122, 26)
GREY = (105, 100, 88)
PANEL = (255, 253, 247)

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
LEADS = [
    dict(n=1, tag="CLIMATE", region="WORLD", badge="CONFIRMED",
         title="COP31 AFTERMATH",
         body="The blame game starts a day after the talks collapse \u2014 "
              "the first COP failure since 2009. Pacific islands say they "
              "were \u201clet down on all sides\u201d; Australia\u2019s "
              "opposition wants the talks chief sacked.",
         src="Reuters", kind="globe", tint=BLUE),
    dict(n=2, tag="LIBYA", region="AFRICA", badge="CLAIM",
         title="UKRAINE SINKS THE MERKURY",
         body="Zelenskyy says seven Ukrainian naval drones sank the "
              "Russian corvette at Benghazi and hit the cargo ship "
              "Angara. A Ka-27 helicopter aboard was also destroyed.",
         src="AP / SBU", kind="ship", tint=RED),
    dict(n=3, tag="MARKETS", region="AMERICAS", badge="CONFIRMED",
         title="HUANG IS BACK",
         body="Nvidia\u2019s board votes unanimously to bring back "
              "co-founder Jensen Huang, 11 days after he quit. Shares "
              "close up 31.5% \u2014 their best day since 2003.",
         src="Reuters / AP / CNN", kind="coin", tint=TEAL),
    dict(n=4, tag="INDONESIA", region="ASIA", badge="OFFICIAL",
         title="INDONESIA FIRE: 24 DEAD",
         body="Indonesia confirms 24 dead in the Cikande candy-factory "
              "fire; about 30 workers are still missing. Rescuers "
              "search unstable wreckage; DNA tests will identify victims.",
         src="Reuters", kind="flame", tint=OCHRE),
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
    (22, "Democrats win 258 House seats, most since 1992", "AMERICAS", "REPORTED"),
    (23, "Bangladesh will jail ex-PM Hasina if she returns", "ASIA", "REPORTED"),
    (24, "Houthi attacks kill 2, wound 8 in Taiz, Yemen", "MIDEAST", "REPORTED"),
    (25, "Saudi Arabia condemns attack on UN site in Khartoum", "MIDEAST", "OFFICIAL"),
    (26, "US sanctions Iranian exchange houses, Dubai firms", "MIDEAST", "OFFICIAL"),
    (27, "Guterres calls for global AI rules within a year", "WORLD", "OFFICIAL"),
    (28, "Asian chip stocks slide: Kospi -3.3%, Nikkei -5.1%", "ASIA", "CONFIRMED"),
    (29, "US troops in South Korea drill live-fire in Japan", "ASIA", "REPORTED"),
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
    # off the true point (thin leader line) where pins would merge
    (1, 30.7, 36.9, 0, 8), (2, 20.1, 32.1, -12, 0),
    (3, -121.95, 37.35, 0, 0), (4, 106.2, -6.1, 0, 0),
    (5, 30.3, 50.8, 0, 0), (6, 56.3, 26.5, 0, 0),
    (7, 4.35, 50.85, -18, 16), (8, 44.5, 40.2, 0, 0),
    (9, 77.2, 28.6, 0, 0), (10, 30.0, 1.5, 0, 0),
    (12, -0.13, 51.5, 0, 0), (13, 8.65, 49.87, 20, -14),
    (14, 33.07, 68.97, 0, 0), (25, 32.5, 15.6, 12, 0),
]


def draw_icon(d, kind, cx, cy, s, ink, accent):
    """Small pictogram centred at (cx, cy), size s, drawn from shapes."""
    import math
    if kind == "globe":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=ink, width=3)
        d.ellipse([cx - s * 0.45, cy - s, cx + s * 0.45, cy + s],
                  outline=ink, width=2)
        d.line([cx - s, cy, cx + s, cy], fill=ink, width=2)
        d.line([cx - s * 0.8, cy + s * 0.8, cx + s * 0.8, cy - s * 0.8],
               fill=accent, width=4)
    elif kind == "sea":
        for yy in (-0.5, 0.0, 0.5):
            y = cy + yy * s
            d.arc([cx - s, y - s * 0.35, cx - s * 0.2, y + s * 0.35],
                  180, 360, fill=ink, width=3)
            d.arc([cx - s * 0.2, y - s * 0.35, cx + s * 0.6, y + s * 0.35],
                  180, 360, fill=ink, width=3)
        d.polygon([(cx - s * 0.9, cy - s * 0.9), (cx + s * 0.9, cy - s * 0.9),
                   (cx + s * 0.5, cy - s * 0.45), (cx - s * 0.5, cy - s * 0.45)],
                  fill=ink)
        d.rectangle([cx - s * 0.08, cy - s * 1.15, cx + s * 0.08, cy - s * 0.85],
                    fill=ink)
    elif kind == "ship":
        d.polygon([(cx - s, cy + s * 0.3), (cx + s, cy + s * 0.3),
                   (cx + s * 0.7, cy + s * 0.8), (cx - s * 0.7, cy + s * 0.8)],
                  fill=ink)
        d.rectangle([cx - s * 0.5, cy - s * 0.3, cx + s * 0.3, cy + s * 0.3],
                    fill=ink)
        d.rectangle([cx - s * 0.1, cy - s * 0.9, cx + s * 0.1, cy - s * 0.3],
                    fill=ink)
        for a in (0, 60, 120, 180, 240, 300):
            r1, r2 = s * 0.35, s * 0.75
            x1 = cx + s * 0.55 + r1 * math.cos(math.radians(a))
            y1 = cy - s * 0.75 + r1 * math.sin(math.radians(a))
            x2 = cx + s * 0.55 + r2 * math.cos(math.radians(a))
            y2 = cy - s * 0.75 + r2 * math.sin(math.radians(a))
            d.line([x1, y1, x2, y2], fill=accent, width=3)
        d.ellipse([cx + s * 0.35, cy - s * 0.95, cx + s * 0.75, cy - s * 0.55],
                  fill=accent)
    elif kind == "flame":
        d.polygon([(cx, cy - s), (cx + s * 0.75, cy + s * 0.1),
                   (cx + s * 0.4, cy + s * 0.7), (cx, cy + s * 0.45),
                   (cx - s * 0.4, cy + s * 0.7), (cx - s * 0.75, cy + s * 0.1)],
                  fill=accent)
        d.polygon([(cx, cy - s * 0.35), (cx + s * 0.35, cy + s * 0.2),
                   (cx, cy + s * 0.6), (cx - s * 0.35, cy + s * 0.2)],
                  fill=(255, 220, 120))
    elif kind == "blast":
        pts = []
        for i in range(12):
            r = s if i % 2 == 0 else s * 0.45
            a = math.radians(i * 30)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=accent)
        d.ellipse([cx - s * 0.3, cy - s * 0.3, cx + s * 0.3, cy + s * 0.3],
                  fill=(255, 220, 120))
    elif kind == "rocket":
        d.polygon([(cx, cy - s), (cx + s * 0.45, cy - s * 0.1),
                   (cx + s * 0.45, cy + s * 0.6), (cx, cy + s),
                   (cx - s * 0.45, cy + s * 0.6), (cx - s * 0.45, cy - s * 0.1)],
                  fill=ink)
        d.ellipse([cx - s * 0.18, cy - s * 0.55, cx + s * 0.18, cy - s * 0.15],
                  fill=PAPER)
    elif kind == "cross":
        d.rectangle([cx - s * 0.25, cy - s, cx + s * 0.25, cy + s], fill=accent)
        d.rectangle([cx - s, cy - s * 0.25, cx + s, cy + s * 0.25], fill=accent)
    elif kind == "coin":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=ink, width=3)
        d.ellipse([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                  outline=ink, width=2)
        d.text((cx - 4, cy - 9), "B", font=font(SANS_B, 16), fill=ink)
    elif kind == "ball":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=ink, width=3)
        d.polygon([(cx, cy - s * 0.45), (cx + s * 0.43, cy - s * 0.14),
                   (cx + s * 0.26, cy + s * 0.36), (cx - s * 0.26, cy + s * 0.36),
                   (cx - s * 0.43, cy - s * 0.14)], fill=ink)
    elif kind == "flag":
        d.rectangle([cx - s * 0.15, cy - s, cx - s * 0.02, cy + s], fill=ink)
        d.polygon([(cx, cy - s), (cx + s, cy - s * 0.7),
                   (cx + s, cy - s * 0.3), (cx, cy - s * 0.55)], fill=accent)


def badge_circle(d, x, y, n, diam=26):
    """Red numbered circle."""
    d.ellipse([x, y, x + diam, y + diam], fill=RED)
    f = font(SANS_B, 15 if n < 10 else 13)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (diam - tw) / 2, y + (diam - 15) / 2 - 1), t, font=f,
           fill=(255, 255, 255))


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
    f_lead_b = font(SANS, 12)
    f_sec_b = font(SANS, 11)
    lead_w = (W - 44 - 6) / 2
    tw_lead = lead_w - 128 - 20
    for st in LEADS:
        lines = wrap(d, st["body"], f_lead_b, tw_lead)
        assert len(lines) <= 4, f"lead {st['n']} body needs {len(lines)} lines"
        assert len(wrap(d, st["title"], font(SANS_B, 17), tw_lead)) <= 1, \
            f"lead {st['n']} title wraps"
    sec_w = (W - 44 - 6) / 2
    tw_sec = sec_w - 86
    for st in SECONDARIES:
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']} \u00b7 {st['badge']}"
        assert d.textlength(title, font=font(SANS_B, 13)) <= tw_sec, \
            f"secondary {st['n']} title too long"
        # body must fit in 2 lines with " \u2014 src" on the last line
        suffix = " \u2014 " + st["src"]
        lines = wrap(d, st["body"], f_sec_b, tw_sec)
        assert len(lines) <= 2, f"secondary {st['n']} body needs {len(lines)} lines"
        assert d.textlength(lines[-1] + suffix, font=f_sec_b) <= tw_sec, \
            f"secondary {st['n']} body+src too long"
    f_also = font(SANS, 10)
    f_also_b = font(SANS_B, 9)
    for n, item, _r, badge in ALSO:
        bw = d.textlength(" \u00b7 " + badge, font=f_also_b)
        line = f"{n}. {item}"
        assert d.textlength(line, font=f_also) + bw <= 348, \
            f"ALSO {n} too long: {line}"
    dc = wrap(d, DATE_CHECK, font(SANS_B, 11), W - 44 - 20)
    assert len(dc) <= 2, f"DATE CHECK needs {len(dc)} lines"
    assert d.textlength(LEGEND, font=font(SANS, 9)) <= W - 44, "legend too long"
    for _num, lab, _n in NUMBERS:
        assert len(wrap(d, lab, font(SANS, 11), (W - 44) / 6 - 12)) == 1, \
            f"numbers label wraps: {lab}"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 22

    # sanity: 35 stories, region counts computed from the tags
    all_stories = list(LEADS) + list(SECONDARIES) + [
        dict(n=n, region=r) for n, _t, r, _b in ALSO]
    assert len(all_stories) == 35, len(all_stories)
    counts = Counter(s["region"] for s in all_stories)
    assert sum(counts.values()) == 35
    regions = [(name, counts[name]) for name in REGION_ORDER]

    fit_check(d)

    # ---------------- masthead ----------------
    d.rectangle([0, 0, W, 6], fill=RED)
    f_title = font(SERIF, 46)
    title = "THE MONDAY GLOBE"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 14), title, font=f_title, fill=INK)
    f_date = font(SERIF, 40)
    date = "MONDAY 23 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 64), date, font=f_date, fill=RED)
    f_sub = font(SANS, 13)
    sub = ("35 STORIES FROM ONE DAY  \u00b7  VERIFIED FROM LIVE REPORTS  "
           "\u00b7  ANTALYA \u00b7 BENGHAZI \u00b7 SANTA CLARA \u00b7 JAKARTA")
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, 110), sub, font=f_sub, fill=GREY)
    d.line([MX, 130, W - MX, 130], fill=INK, width=2)
    d.line([MX, 134, W - MX, 134], fill=INK, width=1)

    # ---------------- numbers strip ----------------
    y0, y1 = 142, 192
    cell_w = (W - 2 * MX) / 6
    f_num = font(SANS_B, 26)
    f_lab = font(SANS, 11)
    for i, (num, lab, story_n) in enumerate(NUMBERS):
        x = MX + i * cell_w
        if i:
            d.line([x, y0 + 4, x, y1 - 4], fill=GREY, width=1)
        tw = d.textlength(num, font=f_num)
        d.text((x + (cell_w - tw) / 2, y0 + 2), num, font=f_num, fill=RED)
        lines = wrap(d, lab, f_lab, cell_w - 12)
        yy = y0 + 32
        for ln in lines:
            tw = d.textlength(ln, font=f_lab)
            d.text((x + (cell_w - tw) / 2, yy), ln, font=f_lab, fill=INK)
            yy += 13
    d.line([MX, y1, W - MX, y1], fill=INK, width=1)

    # ---------------- region bar (counts computed above) ----------------
    y0 = 198
    total = sum(c for _, c in regions)
    x = MX
    bar_w = W - 2 * MX
    f_reg = font(SANS_B, 11)
    for (name, cnt), col in zip(regions, REGION_COLS):
        seg = bar_w * cnt / total
        d.rectangle([x, y0, x + seg - 1, y0 + 20], fill=col)
        label = f"{REGION_SHORT.get(name, name)} {cnt}"
        tw = d.textlength(label, font=f_reg)
        d.text((x + (seg - tw) / 2, y0 + 4), label, font=f_reg,
               fill=(255, 255, 255))
        x += seg
    d.text((MX, y0 + 24),
           "WHERE THE NEWS CAME FROM \u2014 35 STORIES, 6 REGIONS",
           font=font(SANS_B, 10), fill=GREY)

    # ---------------- leads: 2 x 2 ----------------
    lead_y, lead_h, gap = 236, 124, 6
    lead_w = (W - 2 * MX - gap) / 2
    f_tag = font(SANS_B, 10)
    f_lead_t = font(SANS_B, 17)
    f_lead_b = font(SANS, 12)
    f_src = font(SANS, 10)
    for i, st in enumerate(LEADS):
        x = MX + (i % 2) * (lead_w + gap)
        y = lead_y + (i // 2) * (lead_h + gap)
        d.rectangle([x, y, x + lead_w, y + lead_h], fill=PANEL,
                    outline=INK, width=1)
        iw = 128
        d.rectangle([x + 1, y + 1, x + iw, y + lead_h - 1], fill=st["tint"])
        draw_icon(d, st["kind"], x + iw / 2, y + lead_h / 2 - 4, 34,
                  PAPER, (255, 220, 120))
        badge_circle(d, x + 6, y + 6, st["n"])
        tx = x + iw + 10
        tw_ = lead_w - iw - 20
        d.text((tx, y + 7), st["tag"], font=f_tag, fill=RED)
        # verification pill, top-right of the panel
        fill = BADGE_FILL[st["badge"]]
        f_pill = font(SANS_B, 9)
        pw = d.textlength(st["badge"], font=f_pill) + 14
        badge_pill(d, x + lead_w - pw - 8, y + 6, st["badge"], fill)
        yy = y + 23
        for ln in wrap(d, st["title"], f_lead_t, tw_):
            d.text((tx, yy), ln, font=f_lead_t, fill=INK)
            yy += 20
        for ln in wrap(d, st["body"], f_lead_b, tw_):
            d.text((tx, yy), ln, font=f_lead_b, fill=INK)
            yy += 14
        d.text((tx, y + lead_h - 16), "Source: " + st["src"], font=f_src,
               fill=GREY)

    # ---------------- secondaries: 2 cols x 5 rows ----------------
    sec_y, sec_h, sec_gap = 496, 40, 4
    sec_w = (W - 2 * MX - gap) / 2
    f_sec_t = font(SANS_B, 13)
    f_sec_b = font(SANS, 11)
    for i, st in enumerate(SECONDARIES):
        x = MX + (i % 2) * (sec_w + gap)
        y = sec_y + (i // 2) * (sec_h + sec_gap)
        d.rectangle([x, y, x + sec_w, y + sec_h], fill=PANEL, outline=GREY,
                    width=1)
        draw_icon(d, st["kind"], x + 22, y + sec_h / 2, 13, INK, RED)
        badge_circle(d, x + 44, y + 8, st["n"], diam=24)
        tx = x + 76
        tw_ = sec_w - 86
        # title line: number + title + tag, then coloured badge word
        head = f"{st['n']}. {st['title']}  \u2014  {st['tag']}  \u00b7  "
        d.text((tx, y + 2), head, font=f_sec_t, fill=INK)
        hw = d.textlength(head, font=f_sec_t)
        d.text((tx + hw, y + 2), st["badge"], font=f_sec_t,
               fill=BADGE_FILL[st["badge"]])
        # body, 2 lines max, with the source appended to the last line
        suffix = " \u2014 " + st["src"]
        lines = wrap(d, st["body"], f_sec_b, tw_)
        # trim the last line so the source fits on it
        while (d.textlength(lines[-1] + suffix, font=f_sec_b) > tw_
               and len(lines[-1]) > 10):
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip(" ,.;")
        yy = y + 19
        for j, ln in enumerate(lines):
            d.text((tx, yy), ln, font=f_sec_b, fill=(60, 56, 48))
            if j == len(lines) - 1:
                sw = d.textlength(ln, font=f_sec_b)
                d.text((tx + sw, yy), suffix, font=f_sec_b, fill=GREY)
            yy += 11

    # ---------------- bottom band: map + ALSO ----------------
    bot_y, bot_h = 720, 240
    map_w = 600
    d.rectangle([MX, bot_y, MX + map_w, bot_y + bot_h], fill=PANEL,
                outline=INK, width=1)
    d.text((MX + 10, bot_y + 6), "WHERE IT HAPPENED",
           font=font(SANS_B, 13), fill=RED)
    d.text((MX + 10, bot_y + 24), "Numbered pins match the stories above",
           font=font(SANS, 10), fill=GREY)
    mx0, my0 = MX + 14, bot_y + 44
    mw, mh = map_w - 28, bot_h - 56
    cw, ch = mw / 64, mh / 24
    for r, spans in enumerate(MAP_ROWS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                d.ellipse([mx0 + c * cw + 1, my0 + r * ch + 1,
                           mx0 + (c + 1) * cw - 1, my0 + (r + 1) * ch - 1],
                          fill=(150, 160, 140))
    f_pin = font(SANS_B, 10)
    for n, lon, lat, dx, dy in PINS:
        px = mx0 + (lon + 180) / 360 * mw
        py = my0 + (90 - lat) / 150 * mh
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, cx, cy], fill=GREY, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = d.textlength(t, font=f_pin)
        d.text((cx - tw / 2, cy - 7), t, font=f_pin, fill=(255, 255, 255))

    # ALSO list
    ax = MX + map_w + 12
    aw = W - MX - ax
    d.rectangle([ax, bot_y, ax + aw, bot_y + bot_h], fill=PANEL,
                outline=INK, width=1)
    d.text((ax + 10, bot_y + 6), "ALSO ON MONDAY",
           font=font(SANS_B, 13), fill=RED)
    d.line([ax + 10, bot_y + 26, ax + aw - 10, bot_y + 26], fill=GREY, width=1)
    f_also = font(SANS, 10)
    f_also_b = font(SANS_B, 9)
    yy = bot_y + 28
    for n, item, _r, badge in ALSO:
        line = f"{n}. {item}"
        d.text((ax + 10, yy), line, font=f_also, fill=INK)
        bw = d.textlength(line, font=f_also)
        d.text((ax + 10 + bw, yy), " \u00b7 " + badge, font=f_also_b,
               fill=BADGE_FILL[badge])
        yy += 10

    # ---------------- DATE CHECK footer ----------------
    fy = bot_y + bot_h + 8
    d.rectangle([MX, fy, W - MX, fy + 30], fill=(232, 222, 200), outline=RED,
                width=1)
    f_dc = font(SANS_B, 11)
    lines = wrap(d, DATE_CHECK, f_dc, W - 2 * MX - 20)
    yy = fy + 3
    for ln in lines:
        d.text((MX + 10, yy), ln, font=f_dc, fill=INK)
        yy += 13

    # ---------------- HOW WE CHECKED legend ----------------
    d.text((MX, fy + 34), LEGEND, font=font(SANS, 9), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
