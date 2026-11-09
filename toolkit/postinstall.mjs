// Copy the pinned GSAP runtime into every film that loads it from assets/gsap.min.js (it is not committed).
import fs from "node:fs"; import path from "node:path";
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const gsap = path.join(root, "node_modules/gsap/dist/gsap.min.js");
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
  e.name === "node_modules" || e.name.startsWith(".") ? [] : e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
let n = 0;
for (const f of walk(path.join(root, "films")).filter((f) => f.endsWith(".html"))) {
  if (!fs.readFileSync(f, "utf8").includes("assets/gsap.min.js")) continue;
  const a = path.join(path.dirname(f), "assets"); fs.mkdirSync(a, { recursive: true });
  fs.copyFileSync(gsap, path.join(a, "gsap.min.js")); n++;
}
console.log(`gsap.min.js copied into ${n} film folders`);
