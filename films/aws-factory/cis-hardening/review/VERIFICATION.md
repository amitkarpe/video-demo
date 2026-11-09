# Verification and QA record — "CIS Hardening in AWS Factory"

**VERIFIED** = measured here on the final file. **NOT_VERIFIED / NOT_ASSESSED** = not done or not possible here. A mechanical pass is not owner acceptance.

## 1. Identity and workflow
- **Output:** `amitkarpe/video-demo` (public), branch `feat/cis-hardening-film` from `feat/10-engineering-deep-dive` (`995e828`). Folder `benchmarks/hyperframes/cis-hardening/`. Owning issue #32, draft PR #33.
- **Source:** `amitkarpe/aws-factory` @ `080897512f33ab8c375995413add7ee8d882d013` (private). Read from a scratch clone with the push URL disabled. No AWS action and no source write.
- **Workflow:** two phases. Phase 1 delivered three native styles and a 7-slide storyboard. Amit replied "Go", accepting the recommended style A (Swiss Grid) and the slides as drafted. Phase 2 is this film.
- **Agent:** `claude-opus-5-5`. Effort setting UNAVAILABLE.
- **Public-output rule:** no CIS control numbers, no account, instance or image IDs, no dates, no credential details. One further accepted risk, a credential setting, is deliberately left out. A pattern scan of the committed files found none of these.

## 2. Final file (VERIFIED)

| Check | Artifact | Method | Observed | Disposition |
|---|---|---|---|---|
| Container/codec | `out/cis-hardening.mp4` sha256 `46830a9487c7d22780ea3ba9d36c3eb0a8a66edea436ccd7b4fe80a9cd5c6c16` | `ffprobe` | H.264 1920×1080 30 fps; AAC 48 kHz stereo; 156.327 s; 25,337,104 bytes | PASS |
| Full decode | same | `ffmpeg -v error -i … -f null -` | exit 0 | PASS |
| Full-duration playback | same (hashed in-page by the browser: identical) | Built-in Chromium `<video>`, unmuted, `playbackRate` 4 | see §2a | see §2a |
| Motion | same | `mpdecimate` | 2,544 of ≈ 4,690 frames distinct; lint reports no dead stretch | PASS |
| Loudness | same | `ebur128=peak=true` | −16.0 LUFS, LRA 3.4 LU, true peak −1.5 dBTP | PASS |
| Lint | `index.html` | `npx hyperframes check` | 0 errors; warnings: tag pills at 22 px (secondary), file length | Accepted (laptop 720p target; essential text ≥ 28 px or captioned) |
| Captions | `captions.srt` | parsed | 36 cues, ≤ 92 characters (two lines), minimum on screen 1.87 s, 0 overlaps; timed from post-edit clip lengths | PASS |
| 720p readability | `review/qa/*.jpg` (22 frames, one per line, plus one transition) | viewed at 1280×720, plus vision QA | essential text ≥ 28 px; captions ≈ 25 px at 720p | PASS |
| Keyframes | `keyframes/0[1-7]-*.png` | taken from the final file | — | — |

### 2a. Playback
**PASS at 4× speed.** `played` = [[0, 156.327]], `ended=true`, `error=null`, no error or stall events, unmuted, 40.3 s of real time. The browser fetched the file over local HTTP and its in-page SHA-256 matched the final hash. This is not a 1× human viewing.

## 3. Self-review before QA
- **Draft review found and fixed:**
  - Squares jumped because a bob animation used an absolute position.
  - Squares covered the bucket cards before sorting.
  - The gate illustration overlapped the STOP box.
  - The travelling marker landed on "SHIP".
  - The credits ran off the edge.
  - The hook headline touched the squares; the safety caption touched its illustration.
  - The "upstream" squares were invisible: navy on navy.
- **Lint-driven fixes:**
  - The square sorting used `left/top`; it now uses transforms.
  - Two hook lines overlapped.
  - Gold text was below 3:1 contrast.
  - There were six still stretches (now a slow grid drift and scene breathing).
  - One caption was too short to read.
- **Accuracy fixes before narration:**
  - "Every week" became "on every new parent image or new patches".
  - "Every control" became "every check the scanner can test", because some CIS controls need manual review.

## 4. OpenAI QA (advice, with dispositions)

