import { copyFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(dirname(new URL(import.meta.url).pathname), "entry.png"), join(outDir, "entry.png"));
console.log("entry.png written to", outDir);
