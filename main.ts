// Entrypoint: stage entry.png + manifest.json into the output directory.
// Node 22 runs this directly as ESM, no build step needed.

import { copyFileSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

const DEFAULT_OUT = "/output";
const EDITION = "2026-1120";
const ITEMS = 18;
const VERSION = "v4";

async function main() {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || DEFAULT_OUT;
  const here = fileURLToPath(new URL(".", import.meta.url));
  const src = join(here, "entry.png");

  mkdirSync(outDir, { recursive: true });
  copyFileSync(src, join(outDir, "entry.png"));

  const manifest = {
    image: "entry.png",
    dimensions: { width: 1024, height: 1024 },
    edition: EDITION,
    items: ITEMS,
    version: VERSION,
  };
  writeFileSync(join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");

  const bytes = statSync(src).size;
  console.log(`[entry] entry.png (${bytes} bytes) + manifest.json -> ${outDir}`);
  console.log(`[entry] items: ${ITEMS}, edition: ${EDITION}, version: ${VERSION}`);
}

main().catch((err) => {
  console.error("[entry] failed:", err);
  process.exit(1);
});
