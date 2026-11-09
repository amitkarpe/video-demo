# OpenAI API voice lab (Mac)

## Confirmed credit grant (owner screenshots, 7 Nov 2026)

- ChatGPT Business subscription successfully linked to the **Personal** OpenAI Platform organization.
- **$61.00 promotional API grant**, issued 7 Nov 2026, expires 23 Nov 2026 (prorated).
- Previous grant: **$3.14 remaining**, expires 1 Apr 2027.
- Claim screen indicates **$120 next cycle on 23 Nov 2026**, subject to continuing eligibility; it is not guaranteed cash.
- Auto-reload was OFF. Keep it OFF. Credits are metered API allowance, separate from ChatGPT/Work/Codex subscription usage.

## First experiment: Mac voice narration (no paid software)

1. Check [credit grants](https://platform.openai.com/settings/organization/billing/credit-grants) and [usage](https://platform.openai.com/usage).
2. In the **linked Personal API organization**, make a project API key through [API keys](https://platform.openai.com/api-keys) using a secure local flow. ChatGPT sign-in is **not** an API key.
3. Keep the API key in macOS Keychain or a non-repository secret store; local Codex should expose it only as the environment variable OPENAI_API_KEY to the test process. Never commit, log, screenshot or paste it in ChatGPT or a PR.
4. Use the current [Realtime API WebRTC guide](https://developers.openai.com/api/docs/guides/voice-webrtc) and [Realtime getting started guide](https://developers.openai.com/api/docs/guides/realtime). Prefer **gpt-realtime-2.1-mini** for the first low-cost test. The old gpt-realtime-mini is deprecated, with shutdown scheduled for Jan 20, 2027.
5. Run one **manual, max-60-second, localhost-only** narration test on a fictional EC2 finding. Never include customer/security/workplace secrets. Record whether audio sounded natural, the total duration, and whether the actual API billing dashboard shows consumption. No live AWS calls.
6. If local Kokoro narration already in [draft PR #2](https://github.com/amitkarpe/video-demo/pull/2) is good enough, prefer it for unlimited offline revisions. Do **not** edit PR #2 from this voice lab branch.

## Short narration sample

> This is a simulation. An EC2 server has a high severity finding. An AI assistant summarizes the risk and proposes a fix. A person reviews and approves the plan. Only after approval would AWS Systems Manager perform patching. No real AWS changes are made. Finally, the system verifies the outcome and records audit evidence.

## Budget / security guardrails

- Promotional credits are not unlimited. All generated audio, text, and sessions consume API budget under the published [model pricing](https://developers.openai.com/api/docs/pricing).
- Start with one test. Do not enable automatic billing, buy credits, or change payment settings.
- Keep all keys on the **local server**, never in browser JavaScript. Browser access needs a short-lived ephemeral Realtime client token minted locally.
- Use WebRTC, a one-click Start/Stop UI, and auto-stop after 60 seconds. A browser agent's successful page load does not prove the voice session worked; verify audio playback and usage.
- No public listener, public tunnel, analytics, authentication state or repository credentials.
- This document is a handoff. **No API request has been executed by the GitHub-only authoring session.**

## Local Codex acceptance

Reuse [Issue #3](https://github.com/amitkarpe/video-demo/issues/3). Build the smallest localhost voice sample using Node 22+ and current OpenAI official Realtime WebRTC documentation, with manual click, ≤60-sec timer, server-only main API key, and ephemeral browser credentials. Perform syntactic tests first; use one actual API session only after the owner configures credentials securely. Record user listening feedback and billing evidence; do not touch the existing video writer PR #2. Keep one cohesive PR, no merging without separate authorization.
