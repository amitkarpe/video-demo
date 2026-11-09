#!/usr/bin/env python3
"""Phase 1 storyboard for the CIS hardening film: the same slides in three native HyperFrames looks.
  python3 phase1/make_slides.py      -> phase1/<style>/index.html (+ assets), one slide every 3 s
Looks copy the native examples' tokens:
  swiss-grid    #f2f2f2 grid paper, navy #0a1e3d, gold #d4a017, Helvetica 900/300, hard offset shadow
  warm-grain    cream #f5f0e0, green #3b5e3a, amber #cc8832, terracotta #c45d3e, round shapes
  decision-tree white, pastel nodes (#a8d8f0 #c2e8a0 #f5c5a3), #333 connectors, soft shadow
Public-safe: no control numbers, IDs, dates or credential details."""
import pathlib, shutil
HERE = pathlib.Path(__file__).resolve().parent
GSAP = HERE.parents[1] / "node_modules" / "gsap" / "dist" / "gsap.min.js"
SLIDE = 3.0

THEMES = {
  "swiss-grid": dict(bg="#f2f2f2", ink="#0a1e3d", soft="#46546e", c1="#0a1e3d", c1t="#ffffff", c2="#d4a017", c2t="#0a1e3d",
                     c3="#ffffff", c3t="#0a1e3d", line="#0a1e3d", kick="#0a1e3d", font='"Helvetica Neue",Helvetica,Arial,sans-serif', hw=900, lw=300,
                     radius="0px", shadow="20px 20px 0 rgba(10,30,61,.12)", card="#ffffff", stop="#b3261e", ok="#1e7a46",
                     deco='<img class="abs" src="assets/grid.svg" style="left:0;top:0;width:1920px;height:1080px" alt="">', caps=True),
  "warm-grain": dict(bg="#f5f0e0", ink="#2d2a24", soft="#6b6253", c1="#3b5e3a", c1t="#fff8ea", c2="#cc8832", c2t="#2d2a24",
                     c3="#c45d3e", c3t="#fff8ea", line="#2d2a24", kick="#3b5e3a", font='"Avenir Next","Outfit",Helvetica,sans-serif', hw=700, lw=400,
                     radius="40px", shadow="0 18px 40px rgba(60,40,10,.16)", card="#fffaf0", stop="#c45d3e", ok="#3b5e3a",
                     deco='<div class="abs" style="inset:0;background:radial-gradient(#00000010 1px,transparent 1.2px) 0 0/7px 7px"></div>', caps=False),
  "decision-tree": dict(bg="#ffffff", ink="#1f1f1f", soft="#5c5c5c", c1="#a8d8f0", c1t="#123247", c2="#c2e8a0", c2t="#20380f",
                        c3="#f5c5a3", c3t="#4a2410", line="#333333", kick="#1f1f1f", font='"Helvetica Neue",Inter,Arial,sans-serif', hw=600, lw=500,
                        radius="12px", shadow="0 4px 12px rgba(0,0,0,.1)", card="#ffffff", stop="#d64545", ok="#3c8a2e",
                        deco='<div class="abs" style="inset:0;background:radial-gradient(#00000014 1.4px,transparent 1.6px) 0 0/32px 32px"></div>', caps=False),
}

