# Verification and review limits

## Production boundary

This is a **source-grounded synthetic engineering film**, not live acceptance of AWSOps. Source main matched `15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9`. Eighteen scoped files were Git-blob verified before use. Accepted historical source/read/transfer records are classified in evidence.md. No source repository changes, AWS calls, provider clients, authentication flow, infrastructure, paid API/service, new agent, deployment or publication occurred. Actual paid usage: **USD 0**.

The deliverable follows the natural local speech: **649 seconds / 10:49**, normal speed 1.0, no music, 100 measured sentence WAVs and 100 sentence-aligned captions. No overlap was found; the last speech ends at 647.791 seconds. The sentence cache protects unchanged narration across visual edits; a successful `--reuse-audio` build reused all 100 clips without synthesis. No good narration was regenerated, trimmed, padded or accelerated to hit a runtime target.

## Local checks actually performed

- Pure offline fixture check using the pinned, byte-verified intake/scope helpers: `IMPORTED_ASSERTION`, zero real writes, unknown-field rejection, matching complete scope digest and mismatch after a revision change. No application/executor test suite was rerun, and no provider code was executed.
- HyperFrames 0.9.20 final check: **passed**; browser checks enabled, no lint/runtime/audio/craft errors; 169/169 contrast checks passed. Its optional motion-analysis module was disabled, so actual motion is checked separately on encoded frames rather than inferred from that heading. One layout warning identifies the deliberately disconnected lost-response arrow. Five connector information notices concern diagram spacing/branch lines; these are not claimed as perfect automated layout acceptance.
- Source-composition snapshots inspected across the opening, import, scope before/after drift, decision race, policy/ledger, UNKNOWN/read-only reconciliation, conditional cleanup and evidence board. Corrected a small extra-field/companion-box overlap and initial reveal timing; added required media IDs before rendering. One 16-second scope proof was encoded with H.264/AAC before the full production; its 1280×720 frame was inspected for ordinary laptop legibility. Main fields, warnings and captions were readable at that size; no audience comprehension test is claimed.

The final 46,284,509-byte MP4 is H.264/AAC, 1920×1080, 30 fps, exactly 649 seconds. Full FFmpeg decoding passed. Encoded-frame comparisons independently show scope revision drift (183→190s), moving Reject request (266→268s), request-packet movement after the entry transform settles (397→398.3s), and evidence-lane reveal (501→507s); crops exclude captions. Metrics are retained in motion-check.json. Final encoded UNKNOWN, evidence-lane and dated evidence-board frames were inspected; the 1280×720 evidence payoff keeps fields and captions readable. Signal measurement found active audio (mean -26.2 dB, peak -5.5 dB), not a human quality judgment. The output-directory copy matches the repository MP4 SHA-256. Final-file player samples are recorded individually in validation.json.

## Human acceptance remains separate

The voice is generated locally with Kokoro `am_michael`. The agent cannot hear or evaluate pronunciation/prosody, and programmatic checks cannot establish human comprehension or creative quality. Actual-player sampling is reported separately from full FFmpeg decoding; neither is represented as a human listening pass. Human technical, listening and creative acceptance remain pending. The PR is draft and unmerged.

The film's deliberately conservative conclusion matters more than a polished badge: a provider MATCH can coexist with compliance UNKNOWN and freshness NOT_VERIFIED. The normal live approval path still fails closed without its trusted binding; a synthetic Approve Once is not an owner's decision. Dated source/Config receipts and transferred live work are never promoted into fresh deployment or AWS acceptance.

Delivery playback: final-file ffplay samples 0–20s, 395–430s, 500–530s and 629s through the 649s ending all exited successfully. These are sampled actual-player checks plus full programmatic decode, not a claim that the agent heard or a human accepted the full narration. MP4 SHA-256: `4a84d17f7381171abdfdbc4479863ebbcefaa461ac2cc922cf8e89f3b71a1450`.
