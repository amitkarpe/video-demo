# Shot list — "The reply disappeared" (53.7 s)

Times are from `cues.json`. Narration is the caption text. Camera = a pan/zoom over one continuous system map, so the viewer never leaves the same world until the final evidence ladder.

| # | Time | Narration | What moves | Camera |
|---|---|---|---|---|
| 0 | 0.0–1.3 | (silent) | Fade up. `APPROVE_ONCE ✓` draws. Ledger row `policy = INTENT`. Official S3 icon appears across the boundary. | Close on the trusted backend |
| 1 | 1.3–5.0 | "In this simulated branch, an approved request leaves the backend." | Ledger flips to `CALLING` *before* the `PutBucketPolicy` packet leaves. Packet crosses the SDK boundary and reaches S3. | Pull back to full map |
| 2 | 5.4–7.5 | "The reply never arrives." | S3 goes foggy with a `?`. A green acknowledgement signal leaves S3, breaks up and dies at the boundary (`✕`). Amber ring pulses; 1.1 s silent hold. | Slow push toward the boundary |
| 3 | 8.6–10.0 | "Did the change fail?" | Card B, `NOT APPLIED`, lights. | Move to the S3 side |
| 4 | 10.3–12.1 | "Or did only the reply fail?" | Card A, `APPLIED · NO REPLY`, shows the fixed policy (Deny `s3:*` if SecureTransport=false). | Hold |
| 5 | 12.8–16.1 | "The SQLite ledger already says CALLING." | Ledger card enlarges; step strip `INTENT ▸ CALLING ▸ SDK CALL ▸ ✕ ACK`. | Zoom to ledger |
| 6 | 16.4–18.1 | "It was committed before the call." | Green bracket under `CALLING` → `SDK CALL`: "SAVED BEFORE THE CALL". | Hold |
| 7 | 18.7–22.6 | "So AWSOps does not send that write again." | A ghost `PutBucketPolicy` retry hits a red gate and bounces: `NO RESEND`. | Back to full map |
| 8 | 22.9–26.4 | "It reconciles the same run, read-only." | Reconciler turns cyan; a `GetBucketPolicy` probe travels the read-only rail to S3. Label `READ-ONLY · SAME RUN A`. | Follow the probe |
| 9 | 27.0–32.1 | "A matching S3 policy, independently read back, answers one question only." | S3 fog lifts, card A turns solid green, `Deny · observed` returns, `readback: MATCH`. World recedes; the four-row ladder opens with only `PROVIDER READBACK = MATCH` filled. | Dissolve to ladder |
| 10 | 32.6–34.9 | "Execution is still unknown." | `EXECUTION = UNKNOWN`; red `✕` connector: MATCH does not upgrade it. | Static |
| 11 | 35.1–37.1 | "Compliance is unknown." | `COMPLIANCE = UNKNOWN`; second `✕` connector. | Static |
| 12 | 37.3–39.4 | "Freshness is not verified." | `FRESHNESS = NOT_VERIFIED`. | Static |
| 13 | 39.7–42.5 | "No AWS Config evaluation has run." | The official AWS Config icon gets a red dashed "not called" frame. | Static |
| 14 | 43.2–48.0 | "Until the missing evidence is resolved, the outcome stays NEEDS_REVIEW." | `NEEDS_REVIEW` stamp lands with an amber glow. | Static |
| 15 | 48.6–52.2 | "This demonstrates control logic, not live acceptance." | Footer: SYNTHETIC / MOCK · live acceptance still pending. AWS icon credit. Fade to black. | Static |

Persistent on every frame: `SYNTHETIC / MOCK WALKTHROUGH` pill; `RUN A · run-canary-3f9c… · SYNTHETIC ID` tag (invented id, not a real account or run).

Keyframes: problem ≈ 7.9 s (end of shot 2), mechanism ≈ 20.2 s (shot 6), payoff ≈ 51.0 s (shot 14).
