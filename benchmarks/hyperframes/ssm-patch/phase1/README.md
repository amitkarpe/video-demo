# Phase 1 review pack — Patching Running Servers in AWS Factory

**What this is:** the storyboard for review, before full production (Issue #35). Nothing here is the final film.

## Look at these (pictures first)
1. **`style-options.jpg`**: the same 3D world and the same two frames ("two roads" and "the rules gate") in three Three.js looks:
   - **A · Pastel diorama:** soft pastel miniature with rounded "clay" edges and soft shadows. Closest to the clay diorama you picked earlier. **Recommended.**
   - **B · Blueprint isometric:** white blocks with navy outlines on a grid and one orange accent. Technical and calm.
   - **C · Bold toy blocks:** saturated primary colours with a hard sun. Playful and loud.
2. **`storyboard.jpg`**: all 8 slides in look A, each with its narration line.
3. **`voice-sample.m4a`**: the narration voice (OpenAI `gpt-realtime-2.1`, `marin`), 9.8 s, line s06.

## Slides and narration (full text in `../script.json`; about 2.5 minutes)
| # | Slide | Narration (gist) |
|---|---|---|
| 1 | New security fixes arrive every week | How do running servers keep up, safely? |
| 2 | Two roads | Build fresh images, or patch running servers in place with Patch Manager |
| 3 | Patch groups | A tag on each server: database group, code-hosting group, backup host |
| 4 | The rules (patch baseline) | Security at once · other updates after 7 days · database and container engine never in place |
| 5 | The weekend window | Scan at night, install at dawn, each group in its own window, no automatic reboot |
| 6 | The trap | A wrong tag means scanned, never installed. **Scanned is not patched.** |
| 7 | The check | Reports list every server's patch result and flag "no patch data"; new rules go to one server first; the owner approves |
| 8 | Close | Fresh images for new servers. Patch Manager for running ones. A daily check that no server is left behind. |

## In Phase 2, the world moves
- The camera glides across one continuous 3D island; there are no slide cuts:
  - image blocks ride the factory belt
  - update crates meet the rules gate (green passes, blue waits on the 7-day shelf, red hits the barrier)
  - the sky turns to night and a scan ring sweeps the groups
  - status lights turn from amber to green at dawn
  - the lonely server's red halo pulses
- The narration drives every move. Captions are burned in, with a light score.

## Public-safe
Generic groups only: no account, host names, IDs, schedule times, dates or patch counts. `../CLAIMS.md` maps each statement to the private source, with accuracy notes.

## Please reply
Pick a look (A, B or C) and give per-slide notes if any (**keep**, **change: …** or **drop**). "Go" means look A and the slides as drafted.

## Rebuild (no paid API)
```bash
python3 phase1/make_phase1.py
npx hyperframes snapshot ssm-patch/phase1/styles --at 2.2,5.2,8.2,11.2,14.2,17.2 --no-end -o ssm-patch/phase1/_snap/styles
npx hyperframes snapshot ssm-patch/phase1/storyboard --at 2.2,5.2,8.2,11.2,14.2,17.2,20.2,23.2 --no-end -o ssm-patch/phase1/_snap/storyboard
python phase1/make_sheets.py   # needs Pillow
```

**Phase 1 spend:** USD 0.0145 (one voice line). Images: none; every frame is Three.js code rendered by HyperFrames.
