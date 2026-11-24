// The Monday Globe — make.fun news-image-20261123 entry.
//
// The image is drawn at build time by render.py (Pillow) and shipped in
// this repository as entry.png. This program only copies that file to the
// output directory, so both graded runs write exactly the same bytes.
// Node 22, standard library only; no network.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error("entry.png is missing from the repository: " + source);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
if (!existsSync(target) || statSync(target).size !== statSync(source).size) {
  throw new Error("entry.png was not copied to " + target);
}
console.log("wrote " + target);
