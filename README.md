# The World In One Day — premium editorial infographic, 20 November 2026 (v3)

![poster](entry.png)

A total redesign of the v2 dark broadsheet into a premium international-newspaper
infographic on cream paper (#F4F0E5) with editorial ink (#171717) and muted accents:
dull red, navy, dull blue, forest green, antique gold. Serif typography (DejaVu Serif)
for date/headlines/statistics, sans-serif (DejaVu Sans) for labels and captions.
Deterministic Pillow render — no randomness, no timestamps, byte-identical across runs.

**32 verified news items** (all dated 20 November 2026, UTC): 3 lead stories,
9 supporting cards, 20 numbered briefs.

Layout (8 sections):
- **Masthead** — kicker, oversized serif date, one-sentence editorial summary, double rule
- **Key statistics** — 9+ Kyiv dead · 300K+ evacuated · $2.36bn GTA VI · Nikkei -5.1% · $93.5bn Anthropic IPO
- **Region strip** — Europe(6) Asia-Pacific(6) Middle East(6) Americas(4) Africa(3) Oceania(2) Global(5)
- **Three leads** with vector illustrations: Kyiv night-sky missile intercepts, Cyclone Akvan
  landfall map with storm spiral, Asian index selloff line chart + GTA VI bars
- **Supporting grid** — 9 cards, each with a distinct vector icon (UK-EU flags, trilateral
  table, downed plane, Riyadh tower, Hormuz tanker, gavel, chip, bitcoin coin, COP globe)
- **Where it happened** — dot-matrix world map with 10 numbered, colour-coded markers + legend
- **Also on Friday** — 3-column × 7-row numbered briefs
- **Footer** — date-check line + sources, thin rules

RGB 1024×1024 PNG (~460 KB, no palette quantisation). Built-in QA: bounding-box overlap
detector across all text runs (must report "none").

## Run

```bash
python3 render.py   # generates entry.png (1024x1024, RGB)
node main.ts        # stages entry.png + manifest.json into $MAKEFUN_OUTPUT_DIR or /output
```

Referral: a2ffxt26
