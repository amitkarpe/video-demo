#!/usr/bin/env python3
"""Phase 1 review pack for the patching film: a Three.js miniature world inside HyperFrames.
  python3 phase1/make_phase1.py   -> phase1/styles/ (3 looks x 2 key frames) and phase1/storyboard/ (8 slides, look A)
Each slide is 3 s; the 3D scene is drawn from the hf-seek time only. Snapshot each project with
  npx hyperframes snapshot ssm-patch/phase1/<project> --at 2.2,5.2,... --no-end
Public-safe: generic groups only; no account, host names, IDs, dates or exact times."""
import json, pathlib, shutil

HERE = pathlib.Path(__file__).resolve().parent
FILM = HERE.parent
SLIDE = 3.0

LOOK = {
  "diorama":   dict(font="'Avenir Next','Nunito',Helvetica,sans-serif", ink="#2f2a3a", soft="#5d566b", card="rgba(255,252,247,.90)",
                    border="0", radius="28px", shadow="0 18px 40px rgba(70,50,90,.18)", accent="#7b6cf6", hw=800, chip="#2f2a3a", chipt="#fffaf2"),
  "blueprint": dict(font="'Helvetica Neue',Helvetica,Arial,sans-serif", ink="#1d3a6b", soft="#4d638a", card="rgba(255,255,255,.94)",
                    border="2px solid #1d3a6b", radius="0px", shadow="none", accent="#ff7a1a", hw=700, chip="#1d3a6b", chipt="#ffffff"),
  "toy":       dict(font="'Arial Rounded MT Bold','Avenir Next',Helvetica,sans-serif", ink="#1b1b2f", soft="#35354f", card="#ffffff",
                    border="5px solid #1b1b2f", radius="20px", shadow="10px 10px 0 #1b1b2f", accent="#eb3b5a", hw=800, chip="#1b1b2f", chipt="#ffd23f"),
}
NAMES = {"diorama": "A · Pastel diorama", "blueprint": "B · Blueprint isometric", "toy": "C · Bold toy blocks"}

# (shot, kicker, title, sub, labels {anchor: text}, extra html, narration excerpt)
STORY = [
  ("hook", "AWS Factory · Amazon Linux 2023", "New security fixes arrive every week.", "How do running servers keep up — safely?",
   {}, "", "Every week, new security fixes arrive… so how does AWS Factory keep running servers patched, safely?"),
  ("roads", "Two roads", "Build fresh · Patch in place", "This film follows road ②",
   {"factory": "① Build fresh — a new image with the latest patches", "db": "② Patch in place — AWS Systems Manager Patch Manager"}, "",
   "Road one: build fresh… Road two: patch in place, with AWS Systems Manager Patch Manager."),
  ("groups", "Patch groups", "A patch group is a tag on each server", "Each group gets its own time slot",
   {"db": "Database group", "code": "Code-hosting group", "backup": "Backup host"}, "",
   "Patch Manager starts with a simple label: a tag on each server, called its patch group."),
  ("rules", "The rules · patch baseline", "Which updates, and when", "",
   {"sec": "Security updates → at once", "other": "Other updates → wait 7 days", "app": "Database & container engine → never in place"}, "",
   "Security updates are approved at once. Other updates wait seven days. Some packages are never patched in place."),
  ("night", "The weekend window", "Scan at night. Install at dawn.", "Each group in its own window · no automatic reboot",
   {}, "", "Every weekend night Patch Manager scans each server… early next morning each group installs in its own window."),
  ("trap", "The trap", "Scanned is not patched", "A policy patches only servers whose tag matches its group",
   {"lonely": "Tag matches no group → scanned, never installed"}, "",
   "A server with the wrong tag is still scanned — so it looks watched — but nothing is ever installed."),
  ("check", "The check", "Coverage is checked, not assumed", "",
   {}, "REPORT", "The daily report lists every server's patch result and flags any server with no patch data."),
  ("close", "", "Fresh images for new servers.<br>Patch Manager for running ones.", "And a daily check that no server is left behind.",
   {}, "", "Fresh images for new servers. Patch Manager for running ones. And a daily check that no server is left behind."),
]

