// AWS Factory · patching film — one miniature 3D world, three looks.
// Everything is a pure function of (shot, p, t): HyperFrames seeks each frame on its own.
//   buildWorld(style) -> { scene, camera, set(shot, p, t), anchors }
// Public-safe: generic groups only, no IDs, names, dates or counts from a real account.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

export const STYLES = {
  // A · pastel miniature, soft light, rounded "clay" edges (the owner's earlier pick)
  diorama: {
    sky: ["#ffd8c4", "#ece6ff"], night: ["#4b4f86", "#a99ad6"], ground: "#f4e7d0", side: "#e3ceaa",
    pad: { db: "#8fd1c0", code: "#f7b59c", backup: "#b6c2f3" }, rack: "#fffaf2", trim: "#3d4a5c",
    walls: "#f3c48d", roof: "#e07a5f", belt: "#6b7a8f", image: "#f2b134", gate: "#ffd76e",
    sec: "#5fc184", other: "#62a3e8", app: "#ee6b67", shelf: "#d9b98c", ring: "#7b6cf6",
    edges: null, round: 0.12, flat: false, soft: true, rough: 0.82, hemi: 1.15, sun: 2.1, fov: 26,
  },
  // B · blueprint isometric: white blocks, navy outlines, one orange accent
  blueprint: {
    sky: ["#eef3fa", "#dce6f4"], night: ["#d3dcec", "#bccbe2"], ground: "#ffffff", side: "#eef2f8",
    pad: { db: "#e6f1ff", code: "#fff1e6", backup: "#eef0ff" }, rack: "#ffffff", trim: "#1d3a6b",
    walls: "#ffffff", roof: "#f3f6fb", belt: "#dfe6f2", image: "#ff7a1a", gate: "#ffffff",
    sec: "#2e9e5b", other: "#2f6fd6", app: "#d6453d", shelf: "#ffffff", ring: "#ff7a1a",
    edges: "#1d3a6b", round: 0.0, flat: true, soft: false, rough: 1, hemi: 2.4, sun: 0.0, fov: 14,
  },
  // C · bold toy blocks: saturated primaries, hard sun, flat faces
  toy: {
    sky: ["#7fcfff", "#d8f2ff"], night: ["#24306e", "#5a6fc0"], ground: "#5cc46b", side: "#3e9a4d",
    pad: { db: "#ffd23f", code: "#3fa7ff", backup: "#ff5c8a" }, rack: "#ffffff", trim: "#1b1b2f",
    walls: "#ff8c42", roof: "#d7263d", belt: "#2e2e3a", image: "#ffd23f", gate: "#ffd23f",
    sec: "#2ecc71", other: "#2f80ed", app: "#eb3b5a", shelf: "#c9a46b", ring: "#ffffff",
    edges: null, round: 0.0, flat: true, soft: false, rough: 0.6, hemi: 1.0, sun: 3.0, fov: 30,
  },
};

