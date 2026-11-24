# RESULTS — news-image-20261123 ("The Monday Globe")

## Entry
- Competition: news-image-20261123 — "Sum up 23 November's world news in one image"
- Deadline: Tue 25 Nov 07:00 WIB (2026-11-25T00:00:00Z). Pot $100, top 50 paid.
- Repo: https://github.com/DanuMahiru/news-image-20261123
- Build commit (NOT pushed — parent pushes):
  `fb5ac88d6e8b5e9c04e848cad46bc7a82d60b730`
- This report is committed on top of the build commit; the pushed HEAD
  is the commit containing this file (see git log).
  - Parent commit `b8a7431` (owner.json, pre-existing; untouched).
- Files: render.py, main.ts, package.json, entry.png, README.md, LICENSE,
  RESEARCH.md, .makefun/owner.json (wallet Ht2eWKDiyDQqBK3k7nxuLbC5zAfywxhipgBd4kdZbGSJ).

## The image
- `entry.png`: 1024×1024 RGB, 208,428 bytes (limit 1 MiB).
- sha256 `d95cbdc553633f47fc2bf42dadc02d46d7be1762c4f007d2a1cb30cd8197b10e`
  — identical across repeated runs (deterministic).
- main.ts copies entry.png to MAKEFUN_OUTPUT_DIR (or /output); verified
  byte-identical (same sha256 as entry.png).
- "The Monday Globe", news-21 v2 / news-22 formula: 35 numbered stories,
  date masthead "MONDAY 23 NOVEMBER 2026", 6-cell numbers strip (7 naval
  drones · 31.5% Nvidia · 24 factory-fire dead · 11 killed in Dymer ·
  5,775 Ebola deaths · $61,327 Bitcoin close), region bar computed from
  the story tags (EUROPE 16, MIDEAST 4, AFRICA 3, ASIA 5, AMERICAS 2,
  WORLD 5 = 35), 4 illustrated leads + 10 illustrated secondaries,
  dotted world map with 14 numbered pins, "ALSO ON MONDAY" list (21
  more), DATE CHECK box, per-story sources. New in this edition: every
  story carries a verification badge (CONFIRMED / OFFICIAL / REPORTED /
  CLAIM) with a HOW WE CHECKED legend in the footer. All drawn with
  Pillow, no photos, no network. Renderer written fresh in this session;
  no files copied from the news-22 repo (read as design reference only).

## Stories (all verified Mon 23 Nov 2026; full list + URLs in RESEARCH.md)
- Leads: COP31 aftermath, blame game begins (first COP failure since
  2009; Pacific "let down on all sides"); Ukraine says 7 naval drones
  sank the Russian corvette Merkury at Benghazi; Nvidia reinstates
  Jensen Huang, shares +31.5% (best day since 2003, ~$950bn added);
  Indonesia factory fire, 24 dead confirmed, ~30 missing.
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
  Democrats take 258 House seats; Bangladesh to jail Hasina if she
  returns; Houthi attacks kill 2 in Taiz; Saudi condemns UN-site attack
  in Khartoum; US sanctions Iranian exchange houses; Guterres calls for
  global AI rules; Asian chip stocks slide; US troops drill live-fire
  in Japan; oil -3.5%, gold +4.2%; Euro Stoxx +2.2%; NATO planes to
  Poland; Estonia readies for more ship strikes; Rylsk drone unit hit;
  Novoshakhtinsk refinery hit.
- DATE CHECK excludes pre-Monday items: COP31 collapse, Merkury blast,
  factory fire breaking out, Dymer strike, Sparta II hit, BepiColombo
  glitch, Thailand chemicals ban, Netanyahu–Eisenkot talks, Poland
  missile ID (all Sat/Sun), Shenzhen summit (Thu).

## Verification (visual read of the rendered image)
- Defects found and fixed: (1) numbers-strip labels wrapped to two
  lines and the second line was clipped by the strip's bottom rule —
  shortened every label to one line ("naval drones · №2" etc.) and added
  a render-time assertion that each label fits one line. (2) Map pins
  merged into a blob over Europe (London/Brussels/Darmstadt) and touched
  around Antalya/Dymer/Benghazi and Ituri/Khartoum — added per-pin label
  offsets with thin leader lines to the true point; all 14 pins are now
  individually legible.
- Confirmed by eye after the fixes: every lead body ends on a full stop;
  every secondary body fits whole in two lines with its source appended
  in grey; every ALSO item fits whole with its badge; DATE CHECK fits on
  two lines; HOW WE CHECKED legend fits on one line; no overlaps or
  clipped text remain.

## Kit check (local, kit news-image-20261123-kit, --worktree, no transcripts)
- 4 passed, 1 failed, 14 skipped, 5 checked at submission.
- Passes: competition_open, snapshot (8 files, 255,019 bytes),
  license_osi (SPDX MIT), entrypoint (main.ts / node22).
- FAIL (expected, no transcripts supplied): transcripts_present.
- At submission: repo_public, repo_owner, repo_created_after_open,
  commit_in_repo, duplicate_snapshot — need the push + submit.
- NOTE — blind rounds are ON for this competition (RULES.txt): nothing
  is judged when you submit and no live rank or score shows until the
  rounds publish. Next round: 2026-11-24T00:00:00Z. The dev grade will
  show no provisional rate; the parent should check
  GET /api/competitions/news-image-20261123/rounds after that round.

## NOT submitted (as tasked)
Parent to submit: bundle this builder's session with --muse-usage,
re-run check with the bundle, push the final HEAD to
https://github.com/DanuMahiru/news-image-20261123.git, then submit
with the full agent-fact flags before Tue 25 Nov 07:00 WIB.
