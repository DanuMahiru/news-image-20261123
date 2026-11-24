# The Monday Globe — news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/DanuMahiru/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/DanuMahiru/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world news of **Monday 23 November 2026**,
built for the make.fun competition
https://make.fun/bounty/news-image-20261123
(pot $100, top 50 paid; entries close Tue 25 Nov 07:00 WIB).

## The image

`entry.png` (1024×1024, ~208 KB) is a newspaper front page drawn with
Pillow by `render.py`: 35 numbered stories, a huge date masthead
("MONDAY 23 NOVEMBER 2026"), a 6-cell numbers strip (every cell tied
to an illustrated story), a region bar with per-region counts computed
from the story tags, 4 large illustrated leads, 10 illustrated
secondaries, a "WHERE IT HAPPENED" dotted world map with 14 numbered
pins, an "ALSO ON MONDAY" list, a DATE CHECK box, and per-story source
attribution. Every story carries a verification badge — CONFIRMED,
OFFICIAL, REPORTED or CLAIM — explained by a HOW WE CHECKED legend in
the footer. No photos, no network — every glyph is drawn from shapes.

Leads: COP31 aftermath, blame game begins · Ukraine says its sea
drones sank the Russian corvette Merkury at Benghazi · Nvidia
reinstates Jensen Huang, shares jump 31.5% · Indonesia factory fire,
24 dead confirmed.

## Files

- `render.py` — draws `entry.png` (deterministic: same bytes every run)
- `main.ts` — Node 22, stdlib only; copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR` (or `/output`)
- `entry.png` — the finished image
- `RESEARCH.md` — every story with its source URL
- `RESULTS.md` — build report (commit, hashes, kit check)
- `.makefun/owner.json` — claim file for the make.fun wallet

## Run it

```sh
python3 render.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Research

All 35 stories were verified from live reports on 24 Nov 2026
(Reuters, AP, Al Jazeera, CNN, ESA, European Commission, WHO/UN News,
Finnhub). Only stories that happened or were first reported on Monday
23 Nov 2026 are leads; earlier items (COP31 collapse itself, the
Merkury blast, the factory fire breaking out, the Dymer strike, the
Sparta II hit, the BepiColombo glitch, the Thailand chemicals ban,
the Netanyahu–Eisenkot talks, the Poland missile ID, the Shenzhen
summit) are listed in the DATE CHECK box, never as leads. Full list
with sources: `RESEARCH.md`.
