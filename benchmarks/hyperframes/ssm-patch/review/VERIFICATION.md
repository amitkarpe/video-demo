# Verification and QA record — "Patching Running Servers in AWS Factory"

**VERIFIED** means measured here on the final file. **NOT_VERIFIED** means not done or not possible here. A mechanical pass is not owner acceptance.

## 1. Identity and workflow
- **Output:**
  - Repository: `amitkarpe/video-demo` (public).
  - Branch: `feat/ssm-patch-film`, from `feat/10-engineering-deep-dive` (`995e828`).
  - Folder: `benchmarks/hyperframes/ssm-patch/`.
  - Owning issue #35, draft PR #36.
- **Source:** `amitkarpe/aws-factory` @ `0808975` and its patching issue record (private, read-only). No AWS action and no source write.
- **Workflow:** two phases.
  - Phase 1 delivered 3 Three.js looks and an 8-slide storyboard.
  - The owner replied "Create C · Go · Make it generic · Consider all are already working".
  - Phase 2 is this film in look C (bold toy blocks), presented as the working flow (`CLAIMS.md`: OWNER DIRECTION).
- **Agent:** `claude-opus-5-5`. Effort setting UNAVAILABLE.
- **Public-output rule:** generic groups only. No account, host names, IDs, schedule times, dates, patch counts, or current production state.

## 2. Final file (VERIFIED)
| Check | Method | Observed | Disposition |
|---|---|---|---|
| Container/codec | `ffprobe` on `out/ssm-patch.mp4`, sha256 `ac11735196265d1f4de3a9343529db2d4292ea457f4af8bf3efaf4a0bbccd91a` | H.264 1920×1080 30 fps; AAC; 157.167 s; 30,212,244 bytes | PASS |
| Full decode | `ffmpeg -v error … -f null -` | exit 0 | PASS |
| Full-duration playback | Built-in Chromium `<video>`, unmuted, `playbackRate` 4, in-page SHA-256 | Hash identical; `played` = [[0, 157.167]]; `ended=true`; `error=null`; no stall or error events; 39.4 s wall | PASS at 4× (not a 1× human viewing) |
| Motion | `mpdecimate` | 4,638 of ≈ 4,715 frames distinct (continuous 3D camera) | PASS |
| Loudness | `ebur128=peak=true` | −16.0 LUFS, LRA 3.6 LU, peak −1.5 dBFS | PASS |
| Lint | `npx hyperframes check` | 0 errors. Warnings: dead stretches seen only in the HTML layer (the WebGL canvas moves throughout, per the motion row) | Accepted |
| Captions | `captions.srt` | 36 cues, ≤ 86 characters, minimum 1.75 s on screen | PASS |
| 720p readability | `review/qa/*.jpg` (one frame per line) and vision QA | Essential text ≥ 28 px | PASS |
| 3D determinism | The scene is a pure function of time through `hf-seek`; no clock, no RNG | Mix rebuilt byte-identical (`assets/mix.wav` sha256 `7a61c2b1…`). Frame-level repeat-seek identity was not measured | PASS (audio); video NOT_VERIFIED |

## 3. Self-review before QA (fixed)
- **Font:** a system font the renderer could not supply → bundled Nunito.
- **Text floor:** small text was raised to the 28 px floor.
- **Credits:** the credits were too short to read → tail 7 s.
- **Framing:**
  - The factory label clamped onto the title card.
  - Group and scan labels overlapped the cards. Labels now stay below the card band, and the camera targets were raised.
  - The night-shot counter was unreadable on dark sky → light pill.

## 4. OpenAI QA (advice, with dispositions)
**Final-mix transcription** (`gpt-transcribe`, `review/qa-transcribe.json`): WER **0.0%** (0 of 350 words). The final mix was rebuilt deterministically and is byte-identical.

**Vision review** (`gpt-5.5`, 23 frames of the prior candidate, `review/qa-vision.json`): 6 findings.

| Finding (severity) | Disposition |
|---|---|
| The report says "every server" but its rows read as groups (high, 2 frames) | **Accepted.** Rows are now "Database servers", "Code-hosting servers" and "Backup host" |
| The flag says only "daily report"; the source flags in both daily and weekly reports (medium) | **Accepted:** "flagged in the reports" |
| The "No patch data" row is low contrast (medium) | **Rejected.** The frame was taken mid fade-in; the row is full contrast 0.3 s later (see `t0139.0-s22.jpg`) |
| Edge-cropped objects in the factory and gate shots (low, 3 frames) | **Rejected.** The camera moves continuously through one 3D world; partial objects at the frame edge are intended |

## 5. Narration and sound — **AUDIBLE_REVIEW=NOT_VERIFIED**
- No human has listened. Please check:
  - pace
  - the pronunciation of "AWS" and "Patch Manager"
  - whether the toy-box score and the effects (crate thunks, scan ticks, the stamp) ever compete with speech

## 6. Spend (OpenAI; settled from returned usage)
| Endpoint · model | Requests | USD |
|---|---:|---:|
| Realtime `gpt-realtime-2.1`, voice `marin` (23 lines, 1 in Phase 1) | 23 | 0.2251 |
| `audio/transcriptions` · `gpt-transcribe` | 1 | 0.0118 |
| `responses` · `gpt-5.5` (vision QA) | 1 | 0.2275 |
| **Total** | **25** | **0.4645** |

All 25 requests ACK, with no retries. Images: none; the whole world is Three.js code.

## 7. Time
- Phase 1: about 21:55–22:12 SGT on 9 Nov 2026.
- Phase 2: "Go" to verified file, about 25 minutes.
- Revisions: 4 delivery renders of about 50 s each.
