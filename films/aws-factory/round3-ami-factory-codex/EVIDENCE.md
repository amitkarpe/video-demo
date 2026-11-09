# Round 3 evidence

## Product and scope

A 268-second original film, 1920×1080, H.264 / AAC stereo, 30 fps, 8,040 frames, 57,739,637 bytes. The actual output hash is `3e01ae8dd0e64708040999912d97f043f25235f0db1d78bb0099823bb38e8953`.

All work is confined to this lane's output directory and its new isolated branch. The shared benchmark base is pinned to `995e8287847b77f81707e485f9767700bc98c162`. Earlier rounds and the other lane were not changed or used as creative references. Worktree inventory was inspected at closeout; active, unmerged or uncertain checkouts were retained.

## Readiness and technical checks

- Existing authorized credentials: authenticated model lookups succeeded; actual mandatory Images and Speech requests then succeeded. No secret was printed or committed.
- Runtime: Node 26.12.1, npm 11.20.0, FFmpeg 9.0.2, pinned HyperFrames 0.9.20 and GSAP 3.15.0. The optional API environment used Python 3.12.16 with frozen dependencies.
- Computer Use: the local in-app browser opened the composition, changed scene controls and displayed final media. This is evidence of browser control; it does not claim native QuickTime control.
- Rendering: a one-second preflight succeeded, followed by three complete 268-second renders. The final render uses the revised caption breaks, disclosure backing, proposed dashed paths, task-placement motion and explicit ECS-agent health.
- Composition lint: **zero errors, zero warnings**. Full-file FFmpeg decode: **PASS**.
- Final browser playback: **PASS**, continuous played range **0–268 seconds**, `ended=true`, `error=null`, unmuted at normal speed. The exact video hash is bound to `evidence/playback.json`. A separate player was opened at the start for owner review.
- Final audio measurement: **−16.13 LUFS integrated**, **−2.50 dBTP**, **3.70 LU** loudness range. These are measurements of the delivered AAC, not a claim of audible quality.
- Captions: **79 cues**, no overlap, at most two lines, minimum display **0.9 seconds**, all within the film. Word timing comes from the cached narration's full transcription; source display wording and expanded spoken acronyms are distinct and recorded.
- Encoded motion: cropped frame differences confirm changing pixels in the opening camera, task-placement scene and rollback. Crops exclude the title, caption and progress meter. This supports actual encoded motion, not an aesthetic score.
- Integrity: **30 cached media/QA hashes** verified against receipts; **31 paid calls** completed; no reserved/uncertain calls remain. Near-cap and uncertain-request synthetic admission checks both stop before dispatch and leave the ledger unchanged.
- Publication hygiene: text-pattern checks found no API keys, 12-digit account IDs, private resource IDs or AWS ARNs. Manual source/content review confirmed that only original public-safe synthesis and fictional visuals were included. This is not a claim that pattern scanning alone detects every possible secret.

Machine-readable measurements are in `evidence/technical-checks.json`, `evidence/composition-lint.json` and `manifest.json`.

## Visual and audio QA

The author inspected all 14 encoded draft frames at 1280×720. Important states included direct lineage, package-only hardening limits, category-specific acceptance, effective launch/KMS access, separate PROD acceptance, explicit Ops approval, future policy prerequisites, blocked promotion and separate data recovery. Five full-resolution final keyframes and the altered scenes were inspected again. No essential label or caption clipping was observed in those samples.

Whisper checked the complete narration. Its “Free child families” and “production cannery” outputs were uncertain recognitions, not silently accepted transcript text. A separate prompt-free `gpt-4o-transcribe` call on those two cached speech segments recognized **“Three child families”** and **“production canary”**. Exact outputs are retained. Other alignment differences are punctuation, proper-name spacing, hyphens, expanded CRUD and DEV/PROD wording. The script and receipt retain what was requested from the speech model.

The paid GPT Vision frame review was not treated as approval. It incorrectly turned several intentionally illustrated stop conditions into requirements to perform real operations and misassociated timestamps. `VISION_REVIEW_DISPOSITION.md` records why those actions were outside this film's scope. No infrastructure action was taken.

**AUDIBLE_REVIEW=NOT_VERIFIED.** This agent has no verified audible listening channel. Automated ASR, complete decoding, audio-level measurement and browser playback cannot establish voice warmth, pronunciation nuance, music preference or human creative acceptance.

## Self-evaluation without a winner score

| Rubric area | Evidence | Remaining human judgment |
| --- | --- | --- |
| Technical accuracy / explanation | Current versus required versus proposed claims are separated; no unattended PROD claim; source matrix retained | Whether the explanation fits the intended audience |
| Visual design | Original warm/night factory images, consistent machine silhouettes and editable overlays | Beauty, originality and emotional impact |
| Motion / continuity | Generated-set continuity, shared floor, traveling packets, approval signature, reversing image; encoded motion checks | Whether the journey feels sufficiently cinematic |
| Narration / pacing / sound | Real Cedar narration, original score, two ASR checks, measured final mix | Actual listening and pacing preference |
| Readability | 720p frame review, 79 two-line caption cues, sampled final frames | Comfortable viewing on the owner's display |

No numeric score or comparative winner is assigned.

## Accounting and iteration counts

Usage-priced media/QA: **$0.2083537 / $10**; remaining **$9.7916463**. Two image requests, 26 speech requests, two transcription requests and one Vision request. Credits count as spending. These are returned-usage calculations rather than an invoice. Separate inference cost: **UNAVAILABLE** because no verified model tariff or billed subscription breakdown is exposed.

Research: one integrated source/public-doc cycle, then focused model/pricing and final authority checks. Script: one 26-unit narrative version. Images: one original generation plus one continuity edit. Speech: 26 units, one version each, no regenerations. Audio: one original score and one final normalization pass. Captions/layout: initial composition plus two revisions. Rendering: one short preflight plus three full renders. ASR: one full narration pass plus one focused independent cross-check. Vision: one frame-review pass with explicit disposition.

Actual runtime model and effort, token counter scope and captured totals are in `run-metrics.json`. Counters include protocol overhead and cached context, and exclude any later closeout tokens after the recorded capture. No billing estimate is fabricated.