def slides(t):
    U = (lambda s: s.upper()) if t["caps"] else (lambda s: s)
    sq = "".join(f'<i style="left:{(k % 27) * 40}px;top:{(k // 27) * 40}px"></i>' for k in range(243))
    return [
    # 1 hook
    f'''<div class="kick">{U("AWS Factory · Amazon Linux 2023")}</div>
    <div class="title" style="top:200px">243 security checks.<br>Do we fix them all?</div>
    <div class="sub" style="top:470px">The CIS Benchmark · Level 1 and Level 2</div>
    <div class="sq" style="left:820px;top:560px">{sq}</div>''',
    # 2 what is CIS
    f'''<div class="kick">{U("What is CIS?")}</div>
    <div class="title" style="top:180px;font-size:76px">A public checklist for<br>hardening servers</div>
    <div class="card" style="left:120px;top:470px;width:780px"><div class="tag" style="background:var(--c1);color:var(--c1t)">LEVEL 1</div><div class="h">Essential</div><div class="b">Safe defaults almost every server should have.</div></div>
    <div class="card" style="left:1000px;top:470px;width:780px"><div class="tag" style="background:var(--c2);color:var(--c2t)">LEVEL 2</div><div class="h">Defence in depth</div><div class="b">Stricter settings for sensitive systems. Some cost more to apply.</div></div>
    <div class="sub" style="top:850px">Think of it as a building-safety code — for servers.</div>''',
    # 3 where hardening happens
    f'''<div class="kick">{U("Where hardening happens")}</div>
    <div class="title" style="top:170px;font-size:62px">One factory line, rebuilt on every new image or patch</div>
    <div class="node" style="left:110px;top:520px;background:var(--card)">Parent image<div class="nb">GovTech</div></div>
    <div class="arrow" style="left:440px;top:580px;width:120px"></div>
    <div class="node big" style="left:570px;top:470px;background:var(--c2);color:var(--c2t)">Base image<div class="nb">+ CIS fixes · agents · patches</div></div>
    <div class="arrow" style="left:1010px;top:580px;width:120px"></div>
    <div class="node" style="left:1140px;top:380px;background:var(--card)">ECS image</div>
    <div class="node" style="left:1140px;top:540px;background:var(--card)">MongoDB image</div>
    <div class="node" style="left:1140px;top:700px;background:var(--card)">GitLab image</div>
    <div class="arrow" style="left:1390px;top:600px;width:110px"></div>
    <div class="node" style="left:1520px;top:540px;background:var(--c1);color:var(--c1t)">Test<br>&amp; share</div>''',
    # 4 three buckets (key frame)
    f'''<div class="kick">{U("Three buckets")}</div>
    <div class="title" style="top:150px;font-size:66px">Every control lands in one of three buckets</div>
    <div class="bk" style="left:110px;background:var(--c1);color:var(--c1t)"><div class="bh">Hardened upstream</div><div class="bs">by the GovTech parent image</div><div class="bl">Many controls arrive already set.</div></div>
    <div class="bk" style="left:700px;background:var(--c2);color:var(--c2t)"><div class="bh">Fixed by us</div><div class="bs">in the base image</div><div class="bl">• login lockout and password rules<br>• file and log permissions<br>• audit rules<br>• unused network off<br>• signed package sources</div></div>
    <div class="bk" style="left:1290px;background:var(--c3);color:var(--c3t);border:4px dashed var(--line)"><div class="bh">Accepted risk</div><div class="bs">approved by the owner</div><div class="bl">• separate disk partitions (×5)<br>• one file-permission check<br><b>6 controls, listed in code</b></div></div>''',
    # 5 why accept
    f'''<div class="kick">{U("Why accept a risk?")}</div>
    <div class="title" style="top:170px;font-size:70px">Some fixes cost more<br>than the risk they remove</div>
    <div class="card" style="left:120px;top:520px;width:820px"><div class="h">Separate disk partitions</div><div class="b">Would mean a new disk layout for every image — and moving every running workload.</div><div class="pill" style="background:var(--c3);color:var(--c3t)">high cost · high complexity</div></div>
    <div class="card" style="left:1000px;top:520px;width:800px"><div class="h">The trade-off is written down</div><div class="b">Each accepted control is named in the factory's code, with the owner's approval.</div><div class="pill" style="background:var(--c1);color:var(--c1t)">visible · reviewable</div></div>''',
    # 6 the gate (key frame)
    f'''<div class="kick">{U("The release gate")}</div>
    <div class="title" style="top:150px;font-size:66px">Every release is scanned before it ships</div>
    <div class="node" style="left:90px;top:470px;background:var(--card)">Build</div>
    <div class="arrow" style="left:330px;top:530px;width:70px"></div>
    <div class="node" style="left:410px;top:470px;background:var(--card)">Reboot</div>
    <div class="arrow" style="left:650px;top:530px;width:70px"></div>
    <div class="node big" style="left:730px;top:430px;background:var(--c2);color:var(--c2t)">Scan<div class="nb">CIS Level 2 + HCR checks</div></div>
    <div class="arrow" style="left:1150px;top:530px;width:70px"></div>
    <div class="node" style="left:1230px;top:470px;width:290px;background:var(--card)">Compare with the approved list</div>
    <div class="out" style="left:1580px;top:330px;width:280px;border-color:var(--stop);color:var(--stop)">New failure<br><b>STOP</b></div>
    <div class="out" style="left:1580px;top:640px;width:280px;border-color:var(--ok);color:var(--ok)">Only approved<br><b>SHIP</b></div>
    <div class="sub" style="top:860px">Scanner results are never relabelled to look green.</div>''',
    # 7 close
    f'''<div class="title" style="top:300px;font-size:92px;text-align:center;left:0;width:1920px">Fix what we can.<br>Accept what we must.</div>
    <div class="sub" style="top:600px;text-align:center;left:0;width:1920px">On purpose · in writing · re-checked every release</div>''',
    ]

CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{width:1920px;height:1080px;overflow:hidden;background:var(--bg)}
#stage{position:absolute;inset:0;background:var(--bg);font-family:var(--font);color:var(--ink)}
.abs{position:absolute}.slide{position:absolute;inset:0;opacity:0}
.kick{position:absolute;left:120px;top:90px;font:var(--hw) 30px var(--font);letter-spacing:3px;color:var(--kick);border-left:10px solid var(--c2);padding-left:18px}
.title{position:absolute;left:120px;width:1700px;font:var(--hw) 84px/1.08 var(--font);color:var(--ink)}
.sub{position:absolute;left:120px;width:1700px;font:var(--lw) 40px/1.3 var(--font);color:var(--soft)}
.sq{position:absolute;width:1080px;height:360px}.sq i{position:absolute;width:30px;height:30px;background:var(--c1);border-radius:calc(var(--radius) / 5)}
.sq i:nth-child(3n){background:var(--c2)}.sq i:nth-child(41n){background:var(--c3);outline:2px dashed var(--line)}
.card{position:absolute;padding:34px 40px 40px;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);border:2px solid #00000012}
.card .h{font:var(--hw) 44px/1.15 var(--font)}.card .b{margin-top:14px;font:var(--lw) 32px/1.35 var(--font);color:var(--soft)}
.tag,.pill{display:inline-block;margin-bottom:16px;padding:6px 16px;border-radius:999px;font:var(--hw) 22px var(--font);letter-spacing:2px}.pill{margin:22px 0 0}
.node{position:absolute;width:230px;min-height:120px;padding:24px;border-radius:var(--radius);box-shadow:var(--shadow);border:3px solid var(--line);font:var(--hw) 34px/1.15 var(--font);text-align:center;display:flex;flex-direction:column;justify-content:center}
.node.big{width:420px;min-height:220px;font-size:44px}.nb{margin-top:8px;font:var(--lw) 24px/1.25 var(--font)}
.arrow{position:absolute;height:6px;background:var(--line)}.arrow:after{content:"";position:absolute;right:-6px;top:-11px;border:14px solid transparent;border-left:20px solid var(--line);border-right:0}
.bk{position:absolute;top:320px;width:520px;height:560px;padding:40px;border-radius:var(--radius);box-shadow:var(--shadow)}
.bh{font:var(--hw) 50px/1.1 var(--font)}.bs{margin-top:8px;font:var(--lw) 30px var(--font);opacity:.9}.bl{margin-top:34px;font:var(--lw) 31px/1.6 var(--font)}
.out{position:absolute;width:300px;padding:22px;border:6px solid;border-radius:var(--radius);background:var(--card);font:var(--lw) 30px/1.3 var(--font);text-align:center;box-shadow:var(--shadow)}.out b{font:var(--hw) 54px var(--font)}"""

GRID = '<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><rect width="1920" height="1080" fill="#F2F2F2"/>' + \
       "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1080" stroke="#0A1E3D" stroke-opacity="{.16 if x % 240 == 0 else .07}"/>' for x in range(0, 1921, 60)) + \
       "".join(f'<line x1="0" y1="{y}" x2="1920" y2="{y}" stroke="#0A1E3D" stroke-opacity="{.16 if y % 240 == 0 else .07}"/>' for y in range(0, 1081, 60)) + "</svg>"

for name, t in THEMES.items():
    out = HERE / name; (out / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(GSAP, out / "assets" / "gsap.min.js"); (out / "assets" / "grid.svg").write_text(GRID)
    S = slides(t); total = SLIDE * len(S)
    vars_ = ";".join(f"--{k}:{v}" for k, v in t.items() if k not in ("deco", "caps"))
    body = "\n".join(f'<div id="s{i}" class="slide">{s}</div>' for i, s in enumerate(S))
    js = "\n".join(f'tl.set("#s{i}",{{opacity:1}},{i * SLIDE});tl.set("#s{i}",{{opacity:0}},{(i + 1) * SLIDE - 0.001});' for i in range(len(S)))
    (out / "index.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080">
<title>CIS hardening — storyboard ({name})</title><script src="assets/gsap.min.js"></script><style>:root{{{vars_}}}{CSS}</style></head><body>
<div id="stage" class="clip" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080" data-track-index="0">
{t["deco"]}
{body}
</div>
<script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
{js}
tl.set({{}},{{}},{total});window.__timelines["main"]=tl;</script></body></html>''')
    print(name, len(S), "slides,", total, "s")
