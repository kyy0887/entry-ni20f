// Entrypoint: stage entry.png into the output directory.
// Node 22 runs this directly as ESM, no build step needed.

import { copyFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

const DEFAULT_OUT = "/output";

async function main() {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || DEFAULT_OUT;
  const here = fileURLToPath(new URL(".", import.meta.url));
  const src = join(here, "entry.png");

  mkdirSync(outDir, { recursive: true });
  copyFileSync(src, join(outDir, "entry.png"));

  console.log(`[entry] entry.png copied -> ${outDir}`);
}

main().catch((err) => {
  console.error("[entry] failed:", err);
  process.exit(1);
});