const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const seg = (p, a, b) => ease((p - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;

function gradientTexture([top, bottom]) {
  const c = document.createElement("canvas");
  c.width = 4; c.height = 256;
  const g = c.getContext("2d");
  const gr = g.createLinearGradient(0, 0, 0, 256);
  gr.addColorStop(0, top); gr.addColorStop(1, bottom);
  g.fillStyle = gr; g.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export function buildWorld(styleName) {
  const S = STYLES[styleName];
  const scene = new THREE.Scene();
  const day = gradientTexture(S.sky), night = gradientTexture(S.night);
  scene.background = day;
  const camera = new THREE.PerspectiveCamera(S.fov, 16 / 9, 0.5, 400);

  // ---------- materials and helpers
  const mats = {};
  const mat = (hex, extra = {}) => {
    const k = hex + JSON.stringify(extra);
    if (!mats[k]) mats[k] = new THREE.MeshStandardMaterial({ color: hex, roughness: S.rough, metalness: 0, flatShading: S.flat, ...extra });
    return mats[k];
  };
  const edgeMat = S.edges ? new THREE.LineBasicMaterial({ color: S.edges }) : null;
  const box = (w, h, d, hex, r = S.round, extra) => {
    const geo = r > 0 ? new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2, h / 2, d / 2) * 0.999) : new THREE.BoxGeometry(w, h, d);
    const m = new THREE.Mesh(geo, mat(hex, extra));
    m.castShadow = m.receiveShadow = true;
    if (edgeMat) m.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(w, h, d)), edgeMat));
    return m;
  };
  const cyl = (rt, rb, h, hex, seg = 24, extra) => {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, S.flat ? Math.min(seg, 12) : seg), mat(hex, extra));
    m.castShadow = m.receiveShadow = true;
    if (edgeMat) m.add(new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry, 30), edgeMat));
    return m;
  };
  const put = (o, x, y, z, parent = scene) => { o.position.set(x, y, z); parent.add(o); return o; };

  // ---------- lights
  const hemi = new THREE.HemisphereLight("#ffffff", styleName === "toy" ? "#3e9a4d" : "#d8c8b0", S.hemi);
  scene.add(hemi);
  const sun = new THREE.DirectionalLight("#fff3e2", S.sun);
  sun.position.set(-10, 22, 14);
  sun.castShadow = S.sun > 0;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -20, right: 20, top: 14, bottom: -14, near: 1, far: 70 });
  sun.shadow.bias = -0.0006;
  sun.shadow.radius = S.soft ? 6 : 1;
  scene.add(sun);

  // ---------- ground island
  const ground = box(30, 0.8, 16, S.ground, S.round > 0 ? 0.4 : 0);
  put(ground, 0, -0.4, 0);
  const skirt = box(30.6, 0.6, 16.6, S.side, S.round > 0 ? 0.3 : 0);
  put(skirt, 0, -0.95, 0);
  if (styleName === "blueprint") { const grid = new THREE.GridHelper(30, 30, "#9fb6d9", "#c9d7ec"); grid.scale.z = 16 / 30; grid.position.y = 0.012; scene.add(grid); }

  // ---------- the factory (road 1: build fresh)
  const factory = new THREE.Group(); put(factory, -10.5, 0, -2.2);
  put(box(4.4, 2.4, 3.4, S.walls), 0, 1.2, 0, factory);
  for (let i = 0; i < 3; i++) {
    const tooth = cyl(0.85, 0.85, 3.4, S.roof, 3);
    tooth.rotation.set(-Math.PI / 2, 0, 0); // triangular prism along z, apex up
    put(tooth, -1.45 + i * 1.45, 2.75, 0, factory);
  }
  put(cyl(0.32, 0.38, 2.2, S.roof), 1.4, 3.5, -1.0, factory);
  put(box(1.2, 1.3, 0.12, S.trim, 0.04), 2.2, 0.65, 0.6, factory).rotation.y = Math.PI / 2;
  const belt = put(box(5.4, 0.3, 1.0, S.belt, 0.1), -5.6, 0.35, -1.6);
  const images = [];
  for (let i = 0; i < 4; i++) images.push(put(box(0.62, 0.62, 0.62, S.image, 0.14), 0, 0.82, -1.6));

  // ---------- the rules gate (patch baseline)
  const gate = new THREE.Group(); put(gate, -0.4, 0, -1.0);
  put(box(0.5, 3.0, 0.5, S.gate), -1.2, 1.5, 0, gate);
  put(box(0.5, 3.0, 0.5, S.gate), 1.2, 1.5, 0, gate);
  put(box(3.0, 0.55, 0.65, S.gate), 0, 3.1, 0, gate);
  const lane = put(box(1.9, 0.12, 9.5, S.belt, 0.05), -0.4, 0.06, -4.6);
  const barrierPivot = new THREE.Group(); put(barrierPivot, 0.95, 0.9, 0.6, gate);
  const barrier = box(2.2, 0.16, 0.16, S.app, 0.06); barrier.position.x = -1.1; barrierPivot.add(barrier);
  const shelf = new THREE.Group(); put(shelf, -3.6, 0, -4.4);
  put(box(2.0, 0.18, 1.3, S.shelf, 0.06), 0, 1.0, 0, shelf);
  put(box(0.16, 1.0, 1.3, S.shelf, 0.04), -0.92, 0.5, 0, shelf);
  put(box(0.16, 1.0, 1.3, S.shelf, 0.04), 0.92, 0.5, 0, shelf);
  const calendar = put(box(0.9, 1.0, 0.2, "#ffffff", 0.06), 0, 1.75, -0.55, shelf);
  put(box(0.9, 0.24, 0.22, S.app, 0.05), 0, 0.42, 0, calendar);
  const crates = {
    sec: box(0.75, 0.75, 0.75, S.sec, 0.12),
    other: box(0.75, 0.75, 0.75, S.other, 0.12),
    app: box(0.75, 0.75, 0.75, S.app, 0.12),
  };
  for (const c of Object.values(crates)) scene.add(c);

  // ---------- districts (patch groups), each with racks and a tag flag
  const racks = [];
  const lights = [];
  const district = (key, cx, cz, cols, rows, flagHex) => {
    const g = new THREE.Group(); put(g, cx, 0, cz);
    const w = cols * 1.5 + 0.8, d = rows * 1.6 + 0.9;
    put(box(w, 0.16, d, S.pad[key], 0.07), 0, 0.08, 0, g);
    for (let c = 0; c < cols; c++) for (let r = 0; r < rows; r++) {
      const rk = new THREE.Group();
      put(box(1.0, 1.7, 0.95, S.rack), 0, 1.0, 0, rk);
      for (let s = 0; s < 3; s++) put(box(0.7, 0.1, 0.04, S.trim, 0.02), 0, 0.6 + s * 0.4, 0.49, rk);
      const led = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 12), new THREE.MeshStandardMaterial({ color: "#f5a623", emissive: "#f5a623", emissiveIntensity: 0.6, roughness: 0.4 }));
      put(led, 0, 2.0, 0, rk);
      lights.push(led);
      put(rk, (c - (cols - 1) / 2) * 1.5, 0, (r - (rows - 1) / 2) * 1.6, g);
      racks.push(rk);
    }
    const pole = cyl(0.05, 0.05, 2.6, S.trim, 8); put(pole, -w / 2 + 0.25, 1.3, -d / 2 + 0.25, g);
    const flag = box(0.9, 0.55, 0.05, flagHex, 0.03); put(flag, -w / 2 + 0.72, 2.3, -d / 2 + 0.25, g);
    return { g, w, d, flag };
  };
  const D = {
    db: district("db", 6.2, -3.4, 3, 1, S.pad.db),
    code: district("code", 4.6, 2.9, 2, 1, S.pad.code),
    backup: district("backup", 10.6, 2.9, 1, 1, S.pad.backup),
  };
  // the lonely host: carries a tag that no group uses
  const lonely = new THREE.Group(); put(lonely, 11.6, 0, -3.2);
  put(box(1.0, 1.7, 0.95, S.rack), 0, 1.0, 0, lonely);
  const lonelyLed = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 12), new THREE.MeshStandardMaterial({ color: "#f5a623", emissive: "#f5a623", emissiveIntensity: 0.6 }));
  put(lonelyLed, 0, 2.0, 0, lonely);
  put(cyl(0.05, 0.05, 2.4, S.trim, 8), -0.7, 1.2, -0.5, lonely);
  put(box(0.8, 0.5, 0.05, "#b9b9c6", 0.03), -0.28, 2.1, -0.5, lonely);
  const halo = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.06, 8, 48), new THREE.MeshBasicMaterial({ color: S.app, transparent: true }));
  halo.rotation.x = Math.PI / 2; put(halo, 0, 0.12, 0, lonely);

  // scan ring and moon
  const ring = new THREE.Mesh(new THREE.TorusGeometry(2.6, 0.07, 10, 64), new THREE.MeshBasicMaterial({ color: S.ring, transparent: true, opacity: 0.85 }));
  ring.rotation.x = Math.PI / 2; scene.add(ring);
  const moon = new THREE.Mesh(new THREE.SphereGeometry(1.3, 32, 20), new THREE.MeshBasicMaterial({ color: "#fff6d8" }));
  scene.add(moon);

  // ---------- camera presets (position, target)
  const CAM = {
    wide: [[1, 17, 31], [1.0, 2.8, -1.5]],
    factory: [[-6, 9, 15], [-6.5, 1.2, -1.5]],
    districts: [[13.5, 13, 21], [7.4, 0.2, -0.6]],
    gate: [[-5.8, 8.2, 12], [-1.6, 1.0, -2.0]],
    night: [[6, 11, 19], [7.4, 1.4, -0.4]],
    lonely: [[18, 9.5, 12.5], [9.6, 0.6, -1.0]],
    close: [[-1, 12, 24], [2.5, 0.8, -0.5]],
  };
  if (styleName === "blueprint") for (const k in CAM) { const [pos, tgt] = CAM[k]; CAM[k] = [[tgt[0] + (pos[0] - tgt[0]) * 2.1, tgt[1] + (pos[1] - tgt[1]) * 2.4, tgt[2] + (pos[2] - tgt[2]) * 2.1], tgt]; }
  const v = new THREE.Vector3(), w2 = new THREE.Vector3();
  const aim = (a, b, k, drift) => {
    const A = CAM[a], B = CAM[b];
    v.set(lerp(A[0][0], B[0][0], k), lerp(A[0][1], B[0][1], k), lerp(A[0][2], B[0][2], k));
    w2.set(lerp(A[1][0], B[1][0], k), lerp(A[1][1], B[1][1], k), lerp(A[1][2], B[1][2], k));
    v.x += drift; camera.position.copy(v); camera.lookAt(w2);
  };

  const setLed = (m, hex) => { m.material.color.set(hex); m.material.emissive.set(hex); };
  const AMBER = "#f5a623", GREEN = "#3ccf6e", GREY = "#9aa0ad";

  // anchors for HTML labels (world positions)
  const anchors = {
    factory: new THREE.Vector3(-10.5, 4.4, -2.2), gate: new THREE.Vector3(-0.4, 4.0, -1.0), shelf: new THREE.Vector3(-3.6, 2.6, -4.4),
    db: new THREE.Vector3(6.2, 2.9, -3.4), code: new THREE.Vector3(4.6, 2.9, 2.9), backup: new THREE.Vector3(10.6, 2.9, 2.9),
    lonely: new THREE.Vector3(11.6, 2.9, -3.2), barrier: new THREE.Vector3(0.4, 1.6, -0.4),
  };

  // ---------- the state function
  function set(shot, p, t) {
    const drift = Math.sin(t * 0.35) * 0.35;
    scene.background = shot === "night" ? night : day;
    hemi.intensity = shot === "night" ? S.hemi * 0.4 : S.hemi;
    hemi.color.set(shot === "night" ? "#9fa8ff" : "#ffffff");
    sun.intensity = shot === "night" ? S.sun * 0.35 : S.sun;
    // conveyor: images ride out of the factory
    images.forEach((m, i) => { const u = ((t * 0.5 + i * 1.35) % 5.4); m.position.set(-8.3 + u, 0.82, -1.6); m.rotation.y = u * 0.4; m.visible = true; });
    // defaults
    ring.visible = false; moon.visible = false; halo.visible = false;
    barrierPivot.rotation.z = 0;
    crates.sec.position.set(-0.4, 0.5, -8.5); crates.other.position.set(-0.4, 0.5, -7.2); crates.app.position.set(-0.4, 0.5, -5.9);
    for (const l of lights) setLed(l, AMBER);
    setLed(lonelyLed, AMBER);
    for (const k in D) D[k].flag.scale.setScalar(1);

    switch (shot) {
      case "hook": aim("wide", "wide", 0, drift); break;
      case "roads": aim("wide", "wide", 0, drift); break;
      case "groups": {
        aim("districts", "districts", 0, drift);
        const k = Math.sin(t * 3) * 0.5 + 0.5;
        for (const key in D) D[key].flag.scale.setScalar(1 + 0.25 * k);
        break;
      }
      case "rules": {
        aim("gate", "gate", 0, drift * 0.6);
        const a = seg(p, 0.05, 0.6);
        crates.sec.position.set(-0.4, 0.5, lerp(-5.5, 1.6, a));               // security: straight through
        crates.other.position.set(lerp(-0.4, -3.6, a), lerp(0.5, 1.48, a), lerp(-6.6, -4.4, a)); // others: wait on the 7-day shelf
        crates.app.position.set(-0.4, 0.5, lerp(-7.8, -0.9, a));              // application packages: stopped at the barrier
        barrierPivot.rotation.z = 0;
        break;
      }
      case "night": {
        aim("night", "night", 0, drift);
        moon.visible = true; camera.updateMatrixWorld();
        moon.position.copy(camera.localToWorld(v.set(10.6, 4.6 + 0.15 * Math.sin(t * 0.6), -40)));
        ring.visible = true;
        const sweep = (t * 0.45) % 1;
        ring.position.set(lerp(3.6, 11.5, sweep), 1.0 + Math.sin(t * 2.0) * 0.6, lerp(-3.4, 2.9, sweep) * 0.2);
        break;
      }
      case "trap": {
        aim("lonely", "lonely", 0, drift * 0.6);
        halo.visible = true; halo.material.opacity = 0.55 + 0.45 * Math.sin(t * 4);
        for (const l of lights) setLed(l, GREEN);
        setLed(lonelyLed, AMBER);
        break;
      }
      case "check": {
        aim("districts", "wide", 0.35, drift);
        for (const l of lights) setLed(l, GREEN);
        setLed(lonelyLed, GREEN);
        break;
      }
      case "close": default: {
        aim("close", "close", 0, drift);
        for (const l of lights) setLed(l, GREEN);
        setLed(lonelyLed, GREEN);
      }
    }
  }
  anchors.sec = crates.sec.position; anchors.other = crates.other.position; anchors.app = crates.app.position;
  return { scene, camera, set, anchors };
}
