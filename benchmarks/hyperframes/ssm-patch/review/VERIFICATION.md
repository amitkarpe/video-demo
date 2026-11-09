# Verification and QA record — "Patching Running Servers in AWS Factory" (revision 2)

**OWNER ACCEPTANCE:** Amit Karpe replied "Accept the film" on 9 Nov 2026 for revision 2 (`out/ssm-patch.mp4`, sha256 `d5c40f5e…debbb34f9`). Whether the owner listened at 1× is not recorded here.

**VERIFIED** means measured here on the final file. **NOT_VERIFIED** means not done or not possible here. A mechanical pass is not owner acceptance.

## 1. Identity and workflow
- **Output:**
  - Repository: `amitkarpe/video-demo` (public).
  - Branch: `feat/ssm-patch-film`.
  - Folder: `benchmarks/hyperframes/ssm-patch/`.
  - Owning issue #35, draft PR #36.
- **Source:** `amitkarpe/aws-factory` @ `0808975` and its patching issue record (private, read-only). No AWS action and no source write.
- **History:**
  - **Phase 1:** 3 looks and an 8-slide storyboard. The owner chose look C ("Create C · Go · Make it generic · all are working").
  - **Revision 1:** 2:37 (commit `d60a82c`). Not accepted.
  - **Owner review of revision 1:**
    - use the real three families (GitLab, MongoDB, CloudOS workspace on ECS)
    - make them more colourful and more distinct, with more moving parts
    - explain a little more: scan → install only if needed → reboot only in the planned downtime window
  - **Option 2 ("Deepen"):** chosen by the owner from a three-option table. This file records that revision.
- **Agent:** `claude-opus-5-5`. Effort setting UNAVAILABLE.
- **Public-output rule:** generic families only. No account, host names, IDs, schedule times, dates, patch counts, or current production state. Everything is presented as the working flow (`CLAIMS.md`: OWNER DIRECTION).

## 2. What changed from revision 1
| Weakness in revision 1 | Revision 2 |
|---|---|
| Wrong, nameless groups (database / code-hosting / backup host) | The real families: **GitLab**, **MongoDB**, **CloudOS workspace (ECS)** |
| All groups looked alike (white racks) | Each family has its own building and colour: GitLab orange towers with a pulsing pipeline; MongoDB green vault members with turning wheels and a replica ring; CloudOS blue worker nodes with containers and a crane swapping a container |
| Few moving parts | Chimney smoke; a base image splitting into three family images that fly to their pads; servers pop in; flags rise; a night scan beam; red "missing" cubes; install drops; group clocks; a reboot sign; nodes going dark and coming back |
| No AMI → patch-group link | New chapter: one hardened base image → three families → each server's tag = its patch group |
| No decision flow | New chapter with a 6-step strip: scan → missing? → install in the group's window → reboot needed? → downtime window → compliant. MongoDB shows "nothing missing"; GitLab shows "installed, no reboot"; CloudOS shows "new kernel → reboot in the downtime window" |

## 3. Final file (VERIFIED)
| Check | Method | Observed | Disposition |
|---|---|---|---|
| Container/codec | `ffprobe` on `out/ssm-patch.mp4`, sha256 `d5c40f5ed61218ab85a35964de06db293dbac5826ee91f34283f772debbb34f9` | H.264 1920×1080 30 fps; AAC; 180.323 s; 50,669,280 bytes | PASS |
| Full decode | `ffmpeg -v error … -f null -` | exit 0 | PASS |
| Full-duration playback | Built-in Chromium `<video>`, unmuted, `playbackRate` 4, in-page SHA-256 | see §3a | see §3a |
| Motion | `mpdecimate` | 5,404 of ≈ 5,410 frames distinct | PASS |
| Loudness | `ebur128=peak=true` | −16.0 LUFS, LRA 2.9 LU, peak −1.5 dBFS | PASS |
| Lint | `npx hyperframes check` | 0 errors. Contrast fixed (family labels, flow strip). Remaining warnings: dead stretches seen only in the HTML layer (the WebGL canvas moves throughout, per the motion row) | Accepted |
| Captions | `captions.srt` | 42 cues, minimum 1.72 s on screen | PASS |
| 720p readability | `review/qa/*.jpg` (one frame per line), vision QA | Essential text ≥ 28 px | PASS |
| Mix determinism | Rebuilt twice | `assets/mix.wav` sha256 `1560f259…`, identical across picture-only fixes, so the transcription below applies to the final file | PASS |