**Final-mix transcription** (`gpt-transcribe`, `review/qa-transcribe.json`): raw WER 4.7% (17/363). All but one difference is notation: digits for spoken numbers, "HCR" for "H-C-R", US spelling. The one substantive difference: "ask" in "Five controls ask for…" was heard as "asked". It is flagged for human listening, and the meaning is unchanged.

**Vision review** (`gpt-5.5`, 22 frames of the prior candidate, `review/qa-vision.json`): 14 findings.

| Finding (severity) | Disposition |
|---|---|
| "Illustrative" note on the bucket counts missing or unreadable (high/medium, 3 frames) | **Accepted.** The note now shows from the moment the squares sort, at 28 px under the title |
| The clay gate overlapped the 06/06 counter (high, 3 frames) | **Accepted.** Illustration moved down |
| An unlabelled navy square in the gate flow (medium, 2 frames) | **Accepted.** It is now a labelled "RELEASE" chip that travels to SHIP |
| "one file-permission check" is vaguer than the claim (medium) | **Accepted:** "start-up file permissions ×1" |
| "5 × separate disk partition" singular (low) | **Accepted:** plural |
| Loop label small (low, 2 frames) | **Accepted.** 36 px in a bordered label |
| Lower panel crowds the captions (low) | **Accepted.** Raised 30 px |
| No chapter counter on the closing title (high) | **Rejected.** The close is not a chapter, so the counter is deliberately hidden there. The AI disclosure stays visible |

All fixes were verified on the next render. The audio mix is byte-identical across the picture-only fixes (`assets/mix.wav` sha256 `9c8ba0af…` before and after), so the transcription result applies to the final file.

## 5. Narration and sound — **AUDIBLE_REVIEW=NOT_VERIFIED**
- No human has listened. Please check:
  - pace (≈ 150 words per minute)
  - the pronunciation of CIS, GovTech, MongoDB, HCR
  - line s15 "ask for"
  - whether the light score and effects ever compete with speech

## 6. Comprehension (self-check, not an audience test)
- **What happened?** AWS Factory hardens Amazon Linux 2023 against the CIS benchmark in one base image. Checks are hardened upstream, fixed by us, or accepted with owner approval.
- **Why does it work?** The six accepted exceptions are named in code, and every release is scanned after a reboot. Anything else stops the release.
- **What is limited?**
  - Some controls need manual review and are outside the scanner.
  - The accepted risks are owner decisions, not security-authority approvals.
  - The first two buckets' square counts are illustrative.

## 7. Spend (OpenAI, this film; settled from returned usage, estimates)

| Endpoint · model | Requests | USD |
|---|---:|---:|
| Realtime `gpt-realtime-2.1`, voice `marin` (22 lines; 1 in Phase 1) | 22 | 0.2308 |
| `images/generations` · `gpt-image-2.6-sunburst` (3 clay illustrations) | 3 | 0.1369 |
| `audio/transcriptions` · `gpt-transcribe` (final mix) | 1 | 0.0118 |
| `responses` · `gpt-5.5` (vision QA, 22 frames) | 1 | 0.2275 |
| **Total** | **27** | **0.6069** |

All 27 requests ACK, with no retries. The owner set no budget limit; the ledger's working cap was USD 50.

## 8. Usage and time
- **Phase 1:** 9 Nov 2026, about 19:25–19:50 SGT.
- **Phase 2:** "Go" received about 19:52; final file verified about 20:08 SGT. That is ≈ 16 minutes of production after approval, plus documentation.
- **Revisions:** 3 images; 22 voice takes, no re-takes; 1 full draft, 3 delivery renders; 1 transcription pass and 1 vision pass.
- **Tokens:** UNAVAILABLE as per-model counters in-session.

## 9. Rubric self-evaluation (evidence, not a score)

| Area | Evidence | Known weakness |
|---|---|---|
| Technical accuracy (30) | `CLAIMS.md`; wording fixed against the source; public-safe | Generic by rule: no control-level detail |
| Visual art direction (25) | Native Swiss Grid look, consistent; three clay spot illustrations | Mostly diagrammatic by design |
| Motion and continuity (20) | The 243 squares persist and sort into buckets; the line builds; the release chip travels the gate | 2D motion only |
| Narration and sound (15) | Verbatim Realtime voice; −16 LUFS | **Not audibly reviewed** |
| Readability (10) | 720p frames; captions ≥ 1.87 s | Tag pills 22 px |

Total: NOT_ASSESSED.
