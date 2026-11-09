// AWS Factory · patching film — one 3D toy world with three server families.
// Everything is a pure function of (state, t): HyperFrames seeks each frame on its own (hf-seek).
//   buildWorld() -> { scene, camera, apply(state, t), anchors, CAM }
// Public-safe: generic families only; no IDs, host names, dates, times or counts from a real account.
// The Phase 1 look comparison was built from an earlier revision of this file (commit 254f6d3).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const S = {
  sky: ["#7fcfff", "#d8f2ff"], night: ["#1f2a66", "#5267b8"], ground: "#5cc46b", side: "#3e9a4d",
  rack: "#ffffff", trim: "#1b1b2f", walls: "#ff8c42", roof: "#d7263d", belt: "#2e2e3a", image: "#ffd23f",
  gate: "#ffd23f", sec: "#2ecc71", other: "#2f80ed", app: "#eb3b5a", shelf: "#c9a46b", ring: "#ffffff",
  hemi: 1.0, sun: 3.0, fov: 30,
};
export const FAM = {
  gitlab: { color: "#fc6d26", pad: "#ffc9a3", cx: 4.3, cz: -4.3 },
  mongo: { color: "#13aa52", pad: "#b9efcd", cx: 4.6, cz: 3.7 },
  ecs: { color: "#2f80ed", pad: "#bcd8ff", cx: 10.9, cz: -0.2 },
};
const AMBER = "#f5a623", GREEN = "#3ccf6e";

