# The World In One Day — cinematic editorial redesign, 20 November 2026 (v4)

![poster](entry.png)

A ground-up rebuild from a blank 1024×1024 canvas (not a polish of v3): one dominant
hero story, two secondary leads in deliberately different visual formats, six strong
supporting items, and a real equirectangular world map.

**Palette** — paper `#F3F0E8`, ink `#171B22`, graphite `#4B5158`, signal red `#B64B43`,
navy `#203B52`, blue-grey `#708D9D`, forest green `#4F765F`, brass `#B49A67`.
DejaVu Serif for masthead/headlines/figures, DejaVu Sans for labels and metadata.
Deterministic Pillow render — no randomness, no timestamps, byte-identical across runs.

**18 verified news items**, all reported on Friday 20 November 2026.

Layout:
- **Masthead** — 47 px serif wordmark, double rule, `FRIDAY, 20 NOVEMBER 2026` at 24 px,
  edition subtitle right-aligned.
- **Hero (560×344)** — *Kyiv overnight assault*, a layered cinematic night scene:
  gradient night sky with deterministic stars and moon, three depth-separated skyline
  layers with lit windows, river and arched bridge, smoke columns, ballistic missile
  tracks with glowing warheads and four intercept bursts, searchlight beams. Headline
  band beneath in white serif on near-black, with two corner stat flags.
- **Key figures** — verified values only: 300,000+ evacuated, $93.5bn IPO, $2.36bn GTA VI,
  Nikkei −5.1%, 9+ killed.
- **Secondary lead 1 — Cyclone Akvan**: Odisha coastal map (sea, land polygon, coastline
  stroke), three-arm storm spiral, landfall crosshair at Gopalpur, three data figures.
- **Secondary lead 2 — Asia markets**: three-index weekly line chart (Nikkei −5.1%,
  KOSPI −5.2%, Taiwan −6.2%) with labels inside the plot, plus a GTA VI data block with
  comparison bars.
- **Also on Friday** — 6 curated items, each with a region tag, colour key, headline,
  source. No wall of tiny cards.
- **Where it happened** — equirectangular world map drawn from coastal coordinate
  polygons (19 landmasses incl. Greenland, Japan, Indonesia, Australia, New Zealand),
  graticule, continent labels, 8 correctly placed numbered markers, full legend.
- **Footer** — date-check line, sources, edition/version.

RGB 1024×1024 PNG (~204 KB, no palette quantisation). Verified: two runs byte-identical
(`cmp`), 1024×1024, under the 1 MiB limit.

## Run

```bash
python3 render.py   # generates entry.png (1024x1024, RGB)
node main.ts        # stages entry.png + manifest.json into $MAKEFUN_OUTPUT_DIR or /output
```

Referral: a2ffxt26
