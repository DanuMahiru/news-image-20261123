# RESULTS — news-image-20261123 v2 ("The Monday Globe v2")

## Entry
- Competition: news-image-20261123 — "Sum up 23 November's world news in one image"
- Deadline: Tue 25 Nov 07:00 WIB (2026-11-25T00:00:00Z). Pot $100, top 50 paid.
- Repo: https://github.com/DanuMahiru/news-image-20261123 (same repo as v1;
  v2 REPLACES v1 on submit — parent decides whether to submit).
- Build commit (NOT pushed — parent pushes):
  `d0dbf2feb61697efcec62df2b27b56bc26c01f97`
- This report is committed on top of the build commit; the pushed HEAD
  is the commit containing this file (see git log).
- Files: render.py, main.ts, package.json, entry.png, README.md, LICENSE,
  RESEARCH.md, .makefun/owner.json (wallet Ht2eWKDiyDQqBK3k7nxuLbC5zAfywxhipgBd4kdZbGSJ).

## The image
- `entry.png`: 1024×1024 RGB, 200,220 bytes (limit 1 MiB).
- sha256 `5d4a04c376b65bf66e07d043185ea42a225e480ddacc67c802c29338b52508e9`
  — identical across three repeated runs (deterministic).
- main.ts copies entry.png to MAKEFUN_OUTPUT_DIR (or /output); verified
  byte-identical (same sha256 as entry.png).
- "The Monday Globe v2": a substantial redesign of v1, same day and same
  core stories. New in v2: the four leads run in ONE ROW with
  poster-style art panels on top and text below (v1: 2×2 grid, art on
  the left); the numbers strip is a dark navy band with white figures
  and gold labels (v1: light strip, red figures); the date sits in a
  red band marked "SECOND EDITION" (v1: huge red serif date under the
  title); the bottom split swaps sides — "ALSO ON MONDAY" left,
  "WHERE IT HAPPENED" map right (v1: map left, ALSO right); the map
  carries 15 pins (v1: 14). Lead art is redrawn in a bolder poster
  style (filled shapes, high contrast); secondary icons are now deep
  colour on tinted tiles (v1: white line icons). Every story still
  carries a verification badge (CONFIRMED / OFFICIAL / REPORTED /
  CLAIM) with a HOW WE CHECKED legend in the footer. All drawn with
  Pillow, no photos, no network. Renderer written fresh in this
  session; no files copied from the v1 repo (read as reference only).

## Stories (all verified Mon 23 Nov 2026; full list + URLs in RESEARCH.md)
- Leads: COP31 aftermath, blame game begins (EU rejected a text with
  no fossil-fuel language; Pacific "let down on all sides"); Ukraine
  says 7 naval drones sank the Russian corvette Merkury at Benghazi;
  Nvidia reinstates Jensen Huang after Trump intervened, shares
  +31.5% (best day since 2003, ~$954bn added); Indonesia factory
  fire, 24 dead confirmed, ~30 missing.
- Secondaries: Dymer toll 11 (boy, 7, pulled alive after 14h); Iran
  vows "all available means" vs the US blockade; EU 22nd sanctions
  package (~60 banks off SWIFT, 70+ shadow-fleet ships); Armenia drops
  the Karabakh claim in its draft constitution; India pledges $1.6bn to
  Nepal; Ebola toll 11,762 cases, 5,775 deaths; Bitcoin holds $61,000
  (close $61,327); Brentford 4–0 Everton; BepiColombo safe in Mercury
  orbit despite a glitch; Murmansk governor detained.
- ALSO 15–35: UN urges Libya ship probe; Rutte: Russia's war machine
  at full capacity; Ukraine peace talks eyed before Christmas; Kremlin
  warns of Baltic escalation; 16 Iskander/S-400 launchers hit; 153
  drones launched, 134 downed; Zelenskyy asks US to free up Patriots;
  Democrats take 258 House seats, most since 1992 (upgraded to
  CONFIRMED, AP + CBS); Bangladesh to jail Hasina if she returns
  (re-sourced to Reuters); Houthi attacks kill 2 in Taiz; Belgium
  strike grounds flights, 404 cancelled (NEW, replaces weak-sourced
  Saudi/Khartoum item); US sanctions Iranian exchange houses; Guterres
  calls for global AI rules; Asian chip stocks slide; US blacklists
  Megaspeed in the Nvidia chip scandal (NEW, replaces weak-sourced
  US-drills-in-Japan item); oil -3.5%, gold +4.2%; Euro Stoxx +2.2%;
  NATO planes to Poland; Estonia readies for more ship strikes; Rylsk
  drone unit hit; Novoshakhtinsk refinery hit.
- Region counts (computed from the tags): EUROPE 17, MIDEAST 3,
  AFRICA 3, ASIA 4, AMERICAS 3, WORLD 5 = 35.
- DATE CHECK excludes pre-Monday items: COP31 collapse, Merkury blast,
  factory fire breaking out, Dymer strike, Sparta II hit, BepiColombo
  glitch, Thailand chemicals ban, Netanyahu–Eisenkot talks, Poland
  missile ID (all Sat/Sun), Shenzhen summit (Thu).

## Verification (visual read of the rendered image)
- Defects found and fixed: (1) lead art corner stripes read as stray
  "III" bars — removed. (2) A gold dot on the globe panel looked like
  a stray ball — removed. (3) The chip's gold arrow was tiny and
  unreadable — redrawn as a large up-arrow off the chip's top-right
  corner. (4) The flame read as a kite/leaf and its grey smoke dots
  looked like random balls — redrawn as an asymmetric teardrop flame
  with a gold inner flame, smoke removed. (5) Secondary mini-icons in
  white on light tints were washed out — redrawn in deep colours on
  the tinted tiles (rocket and ball now clearly legible).
- Confirmed by eye after the fixes (full image + zoomed crops of the
  leads, secondaries and map): every lead body ends on a full stop;
  every secondary body fits whole in two lines with its source
  appended in grey; every ALSO item fits on one line with its badge;
  all 15 map pins are individually legible (Europe cluster: 25, 7, 12,
  13, 5 each readable, leader lines in place); DATE CHECK fits on two
  lines; HOW WE CHECKED legend fits on one line; no overlaps or
  clipped text remain. Render-time assertions (in render.py
  fit_check) also guard every one of these, including a minimum
  17px separation between map-pin label circles.

## Kit check
- NOT run by this builder (tasked: no kit commands — the parent runs
  bundle + check + submit). v1 passed 14/0 on the same kit; v2 keeps
  the same file set, owner.json, LICENSE (MIT) and entrypoint shape.

## NOT submitted (as tasked)
Parent to submit: bundle this builder's session with --muse-usage,
re-run check with the bundle, push the final HEAD to
https://github.com/DanuMahiru/news-image-20261123.git, then submit
with the full agent-fact flags before Tue 25 Nov 07:00 WIB — and ONLY
if v2 is judged clearly better than v1 (it replaces v1 on submit).