const sm = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const cl = (x) => Math.min(1, Math.max(0, x));
const lerp = (a, b, k) => a + (b - a) * k;
const back = (x) => { x = cl(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

export function buildWorld() {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(S.fov, 16 / 9, 0.5, 400);

  // ---------- helpers
  const cache = {};
  const mat = (hex, extra = {}) => {
    const k = hex + JSON.stringify(extra);
    return cache[k] || (cache[k] = new THREE.MeshStandardMaterial({ color: hex, roughness: 0.6, metalness: 0, flatShading: true, ...extra }));
  };
  const glowMat = (hex, i = 0.9) => new THREE.MeshStandardMaterial({ color: hex, emissive: hex, emissiveIntensity: i, roughness: 0.4 });
  const box = (w, h, d, m, r = 0) => {
    const g = r > 0 ? new RoundedBoxGeometry(w, h, d, 2, Math.min(r, w / 2, h / 2, d / 2) * 0.999) : new THREE.BoxGeometry(w, h, d);
    const o = new THREE.Mesh(g, typeof m === "string" ? mat(m) : m); o.castShadow = o.receiveShadow = true; return o;
  };
  const cyl = (rt, rb, h, m, seg = 20) => { const o = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), typeof m === "string" ? mat(m) : m); o.castShadow = o.receiveShadow = true; return o; };
  const ball = (r, m) => { const o = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 12), typeof m === "string" ? mat(m) : m); o.castShadow = true; return o; };
  const put = (o, x, y, z, parent = scene) => { o.position.set(x, y, z); parent.add(o); return o; };
  const rod = (a, b, r, m, parent) => { // a cylinder from point a to point b
    const d = new THREE.Vector3().subVectors(b, a), o = cyl(r, r, d.length(), m, 10);
    o.position.copy(a).addScaledVector(d, 0.5); o.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.clone().normalize()); parent.add(o); return o;
  };
  const ledMat = () => new THREE.MeshStandardMaterial({ color: AMBER, emissive: AMBER, emissiveIntensity: 0.7, roughness: 0.4 });

  // ---------- lights
  const hemi = new THREE.HemisphereLight("#ffffff", "#3e9a4d", S.hemi); scene.add(hemi);
  const sun = new THREE.DirectionalLight("#fff3e2", S.sun);
  sun.position.set(-10, 22, 14); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -20, right: 20, top: 14, bottom: -14, near: 1, far: 70 });
  sun.shadow.bias = -0.0006; scene.add(sun);
  const rim = new THREE.DirectionalLight("#ffd59a", 1.3); rim.position.set(14, 10, -18); scene.add(rim);

  // ---------- island
  put(box(31, 0.8, 17, S.ground), 0, -0.4, 0);
  put(box(31.6, 0.6, 17.6, S.side), 0, -0.95, 0);

  // ---------- factory, belt and splitter (road 1 and the image line)
  const factory = new THREE.Group(); put(factory, -11.2, 0, -2.2);
  put(box(4.4, 2.4, 3.4, S.walls), 0, 1.2, 0, factory);
  for (let i = 0; i < 3; i++) { const t = cyl(0.85, 0.85, 3.4, S.roof, 3); t.rotation.set(-Math.PI / 2, 0, 0); put(t, -1.45 + i * 1.45, 2.75, 0, factory); }
  put(cyl(0.32, 0.38, 2.2, S.roof), 1.4, 3.5, -1.0, factory);
  const puffs = [0, 1, 2].map(() => put(ball(0.32, new THREE.MeshStandardMaterial({ color: "#ffffff", transparent: true, roughness: 1 })), 1.4, 4.8, -1.0, factory));
  put(box(0.12, 1.3, 1.2, S.trim), 2.22, 0.65, 0.6, factory);
  put(box(5.4, 0.3, 1.0, S.belt, 0.1), -6.3, 0.35, -1.6);
  const images = []; for (let i = 0; i < 4; i++) images.push(put(box(0.62, 0.62, 0.62, S.image, 0.14), 0, 0.82, -1.6));
  const splitter = put(cyl(0.9, 1.0, 0.35, "#ffffff"), -3.0, 0.18, -1.6);
  const baseDisc = put(cyl(0.6, 0.6, 0.2, glowMat("#ffd23f", 0.5)), 0, 0, 0); baseDisc.rotation.x = Math.PI / 2;
  const famDisc = {}; for (const k in FAM) { famDisc[k] = put(cyl(0.5, 0.5, 0.18, glowMat(FAM[k].color, 0.6)), 0, 0, 0); famDisc[k].rotation.x = Math.PI / 2; }

  // ---------- the rules gate (patch baseline)
  const gate = new THREE.Group(); put(gate, -0.6, 0, -1.0);
  put(box(0.5, 3.0, 0.5, S.gate), -1.2, 1.5, 0, gate); put(box(0.5, 3.0, 0.5, S.gate), 1.2, 1.5, 0, gate); put(box(3.0, 0.55, 0.65, S.gate), 0, 3.1, 0, gate);
  put(box(1.9, 0.12, 9.5, S.belt, 0.05), -0.6, 0.06, -4.2);
  const barrierPivot = new THREE.Group(); put(barrierPivot, 0.95, 0.9, 0.6, gate);
  const barrier = box(2.2, 0.16, 0.16, S.app, 0.06); barrier.position.x = -1.1; barrierPivot.add(barrier);
  const shelf = new THREE.Group(); put(shelf, -3.8, 0, -4.6);
  put(box(2.0, 0.18, 1.3, S.shelf, 0.06), 0, 1.0, 0, shelf); put(box(0.16, 1.0, 1.3, S.shelf), -0.92, 0.5, 0, shelf); put(box(0.16, 1.0, 1.3, S.shelf), 0.92, 0.5, 0, shelf);
  const cal = put(box(0.9, 1.0, 0.2, "#ffffff", 0.06), 0, 1.75, -0.55, shelf); put(box(0.9, 0.24, 0.22, S.app), 0, 0.42, 0, cal);
  const crates = { sec: box(0.75, 0.75, 0.75, S.sec, 0.12), other: box(0.75, 0.75, 0.75, S.other, 0.12), app: box(0.75, 0.75, 0.75, S.app, 0.12) };
  for (const c of Object.values(crates)) scene.add(c);

  // ---------- the three families
  const F = {};
  const family = (key, w, d) => {
    const f = FAM[key], g = new THREE.Group(); put(g, f.cx, 0, f.cz);
    const padMat = new THREE.MeshStandardMaterial({ color: f.pad, emissive: f.color, emissiveIntensity: 0, roughness: 0.7, flatShading: true });
    put(box(w, 0.18, d, padMat, 0.08), 0, 0.09, 0, g);
    put(box(w + 0.25, 0.1, d + 0.25, f.color), 0, 0.03, 0, g);
    const flagG = new THREE.Group(); put(flagG, -w / 2 + 0.3, 0, -d / 2 + 0.3, g);
    put(cyl(0.05, 0.05, 2.8, S.trim, 8), 0, 1.4, 0, flagG);
    const flag = put(box(1.0, 0.6, 0.06, f.color, 0.03), 0.52, 2.45, 0, flagG);
    const clock = new THREE.Group(); put(clock, w / 2 - 0.35, 0, -d / 2 + 0.35, g);
    put(cyl(0.05, 0.05, 2.2, S.trim, 8), 0, 1.1, 0, clock);
    const face = put(cyl(0.62, 0.62, 0.1, "#ffffff", 28), 0, 2.75, 0, clock); face.rotation.x = Math.PI / 2;
    const wedge = new THREE.Mesh(new THREE.CircleGeometry(0.56, 24, Math.PI / 6, Math.PI / 3), new THREE.MeshBasicMaterial({ color: f.color })); put(wedge, 0, 2.75, 0.06, clock);
    const hand = new THREE.Group(); put(hand, 0, 2.75, 0.09, clock); const hm = box(0.07, 0.5, 0.04, S.trim); hm.position.y = 0.22; hand.add(hm);
    F[key] = { g, padMat, flagG, flag, clock, hand, units: [], leds: [], missing: [] };
    return F[key];
  };
  const unitLed = (fk, u, y, x = 0, z = 0) => { const l = put(ball(0.15, ledMat()), x, y, z, u); F[fk].leds.push(l); return l; };
  const missingCube = (fk, u, y) => {
    const m = put(box(0.34, 0.34, 0.34, new THREE.MeshStandardMaterial({ color: S.app, emissive: S.app, emissiveIntensity: 0.35, roughness: 0.5 })), 0, y, 0, u);
    m.userData.y = y; F[fk].missing.push(m); return m;
  };

  // GitLab: two towers joined by a glowing pipeline
  const gl = family("gitlab", 4.6, 3.4);
  for (const x of [-1.05, 1.05]) {
    const u = new THREE.Group(); put(u, x, 0, 0.2, gl.g);
    put(box(1.15, 2.3, 1.15, S.rack, 0.08), 0, 1.25, 0, u);
    put(box(1.3, 0.28, 1.3, FAM.gitlab.color, 0.06), 0, 2.5, 0, u);
    for (let s = 0; s < 3; s++) put(box(0.8, 0.16, 0.04, glowMat("#7ad3ff", 0.6)), 0, 0.7 + s * 0.5, 0.59, u);
    unitLed("gitlab", u, 2.85); missingCube("gitlab", u, 3.6); gl.units.push(u);
  }
  const pn = [new THREE.Vector3(-1.05, 3.3, 0.2), new THREE.Vector3(0, 3.9, 0.2), new THREE.Vector3(1.05, 3.3, 0.2)];
  pn.forEach((p) => put(ball(0.2, glowMat(FAM.gitlab.color, 0.5)), p.x, p.y, p.z, gl.g));
  rod(pn[0], pn[1], 0.06, FAM.gitlab.color, gl.g); rod(pn[1], pn[2], 0.06, FAM.gitlab.color, gl.g);
  const pulses = [0, 1].map(() => put(ball(0.12, glowMat("#ffd23f", 1.2)), 0, 0, 0, gl.g));

  // MongoDB: three vault members in a replica ring
  const mg = family("mongo", 5.0, 3.4);
  const mpos = [[-1.5, 0.55], [0, -0.55], [1.5, 0.55]];
  const wheels = [];
  for (const [x, z] of mpos) {
    const u = new THREE.Group(); put(u, x, 0, z, mg.g);
    put(cyl(0.6, 0.66, 1.8, S.rack, 20), 0, 1.0, 0, u);
    for (const y of [0.45, 1.55]) { const band = new THREE.Mesh(new THREE.TorusGeometry(0.64, 0.06, 6, 24), mat(FAM.mongo.color)); band.rotation.x = Math.PI / 2; put(band, 0, y, 0, u); }
    const wheel = new THREE.Group(); put(wheel, 0, 1.0, 0.64, u);
    wheel.add(new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.05, 6, 20), mat("#c9a227")));
    for (let s = 0; s < 3; s++) { const sp = box(0.56, 0.05, 0.05, "#c9a227"); sp.rotation.z = (s * Math.PI) / 3; wheel.add(sp); }
    wheels.push(wheel);
    unitLed("mongo", u, 2.05); missingCube("mongo", u, 2.8); mg.units.push(u);
  }
  const mtop = mpos.map(([x, z]) => new THREE.Vector3(x, 2.05, z));
  for (let i = 0; i < 3; i++) rod(mtop[i], mtop[(i + 1) % 3], 0.04, glowMat(FAM.mongo.color, 0.5), mg.g);
  const mpulse = put(ball(0.11, glowMat("#eafff1", 1.3)), 0, 0, 0, mg.g);

  // CloudOS workspace on ECS: worker nodes carrying containers, and a gantry crane
  const ec = family("ecs", 5.8, 5.0);
  const cols = ["#eb3b5a", "#ffd23f", "#2ecc71", "#9b59b6"];
  [[-1.25, -0.9], [1.25, -0.9], [-1.25, 1.15], [1.25, 1.15]].forEach(([x, z], i) => {
    const u = new THREE.Group(); put(u, x, 0, z, ec.g);
    put(box(1.5, 0.95, 1.3, S.rack, 0.08), 0, 0.6, 0, u);
    put(box(1.52, 0.14, 1.32, FAM.ecs.color), 0, 0.95, 0, u);
    put(box(0.62, 0.42, 0.95, cols[i]), -0.34, 1.25, 0, u); put(box(0.62, 0.42, 0.95, cols[(i + 2) % 4]), 0.34, 1.25, 0, u);
    unitLed("ecs", u, 0.62, 0.62, 0.66); missingCube("ecs", u, 2.1); ec.units.push(u);
  });
  for (const x of [-2.6, 2.6]) for (const z of [-2.1, 2.1]) put(box(0.22, 3.6, 0.22, "#ffd23f"), x, 1.8, z, ec.g);
  for (const z of [-2.1, 2.1]) put(box(5.4, 0.28, 0.3, "#ffd23f"), 0, 3.6, z, ec.g);
  const trolley = put(box(0.6, 0.3, 4.6, S.trim), 0, 3.85, 0, ec.g);
  const cable = put(cyl(0.025, 0.025, 1, S.trim, 6), 0, 3, 0, ec.g);
  const hookBox = put(box(0.62, 0.42, 0.95, "#ff8c42"), 0, 2.4, 0, ec.g);

  // ---------- the lonely host: carries a tag that no group uses
  const lonely = new THREE.Group(); put(lonely, 13.2, 0, -5.9);
  put(box(1.0, 1.7, 0.95, S.rack, 0.08), 0, 0.9, 0, lonely);
  const lonelyLed = put(ball(0.15, ledMat()), 0, 1.95, 0, lonely);
  put(cyl(0.05, 0.05, 2.4, S.trim, 8), -0.7, 1.2, -0.5, lonely); put(box(0.8, 0.5, 0.05, "#9aa0ad", 0.03), -0.28, 2.1, -0.5, lonely);
  const halo = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.07, 8, 48), new THREE.MeshBasicMaterial({ color: S.app, transparent: true }));
  halo.rotation.x = Math.PI / 2; put(halo, 0, 0.12, 0, lonely);
  const lonelyDrop = put(box(0.42, 0.42, 0.42, new THREE.MeshStandardMaterial({ color: S.sec, transparent: true, flatShading: true })), 0, 0, 0);

  // ---------- scan beam, reboot sign, moon
  const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 2.9, 7, 32, 1, true),
    new THREE.MeshBasicMaterial({ color: "#bfe8ff", transparent: true, opacity: 0.25, side: THREE.DoubleSide, depthWrite: false }));
  scene.add(beam);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(2.9, 0.08, 10, 64), new THREE.MeshBasicMaterial({ color: S.ring, transparent: true }));
  ring.rotation.x = Math.PI / 2; scene.add(ring);
  const reboot = new THREE.Group(); put(reboot, FAM.ecs.cx + 3.7, 3.0, FAM.ecs.cz + 1.8);
  const spin = new THREE.Group(); reboot.add(spin);
  spin.add(new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.13, 8, 32, Math.PI * 1.6), glowMat("#f5a623", 0.8)));
  const rTip = new THREE.Mesh(new THREE.ConeGeometry(0.26, 0.42, 3), glowMat("#f5a623", 0.8)); rTip.position.set(0.55, 0, 0); rTip.rotation.z = Math.PI; spin.add(rTip);
  const moon = new THREE.Mesh(new THREE.SphereGeometry(1.3, 32, 20), new THREE.MeshBasicMaterial({ color: "#fff6d8" })); scene.add(moon);

  // ---------- camera presets [position, target]
  const CAM = {
    intro: [[-3, 34, 46], [1.0, 0.0, -0.5]],
    wide: [[1, 17, 31], [1.0, 2.8, -1.5]],
    belt: [[-6.5, 9.5, 15], [-8.4, 1.4, -1.8]],
    split: [[-1, 13, 21], [2.0, 1.6, -1.2]],
    families: [[14, 13.5, 21], [7.8, 2.0, -0.3]],
    gate: [[-6.0, 8.2, 12], [-1.8, 1.0, -2.0]],
    night: [[7.5, 13, 21], [8.0, 2.6, -0.3]],
    ecs: [[18, 10.5, 16.5], [11.2, 2.6, 0.2]],
    lonely: [[21, 9.5, -12.5], [11.6, 0.8, -3.8]],
    check: [[5, 14, 25], [6.0, 1.2, -0.6]],
    close: [[-1, 12.5, 25], [3.0, 0.8, -0.5]],
  };

  // ---------- sky painting (night blend)
  const bgCanvas = document.createElement("canvas"); bgCanvas.width = 4; bgCanvas.height = 256;
  const bgTex = new THREE.CanvasTexture(bgCanvas); bgTex.colorSpace = THREE.SRGBColorSpace; scene.background = bgTex;
  let bgKey = -1;
  const ca = new THREE.Color(), cb = new THREE.Color();
  const mix = (h1, h2, k) => "#" + ca.set(h1).lerp(cb.set(h2), k).getHexString();
  const paintSky = (n) => {
    const key = Math.round(n * 200); if (key === bgKey) return; bgKey = key;
    const g = bgCanvas.getContext("2d"), gr = g.createLinearGradient(0, 0, 0, 256);
    gr.addColorStop(0, mix(S.sky[0], S.night[0], n)); gr.addColorStop(1, mix(S.sky[1], S.night[1], n));
    g.fillStyle = gr; g.fillRect(0, 0, 4, 256); bgTex.needsUpdate = true;
  };
  const cA = new THREE.Color(AMBER), cG = new THREE.Color(GREEN), cOff = new THREE.Color("#30323a"), tmp = new THREE.Color();
  const led = (m, g, off = 0) => { tmp.copy(cA).lerp(cG, g).lerp(cOff, off); m.material.color.copy(tmp); m.material.emissive.copy(tmp); };
  const secC = new THREE.Color(S.sec), redC = new THREE.Color(S.app);
  const camAt = (spec) => { const [p, t] = CAM[spec[0]], d = spec[1] ?? 1; return [t.map((x, i) => x + (p[i] - x) * d), t]; };
  const v = new THREE.Vector3();
  const fams = Object.keys(FAM);

  function apply(st, t) {
    const n = st.night || 0;
    paintSky(n);
    hemi.intensity = S.hemi * (1 - 0.6 * n); hemi.color.set(mix("#ffffff", "#9fa8ff", n));
    sun.intensity = S.sun * (1 - 0.7 * n); rim.intensity = 1.3 * (1 - 0.3 * n);
    // camera: blend two presets, plus a slow drift so the frame never freezes
    const [pa, ta] = camAt(st.cam[0]), [pb, tb] = camAt(st.cam[1]), k = st.cam[2];
    camera.position.set(lerp(pa[0], pb[0], k) + Math.sin(t * 0.31) * 0.45, lerp(pa[1], pb[1], k) + Math.sin(t * 0.23) * 0.25, lerp(pa[2], pb[2], k));
    camera.lookAt(lerp(ta[0], tb[0], k), lerp(ta[1], tb[1], k), lerp(ta[2], tb[2], k));
    camera.updateMatrixWorld();

    // factory life: images on the belt, chimney puffs
    images.forEach((m, i) => { const u = (t * 0.5 + i * 1.35) % 5.4; m.position.set(-9.0 + u, 0.82, -1.6); m.rotation.y = u * 0.4; });
    puffs.forEach((p, i) => { const u = (t * 0.35 + i / 3) % 1; p.position.set(1.4 + u * 0.6, 4.7 + u * 1.8, -1.0); p.scale.setScalar(0.6 + u * 1.2); p.material.opacity = 0.85 * (1 - u); });

    // the image line: one base image splits into three family images that fly to their pads
    const sp = st.split || 0;
    const a0 = sm(cl(sp / 0.35));
    baseDisc.visible = sp > 0 && sp < 0.42;
    baseDisc.position.set(lerp(-6.4, -3.0, a0), 0.9 + Math.sin(a0 * Math.PI) * 0.8 + 0.4 * a0, -1.6); baseDisc.rotation.z = t * 2;
    splitter.scale.setScalar(1 + 0.25 * Math.sin(cl((sp - 0.3) / 0.15) * Math.PI));
    fams.forEach((fk, i) => {
      const d = famDisc[fk], a = sm(cl((sp - 0.38 - i * 0.06) / 0.45));
      d.visible = sp > 0.38 && a < 1;
      d.position.set(lerp(-3.0, FAM[fk].cx, a), 1.2 + Math.sin(a * Math.PI) * 4.2 + a * 1.8, lerp(-1.6, FAM[fk].cz, a)); d.rotation.z = t * 3;
    });
    // families: units pop in when their image lands; flags rise; pads glow when active; clocks appear
    for (const fk of fams) {
      const r = st.reveal?.[fk] ?? 1, f = F[fk];
      f.units.forEach((u, i) => { const s = Math.max(0.0001, back(r * 1.5 - i * 0.18)); u.scale.set(s, s, s); });
      f.flagG.position.y = lerp(-2.9, 0, sm(cl(r * 1.4 - 0.3)));
      f.flag.scale.setScalar(1 + 0.3 * (st.flags || 0) * (0.5 + 0.5 * Math.sin(t * 5)));
      f.padMat.emissiveIntensity = 0.45 * (st.glow?.[fk] || 0) * (0.6 + 0.4 * Math.sin(t * 4));
      f.clock.scale.setScalar(Math.max(0.0001, back(st.clock || 0)));
      f.hand.rotation.z = -(st.hand?.[fk] ?? t * 0.4);
    }
    // idle machinery: GitLab pipeline pulses, MongoDB wheels and replica pulse, ECS crane swapping a container
    pulses.forEach((p, i) => { const u = (t * 0.45 + i * 0.5) % 1, s = u < 0.5 ? u * 2 : (u - 0.5) * 2; p.position.lerpVectors(u < 0.5 ? pn[0] : pn[1], u < 0.5 ? pn[1] : pn[2], s); });
    wheels.forEach((w, i) => (w.rotation.z = t * 0.9 + i));
    { const u = (t * 0.3) % 1, s3 = Math.floor(u * 3), s = u * 3 - s3; mpulse.position.lerpVectors(mtop[s3], mtop[(s3 + 1) % 3], s); }
    { const u = (t / 7) % 1, x = Math.sin(t * 0.45) * 1.6, drop = Math.sin(Math.PI * cl((u - 0.3) / 0.4)) * 1.0;
      trolley.position.x = x; hookBox.position.set(x, 2.5 - drop, 0.15);
      const top = 3.7, bot = 2.71 - drop; cable.position.set(x, (top + bot) / 2, 0.15); cable.scale.y = Math.max(0.05, top - bot); }

    // crates at the rules gate
    const ci = st.crateIn ?? 1, fall = (k0) => 0.5 + (1 - sm(k0)) * 9;
    const s1 = sm(st.sec || 0), s2 = sm(st.other || 0), s3 = sm(st.app || 0);
    crates.sec.position.set(-0.6, (st.sec || 0) > 0 ? 0.5 : fall(cl(ci / 0.6)), lerp(-5.5, 1.6, s1));
    crates.other.position.set(lerp(-0.6, -3.8, s2), (st.other || 0) > 0 ? lerp(0.5, 1.48, s2) : fall(cl((ci - 0.2) / 0.6)), lerp(-6.6, -4.6, s2));
    crates.app.position.set(-0.6, (st.app || 0) > 0 ? 0.5 : fall(cl((ci - 0.4) / 0.6)), lerp(-7.8, -0.9, s3));
    for (const key of ["sec", "other", "app"]) crates[key].rotation.y = Math.sin(t * 1.3 + key.length) * 0.08;
    barrierPivot.rotation.z = lerp(1.1, 0, sm(st.barrier ?? 1));

    // patch flow: missing patches appear after the scan; installs turn them green and sink them in
    for (const fk of fams) {
      const f = F[fk], m = st.missing?.[fk] || 0, fx = st.fix?.[fk] || 0;
      f.missing.forEach((c, i) => {
        const appear = back(m * 1.6 - i * 0.15), sink = sm(cl(fx * 1.5 - i * 0.12));
        c.visible = appear > 0.01 && sink < 0.99;
        c.scale.setScalar(Math.max(0.0001, appear * (1 - sink)));
        c.position.y = c.userData.y + 0.12 * Math.sin(t * 3 + i) - sink * 0.9;
        c.rotation.y = t * 1.5 + i;
        c.material.color.copy(redC).lerp(secC, cl(fx * 2.5 - i * 0.2)); c.material.emissive.copy(c.material.color);
      });
      const down = fk === "ecs" ? (st.down || 0) : 0;
      f.leds.forEach((l) => led(l, st.green?.[fk] || 0, down));
      if (down) f.units.forEach((u) => (u.scale.y = u.scale.x * (1 - 0.18 * down)));
    }
    // scan beam: [x, z, scale, opacity]
    const sc = st.scan;
    beam.visible = ring.visible = !!sc;
    if (sc) {
      beam.position.set(sc[0], 3.5, sc[1]); beam.scale.set(sc[2], 1, sc[2]); beam.material.opacity = 0.28 * sc[3];
      ring.position.set(sc[0], 0.35 + 1.6 * (0.5 + 0.5 * Math.sin(t * 2.4)), sc[1]); ring.scale.setScalar(sc[2]); ring.material.opacity = 0.9 * sc[3];
    }
    // reboot sign over the ECS group, facing the camera
    const rb = st.reboot || 0;
    reboot.visible = rb > 0.01; reboot.scale.setScalar(Math.max(0.0001, back(rb))); reboot.lookAt(camera.position); spin.rotation.z = -t * 2.2;
    // lonely host
    const ld = st.lonelyDrop || 0;
    lonelyDrop.visible = ld > 0 && ld < 1;
    lonelyDrop.position.set(13.2, lerp(9, 4.0, sm(cl(ld * 1.6))), -5.9); lonelyDrop.material.opacity = 1 - sm(cl((ld - 0.6) / 0.4));
    led(lonelyLed, st.green?.lonely || 0);
    halo.visible = (st.halo || 0) > 0.01; halo.material.opacity = (st.halo || 0) * (0.55 + 0.45 * Math.sin(t * 4));
    moon.visible = n > 0.05;
    if (moon.visible) moon.position.copy(camera.localToWorld(v.set(10.6, lerp(-2, 4.6, n), -40)));
  }

  const anchors = {
    factory: new THREE.Vector3(-10.6, 3.4, -0.6), split: new THREE.Vector3(-3.0, 1.2, -1.6), lonely: new THREE.Vector3(13.2, 2.9, -5.9),
    gitlab: new THREE.Vector3(FAM.gitlab.cx, 4.5, FAM.gitlab.cz), mongo: new THREE.Vector3(FAM.mongo.cx, 3.0, FAM.mongo.cz),
    ecs: new THREE.Vector3(FAM.ecs.cx, 4.4, FAM.ecs.cz), reboot: new THREE.Vector3(FAM.ecs.cx + 3.0, 4.1, FAM.ecs.cz + 1.8),
    sec: crates.sec.position, other: crates.other.position, app: crates.app.position,
  };
  return { scene, camera, apply, anchors, CAM };
}
