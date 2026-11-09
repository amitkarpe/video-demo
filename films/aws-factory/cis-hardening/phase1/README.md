# Phase 1 review pack — CIS Hardening in AWS Factory

**What this is:** the storyboard for review, before any full production (Issue #32). Nothing here is the final film.

## Look at these (pictures first)
1. **`style-options.jpg`**: the same two key frames ("three buckets" and "release gate") in three **native HyperFrames styles**:
   - **A · Swiss Grid**: navy and gold on grid paper; structured and technical. **Recommended.**
   - **B · Warm Grain**: cream paper, green, amber and terracotta; friendly and calm.
   - **C · Decision Tree**: white with pastel nodes; diagram-led.
2. **`storyboard-swiss-grid.jpg`**: all 7 slides in the recommended style. The other two styles are in `storyboard-warm-grain.jpg` and `storyboard-decision-tree.jpg`.
3. **`voice-sample.m4a`**: the narration voice (OpenAI `gpt-realtime-2.1`, `marin`), 8 s, line s02.

## Slides and narration (full text in `../script.json`; about 2.5 minutes)
| # | Slide | Narration (gist) |
|---|---|---|
| 1 | 243 security checks. Do we fix them all? | Hundreds of settings; CIS lists 243; the honest answer is no, by decision |
| 2 | What is CIS | A public hardening checklist: Level 1 essentials, Level 2 stricter; a building-safety code for servers |
| 3 | Where hardening happens | GovTech parent → base image → ECS, MongoDB, GitLab → test and share; reruns on new images or patches |
| 4 | Three buckets | Hardened upstream · fixed by us · accepted risk with owner approval |
| 5 | Why accept a risk | Separate disk partitions mean a new disk layout everywhere; the trade-off is written in code |
| 6 | The release gate | Build → reboot → scan → compare with the approved list → STOP or SHIP; labels never relabelled |
| 7 | Close | Fix what we can. Accept what we must — on purpose, in writing, re-checked every release |

## In Phase 2, the slides become motion
- Each slide becomes an animated scene in the chosen style:
  - the 243 squares sort themselves into the three buckets
  - the parts move along the factory line
  - the gate lights STOP or SHIP
- Optional: small clay-diorama illustrations for the plain-language moments (the building-safety analogy, the factory line).

## Please reply per slide
Use **keep**, **change: …** or **drop**, plus the style (A, B or C) and whether you want clay spot illustrations. One overall verdict is enough to start Phase 2.

## Rebuild (no paid API)
```bash
python3 phase1/make_slides.py
for s in swiss-grid warm-grain decision-tree; do npx hyperframes snapshot phase1/$s --at 1.5,4.5,7.5,10.5,13.5,16.5,19.5 --no-end -o phase1/_snap/$s; done
```

**Phase 1 spend:** USD 0.013 (one voice line). Images: none; every frame is code rendered by HyperFrames.