REPORT = """<div class="report"><div class="rh">Patch coverage · every server</div>
<div class="rr"><span>Database group</span><b class="ok">scanned ✓</b><b class="ok">installed ✓</b></div>
<div class="rr"><span>Code-hosting group</span><b class="ok">scanned ✓</b><b class="ok">installed ✓</b></div>
<div class="rr"><span>Backup host</span><b class="ok">scanned ✓</b><b class="ok">installed ✓</b></div>
<div class="rr"><span>No patch data?</span><b class="warn">flagged in the daily report</b></div>
<div class="rf">New rules: one server first → then every group · the owner approves every production change</div></div>"""

def css(L):
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:#000}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:var(--font);color:var(--ink)}}
#gl{{position:absolute;inset:0;width:1920px;height:1080px}}
.slide{{position:absolute;inset:0;display:none;pointer-events:none}}
.card{{position:absolute;left:80px;top:70px;max-width:1300px;padding:34px 44px 36px;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}}
.kick{{font-size:26px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}}
.title{{font-size:64px;line-height:1.08;font-weight:var(--hw);letter-spacing:-.01em}}
.sub{{font-size:32px;line-height:1.3;color:var(--soft);margin-top:14px}}
.lab{{position:absolute;left:0;top:0;transform:translate(-50%,-100%);white-space:nowrap;font-size:30px;font-weight:700;padding:12px 22px;border-radius:999px;background:var(--chip);color:var(--chipt);box-shadow:0 8px 20px rgba(0,0,0,.18)}}
.lab:after{{content:"";position:absolute;left:50%;bottom:-10px;margin-left:-10px;border:10px solid transparent;border-bottom:0;border-top-color:var(--chip)}}
.say{{position:absolute;left:50%;bottom:44px;transform:translateX(-50%);width:1500px;text-align:center;font-size:30px;line-height:1.3;padding:16px 28px;border-radius:14px;background:rgba(20,18,30,.72);color:#fff}}
.say i{{opacity:.7;font-style:normal;font-size:22px;letter-spacing:.06em;display:block;margin-bottom:4px}}
.style-name{{position:absolute;right:70px;top:70px;font-size:34px;font-weight:800;padding:14px 26px;background:var(--chip);color:var(--chipt);border-radius:var(--radius)}}
.report{{position:absolute;right:80px;top:250px;width:860px;padding:34px 40px;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}}
.rh{{font-size:34px;font-weight:800;margin-bottom:18px}}
.rr{{display:flex;gap:18px;align-items:center;font-size:30px;padding:12px 0;border-top:1px solid rgba(0,0,0,.1)}}
.rr span{{flex:1}} .rr b{{font-size:26px;padding:6px 14px;border-radius:10px}}
.ok{{background:#dff5e7;color:#1e7a46}} .warn{{background:#fde8d7;color:#9a4a12}}
.rf{{font-size:26px;color:var(--soft);margin-top:18px;line-height:1.35}}
"""

def page(slides, title):
    """slides: list of dict(style, shot, kicker, title, sub, labels, extra, say, tag)"""
    dur = len(slides) * SLIDE
    looks = sorted({s["style"] for s in slides})
    L0 = LOOK[slides[0]["style"]]
    vars0 = ";".join(f"--{k}:{v}" for k, v in dict(font=L0["font"], ink=L0["ink"], soft=L0["soft"], card=L0["card"], border=L0["border"],
                                                    radius=L0["radius"], shadow=L0["shadow"], accent=L0["accent"], hw=L0["hw"], chip=L0["chip"], chipt=L0["chipt"]).items())
    html = []
    for i, s in enumerate(slides):
        L = LOOK[s["style"]]
        sv = ";".join(f"--{k}:{L[k]}" for k in ["font", "ink", "soft", "card", "border", "radius", "shadow", "accent", "hw", "chip", "chipt"])
        card = ""
        if s["title"]:
            card = f'<div class="card"{' style="top:auto;bottom:150px"' if s["shot"] == "groups" else ""}>{f"<div class=kick>{s["kicker"]}</div>" if s["kicker"] else ""}<div class="title">{s["title"]}</div>{f"<div class=sub>{s["sub"]}</div>" if s["sub"] else ""}</div>'
        labs = "".join(f'<div class="lab" data-anchor="{a}">{t}</div>' for a, t in s["labels"].items())
        say = f'<div class="say"><i>{s["tag"]}</i>{s["say"]}</div>' if s["say"] else ""
        extra = REPORT if s["extra"] == "REPORT" else s["extra"]
        html.append(f'<div class="slide" id="sl{i}" style="{sv}">{card}{extra}{labs}{say}</div>')
    plan = [{"style": s["style"], "shot": s["shot"]} for s in slides]
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<script type="importmap">{{"imports":{{"three":"./lib/three/three.module.js","three/addons/":"./lib/three/addons/"}}}}</script>
<style>:root{{{vars0}}}{css(L0)}</style>
<script>
  // Register readiness and the seek listener synchronously; the module fills them in.
  window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
  window.__hf.buildReady.world = new Promise((res) => (window.__worldReady = res));
  window.__lastSeek = 0;
  window.addEventListener("hf-seek", (e) => {{ window.__lastSeek = e.detail.time; if (window.__renderAt) window.__renderAt(e.detail.time); }});
</script>
</head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
<canvas id="gl" width="1920" height="1080"></canvas>
{"".join(html)}
</div>
<script type="module">
import * as THREE from "three";
import {{ buildWorld }} from "./world.js";
const PLAN = {json.dumps(plan)};
const SLIDE = {SLIDE};
const renderer = new THREE.WebGLRenderer({{ canvas: document.getElementById("gl"), antialias: true, preserveDrawingBuffer: true }});
renderer.setPixelRatio(1); renderer.setSize(1920, 1080, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const worlds = {{}};
for (const s of {json.dumps(looks)}) worlds[s] = buildWorld(s);
const slides = [...document.querySelectorAll(".slide")];
const v = new THREE.Vector3();
function renderAt(t) {{
  const i = Math.min(PLAN.length - 1, Math.max(0, Math.floor(t / SLIDE)));
  const p = (t - i * SLIDE) / SLIDE;
  const W = worlds[PLAN[i].style];
  W.set(PLAN[i].shot, p, t);
  renderer.toneMapping = PLAN[i].style === "blueprint" ? THREE.NoToneMapping : THREE.ACESFilmicToneMapping;
  renderer.render(W.scene, W.camera);
  slides.forEach((el, k) => (el.style.display = k === i ? "block" : "none"));
  for (const lab of slides[i].querySelectorAll(".lab")) {{
    const a = W.anchors[lab.dataset.anchor]; if (!a) continue;
    v.copy(a); if (lab.dataset.anchor.length <= 6 && ["sec","other","app"].includes(lab.dataset.anchor)) v.y += 0.7;
    v.project(W.camera);
    const half = lab.offsetWidth / 2 + 40;
    lab.style.left = Math.min(1920 - half, Math.max(half, (v.x + 1) / 2 * 1920)).toFixed(1) + "px";
    lab.style.top = ((1 - v.y) / 2 * 1080 - 14).toFixed(1) + "px";
  }}
}}
for (const s in worlds) await renderer.compileAsync(worlds[s].scene, worlds[s].camera);
for (const s in worlds) {{ worlds[s].set("hook", 0, 0); renderer.render(worlds[s].scene, worlds[s].camera); }}
const px = new Uint8Array(4); const gl = renderer.getContext(); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
window.__renderAt = renderAt;
renderAt(window.__lastSeek || 0);
window.__worldReady();
</script>
</body></html>
"""

def project(name, slides, title):
    d = HERE / name
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
    (d / "index.html").write_text(page(slides, title))
    shutil.copy(FILM / "src" / "world.js", d / "world.js")
    shutil.copytree(FILM / "lib", d / "lib")
    (d / "hyperframes.json").write_text(json.dumps({"name": f"ssm-patch-{name}"}, indent=1))
    return d

def main():
    styles = []
    for st in ["diorama", "blueprint", "toy"]:
        for k in (1, 3):  # the two key frames: two roads, the rules gate
            shot, kick, title, sub, labels, extra, say = STORY[k]
            styles.append(dict(style=st, shot=shot, kicker=NAMES[st], title=title, sub="", labels=labels, extra="", say="", tag=""))
    project("styles", styles, "Patching film · style options")
    board = []
    for n, (shot, kick, title, sub, labels, extra, say) in enumerate(STORY, 1):
        board.append(dict(style="diorama", shot=shot, kicker=kick, title=title, sub=sub, labels=labels, extra=extra, say=say, tag=f"SLIDE {n} · NARRATION"))
    project("storyboard", board, "Patching film · storyboard")
    print("times styles:", ",".join(f"{i*SLIDE+2.2:g}" for i in range(len(styles))))
    print("times board:", ",".join(f"{i*SLIDE+2.2:g}" for i in range(len(board))))

if __name__ == "__main__":
    main()