### 3a. Playback
**PASS at 4× speed.** `played` = [[0, 180.323]], `ended=true`, `error=null`, no error or stall events, unmuted, 45.2 s of real time. The browser fetched the file over local HTTP and its in-page SHA-256 matched the final hash. This is not a 1× human viewing.

## 4. Self-review before QA (fixed)
- **Lint contrast:**
  - Family labels were darkened: GitLab `#c94f12`, MongoDB `#0f8a43`, ECS `#1f6fd6`.
  - The flow strip got a dark backing with yellow arrows.
  - The green "Compliant" step was darkened.
- **Reboot beat:**
  - The reboot sign was hidden behind the flow strip and its label; it was moved beside the ECS group.
  - The ECS camera was reframed so the nodes are seen going dark and coming back.
- **Trap shot:**
  - The crane blocked the view; the camera now looks from behind the island.
  - A scan beam was added over the lonely server, so it is visibly "scanned".
- **Overlap:** the trap label overlapped the "Scanned is not patched" stamp; the label now leaves before the stamp.

## 5. OpenAI QA (advice, with dispositions)
**Final-mix transcription** (`gpt-transcribe`, `review/qa-transcribe.json`): WER **0.48%** (2 of 421 words). Both differences are notation: "CloudOS" was written as "Cloud OS". No substantive differences.

**Vision review** (`gpt-5.5`, 26 frames, `review/qa-vision.json`, raw reply in `review/qa-vision.raw.txt`): 9 findings. A first call returned a truncated reply that could not be parsed. The tool now saves the raw reply before parsing and allows a longer answer; that call is in the spend.

| Finding (severity) | Disposition |
|---|---|
| The report shows MongoDB as "installed ✓", but MongoDB is the "nothing missing" example (high, 2 frames) | **Accepted.** The MongoDB row now reads "nothing missing ✓" |
| The CloudOS reboot label is long over a busy area (low) | **Accepted:** "CloudOS: new kernel → reboot in the downtime window" |
| "Daily and weekly reports" and "daily check" expose a cadence (medium, 2 frames) | **Rejected.** These are report names and the source's own check, not a patch schedule; no times or days of a production run are shown |
| The flow strip is dense at 720p (low, 4 frames) | **Rejected.** The step text meets the 28 px floor; the highlighted step is the reading cue, and narration names each step |

## 6. Narration and sound — **AUDIBLE_REVIEW=NOT_VERIFIED**
- All 26 lines were re-voiced, and every take was word-exact against the script (provider transcript).
- No human has listened. Please check:
  - the pronunciation of "GitLab", "MongoDB", "CloudOS" and "ECS"
  - pace
  - whether the effects (scan ticks, install thunks, reboot chime) ever compete with speech

## 7. Spend (OpenAI; settled from returned usage)
| Endpoint · model | Requests | USD |
|---|---:|---:|
| Realtime `gpt-realtime-2.1`, voice `marin` (Phase 1 sample, revision 1: 23, revision 2: 26) | 49 | 0.4872 |
| `audio/transcriptions` · `gpt-transcribe` (one per revision) | 2 | 0.0254 |
| `responses` · `gpt-5.5` vision QA (revision 1: 1; revision 2: 2, one unparseable) | 3 | 0.9865 |
| **Total for the film** | **54** | **1.4991** |

Revision 2 alone cost USD 1.03. All requests ACK. No images were generated.

## 8. Time
- Revision 2: from the owner's "2" to the verified file, about 75 minutes.
- Renders: about 62 s each for a full 3-minute delivery render, with a hardware GPU.
