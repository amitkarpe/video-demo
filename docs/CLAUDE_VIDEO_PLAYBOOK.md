# Claude Video Production Playbook

Status: active · Reviewed: 2026-11-08 · Owner: Amit Karpe · Canonical home: `amitkarpe/video-demo/docs/CLAUDE_VIDEO_PLAYBOOK.md`

This is the one reusable guide for producing technical explainer films with Claude Code. A fresh session needs only this file, the project's goal and its authorized sources. It needs no earlier chat, old worktree paths or private repositories.

**Roles.** ChatGPT/Astra owns the plan, teaching angle, factual narrative and first script. Claude owns art direction within that brief, storyboard, production, verification and iterative improvement. Amit owns final creative and listening acceptance. This is the owner's workflow choice. It is not a claim that one model is universally better.

**Authority.** This guide grants no tools, credentials, network access, spending, hearing ability or repository permission. The owning goal and the repository's own rules decide what is allowed. When they conflict with this guide, they win.

---

## 0. Quick start

1. Read the goal (template in §8). Stop and ask once only if the source, output location, approved name, budget or required media is missing or contradictory.
2. Run the **preflight** (§2). Record VERIFIED / MISSING / UNVERIFIED for every capability before any paid call.
3. Build the **claim map** (§6.1) from the sources. Every on-screen fact gets a state.
4. Write a one-page editorial brief: audience, the **one remembered outcome**, and problem → mechanism → consequence → payoff.
5. Design the treatment: a style sheet, three representative frames, and one moving slice of the *hardest middle scene* (§4).
6. Generate the media with a spend ledger (§7) and keep the provider originals immutable (§5.2).
7. Build the full film, then review the **final encoded file**: frames at 1280×720, motion, captions, transcription of the final mix, claims (§6).
8. Repair only measured defects. Re-render the affected scenes, then export once more.
9. Deliver the bundle (§7.3) and the status report (§8.3). Mark everything you could not assess as NOT_ASSESSED.

---

## 1. Planner-to-Claude contract

**Inputs Claude must receive (or confirm absent):** use the goal template in §8.1. It covers the exact source revision, output location and visibility, approved project name, audience and knowledge level, the one remembered outcome, essential facts with states, available assets, script lock level, reference style, API budget, required outputs, the writer, and the actions that are not authorized.

**Editorial freedom.** Unless the goal says the wording is locked, Claude may rephrase for the ear and change pacing, transitions, shots, scene order and duration, as long as the meaning is preserved. Record any material editorial change in the delivery report. Do not freeze a weak script just because a planner wrote it.

**What needs correction or approval:** a change to facts, audience, scope, security posture, authority, or a claim's state. Routine art and production choices do not.

**Story shape.** Use problem → mechanism → consequence → payoff, built around one question the viewer wants answered.
- Explain the value first.
- Attach each material caveat to the visual it qualifies. Do not repeat the whole safety policy in every scene.
- **Never map one repository module, document section or paragraph to one scene.** An inventory is not a story.
- End by landing the remembered sentence.

**Names and dates.** Use only names, brands, schedules and cadences that the sources or the owner approve. Do not invent a product brand, an upstream release cadence or "current" automation from an aspirational brief. If a name is not approved, use the established project name. Example: an earlier AMI film used an unapproved "BlueOps" brand where the established name was "AMI Factory".

---

## 2. Preflight before any paid generation

Prove each capability in the **selected session and execution location** (local, WSL, remote host or container). An installed app is not proof. Record actual versions and paths in the report.

| Capability | Safe verification | Fallback | Blocks if |
|---|---|---|---|
| Execution | Run a shell command; write and read a scratch file in the project; open an image file for inspection | Ask the owner to start a Claude Code session (Desktop **Code** tab or CLI) | Chat-only session, no shell, or read-only project |
| Sources | `git ls-remote` / `git rev-parse <rev>` for the source; read one source file | Owner supplies material, or an explicit "story-only" brief | Required source unreadable |
| Delivery | `git remote -v`; push permission to a new branch; existing authenticated `gh` (or the hosting CLI); output repo visibility; any push-triggered deploys | Deliver the files locally and report | Cannot write to the output location |
| Node / npm | `node --version` (HyperFrames documents **Node 22+** as the minimum); `npm --version` | Use the project's existing compatible install; do not upgrade blindly | Below the minimum, with no approved install |
| Renderer | Reuse the project's lock; a new project pins exact versions once (`npm install --save-exact hyperframes@<ver> gsap@<ver>`, commit `package-lock.json`). Then `npx hyperframes --version`; a 1–2 s test render, then `ffmpeg -v error -i out/preflight.mp4 -f null -` | Fix the browser download or path; reduce workers | The test render or decode fails |
| FFmpeg | `ffmpeg -version`, `ffprobe -version` | Approved package manager | Missing |
| Python helpers | `python3 --version` (Windows: `py --version`); a venv with only the packages the chosen helpers import | Rewrite the helper in Node | No interpreter and no alternative |
| Resources | Free disk (`df -h .` / `Get-PSDrive`); RAM and CPU; fonts actually installed or fetched; H.264/AAC encode | Lower render concurrency; clear only *own* build outputs | Not enough disk for renders plus the final export |
| OpenAI access | Credential **presence only** (below); a free model lookup that returns HTTP 200 for each required model; budget authorized in the goal | Owner provisions a key or budget | Missing key, budget or model, when the goal requires that media |
| Network | HTTPS to the API host; WebSocket only if the chosen narration path needs it | A Speech-API path, if the goal allows it | Required endpoint blocked by policy |
| Review | Can the session view images? Watch a full playback (browser `<video>`)? **Perceive audio?** (Usually no.) | Machine QA plus the human listening checklist (§8.2) | Never assume hearing |

**Credential presence check (never print the value):**

```sh
[ -n "$OPENAI_API_KEY" ] && echo present || echo missing            # macOS/Linux/WSL
if ($env:OPENAI_API_KEY) {'present'} else {'missing'}               # Windows PowerShell
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models/<model-id>                        # 200 = visible to this key (no charge)
(Invoke-WebRequest -Uri https://api.openai.com/v1/models/<model-id> -Headers @{Authorization="Bearer $env:OPENAI_API_KEY"} -SkipHttpErrorCheck).StatusCode   # PowerShell 7
```

**Secrets.**
- Take the key from the process environment or approved secret storage. Use an ignored, protected `.env` only if the owner allows it, and read it inside the generating process.
- Never echo or dump a key. Never ask for one in chat or issues. Never put it in HTML/JS, URLs, logs, screenshots or commits.
- Do not scan unrelated credential stores, rotate keys, change billing, disable sandboxes or proxies, or bypass managed policy.
- Claude Desktop sessions may not inherit shell-profile variables (it does not read PowerShell profiles on Windows). The **owner** sets the variable in a saved local environment (or the approved secret store) and starts a new session; Claude does not read profile files or other stores to find it.
- A Claude or ChatGPT subscription is **not** OpenAI API authorization or credit.
- Missing credential → stop paid work, report the exact blocker, and keep doing no-spend preparation.

**Host differences.** These are documentation-reviewed. Only macOS (Node 26.12.1, FFmpeg 9.0.2, HyperFrames 0.9.20) has actually been executed for these films.

| | macOS | Windows native | WSL 2 (if already authorized) | Linux / headless |
|---|---|---|---|---|
| venv binaries | `.venv/bin/python` | `.venv\Scripts\python.exe` | `.venv/bin/python` | `.venv/bin/python` |
| Paths and quoting | POSIX | Backslashes, PowerShell quoting | Linux paths; never mix with `C:\` | POSIX |
| Review player | Any browser or VLC (QuickTime optional) | Browser or VLC | Browser on the Windows side, via a local HTTP server | No display: full decode, plus a browser playback check if headless Chrome is allowed; otherwise playback = NOT_ASSESSED |
| Fonts | System or fetched OFL fonts | Same; verify the fallback | Linux fonts | Install approved OFL fonts or embed them |

Use relative paths inside the project. Never hard-code `/Users/...`. On any host other than macOS, report the recipe as *documentation-reviewed, first execution* and record what actually ran.

**Corporate or offline hosts:** confirm an approved media environment and permitted data export. Do not work around restrictions or promise compatibility with an arbitrary host.

---

## 3. OpenAI media policy

**Durable rules (Amit's standard cinematic workflow, unless the goal overrides them):**
- Use **real OpenAI-generated artwork** meaningfully in the final film. It should carry the world, metaphor and continuity, not be a background behind slides.
- Use **real OpenAI-generated narration**, disclosed on screen as an AI voice.
- Exact technical labels, diagrams, values, connections and service identities are **deterministic, editable code** (HTML/SVG). Never use generated lettering or invented logos.
- Keep a style sheet: palette, lighting, camera height, line weight and materials. Use reference **image edits** so a character or object stays the same across scenes.
- The image model, the compositor (HyperFrames/GSAP/FFmpeg) and the QA reviewers do different jobs.
- Do not depend on Sora/video generation or GPT Live.
- Record the actual model used. If the goal's model, or the §3 default when the goal names none, is unavailable, use only a successor the goal lists, report it, and never claim the requested model ran. If no successor is listed and the media is required, that media is **BLOCKED**. Report the exact lookup result and continue no-spend work.

**Dated defaults (reviewed 2026-11-08; recheck the official docs, availability, voices, endpoint compatibility, pricing and account eligibility for every production):**

| Need | Default observed | Notes |
|---|---|---|
| Images | `gpt-image-2.6-sunburst` via `/v1/images/generations` and `/v1/images/edits` | Custom sizes (multiples of 16), transparent background, returned `usage`; one image cost a few cents at "high" in Round 3 |
| Narration, Speech API | `POST /v1/audio/speech` `{model, voice, input, instructions, response_format: "wav"}` with `gpt-4o-mini-tts` (voices incl. `cedar`, `marin`) | Returns audio with no usage counts, so reserve from a duration upper bound. `tts-1`, `tts-1-hd` and `gpt-4o-mini-tts` shut down **2027-01-06** |
| Narration, Realtime | `gpt-realtime-2.1` (Round 3, voice `marin`); `gpt-realtime-2.1-mini` is the documented replacement | A **different integration** (WebSocket session). Not a `/audio/speech` model. It can generate saved files without building a voice app |
| Transcription QA | `gpt-transcribe` (or `gpt-live-transcribe`) | `whisper-1` and `gpt-4o-*-transcribe` are deprecated for 2027-02-26 |
| Frame QA | Any supported image-input model (Round 3 used `gpt-5.5` and `gpt-4.1-mini`) | "GPT Vision" is not an endpoint name |

Reserve each call from the *current* published per-token or per-minute prices. On-screen disclosure example: `Narration: AI-generated voice (OpenAI <model>, <voice>) · Artwork: OpenAI <image model>`.

---

## 4. Production loop (one-go)

Run internally: claim map → editorial brief → visual and voice treatment → **three representative compositions** (problem, mechanism, payoff) → **moving slice of the hardest middle scene** (tests mechanism, motion, voice and captions together) → full production → review of the final encoded file → targeted repairs → delivery.

- **Approval pauses.** Under an approved one-go goal, the slice is a **self-review checkpoint, not an owner approval pause**. Add an owner taste gate only when the goal asks for one or a material change needs approval. This replaces the older two-phase pilot rule (discovery → approval → execution) for goals that already grant execution.
- **Effort follows the story.** Let duration, image count, research depth and revision count follow the story and the measured defects. There are no quotas.
- **When to stop.** Stop when the acceptance checks pass or a precise external blocker remains. Unrestricted iteration is not endless re-rendering: reuse cached media and re-render only the affected scenes before the final export.

**Shot rules.**
- **One job per shot.** Each shot has a focus, a visible action or state change, and a teaching purpose.
- **Spatial continuity.** Keep stable spatial identities: the same object stays in the same place and look. Use cause-and-effect transitions (the thing that happens *is* the transition).
- **Camera and reading time.** Make purposeful camera moves and hold long enough to read. Clamp camera moves so generated plates always cover the frame (no exposed edges).
- **Clarity beats decoration.** Show only the **active** state at full strength. Inactive context must stay readable or be hidden; dim, crowded side panels are a defect.
- **Not slides.** Do not decorate slides: no dense dashboards, no particles covering text, no static image pans posing as system mechanics, no constant gratuitous zoom.
- **Metaphor vs architecture.** Keep illustrated metaphor visibly distinct from real architecture.
- **Laptop check.** Review every scene at laptop size (1280×720), including the worst transition frames.

---

## 5. Narration, captions and sound

### 5.1 Writing and generation
- Write for the ear. Keep a pronunciation glossary (acronyms, product names) and test the hard names on a short sample early.
- Generate coherent sentence or scene units for good prosody. Avoid tiny fragments.
- For each take, require all of: a completed provider response, non-empty valid audio, the expected sample rate and channels, and **an independent check of the spoken content**. The generating model's own transcript is not enough. Use a separate transcription: local offline ASR (no spend) or a paid model only if the goal allows paid QA. Investigate mismatches at their timestamps.

### 5.2 Immutable originals (mandatory)

```
media/original/voice/<line>.<take>.<ext>    # provider bytes exactly as returned; never edited or overwritten
media/original/images/<id>.png              # provider output exactly as returned
media/derived/voice/<line>.v<N>.wav         # trims, resamples, gain; regenerated from originals by script
media/manifest.json                         # sha256 of every original, the selected take per line, and the derivation step
```

- Write the provider output to `original/` **before** any processing (trimming, resampling, normalising). Then hash it.
- Selective regeneration adds a **new take** file and updates the selection in the manifest. Never copy derived audio back into `original/`, and never overwrite the takes of untouched lines.
  - Round-3 lesson: the narrator trimmed before its first save, and the README's re-copy step could overwrite retained originals with processed audio during a later selective run. This is a reproducibility risk found by inspection; no audible defect was demonstrated.
- Do not strip every pause, clip quiet syllables or speed up speech to hit an invented length.

### 5.3 Captions and mix
- Rebuild caption timing from the **post-edit audio**: per-sentence cues from the measured clip lengths and the assembly offsets, or word timings from an offline ASR pass over the edited narration. Then transcribe and review the **final mixed export**, not just the voice stems.
- **Caption house defaults:** one or two lines, grouped by spoken meaning, safe margins, at least ~1 s on screen, and about 24 px or more at 720p. Cut text rather than shrinking it.
- Check the central captions and the secondary labels at 1280×720 on the worst transition frames.
- Music and event-tied effects support speech. Duck them under the voice.
- **Loudness house defaults (web):** about −16 LUFS integrated, true peak ≤ −1 dBTP. Measure the loudness, peak and clipping. These are engineering checks, not proof that the sound is pleasing.

---

## 6. Claims, quality gates and review

### 6.1 Claim states (use them on screen and in the report)
- **DOCUMENTED** — the source describes the contract or design.
- **IMPLEMENTED** — code exists at the stated revision.
- **DEMONSTRATED** — measured or live evidence exists.
- **ILLUSTRATIVE** — an outcome invented for the film.
- **PROPOSED** — future or not yet built.
- **UNKNOWN** — not established.

Keep the claim map as a table: `claim | state | source (file@revision or owner brief) | where shown (scene/time) | wording on screen`. Keep the QA record as: `check | artifact sha256 | method | observed result | disposition`.

A "CURRENT" badge with green ticks reads as *result*. Label required checks as requirements ("must place ≥1 task"), not as passes, unless the result is demonstrated. Verify names, dates, cadences and success claims against the source.

### 6.2 Gates to track separately (record the artifact hash, the revision and what was actually observed)

| Gate | Evidence | Not proof of |
|---|---|---|
| Factual fidelity | Claim map ↔ source revision | Audience understanding |
| Secrets, private data, licensing | Pattern scan plus manual review; asset provenance | Absence of every secret |
| Full decode | `ffmpeg -v error -i final.mp4 -f null -` exits 0 | Playback or quality |
| Full-duration playback | Browser `<video>` `played` range [0, duration], `ended=true`, `error=null`, unmuted, file hash bound | Human viewing or listening |
| Motion | Encoded-frame differences on cropped regions; watching the moving slice | Smoothness from stills |
| 720p readability | Frames at 1280×720, including transition frames | Comfort on the owner's display |
| Caption timing | Cues from the final audio; no overlaps; dwell time | Prosody |
| Machine audio QA | Independent transcription of the final mix; loudness | Voice quality, subtle SFX |
| Human listening | Owner's checklist (§8.2) | — |
| Audience comprehension | Three-question test (below) | — |
| Owner acceptance | Explicit owner verdict | — |

- **Decode, playback and listening are three different things.** A few seconds of player progress is not continuous viewing. Machine checks never become "audiovisual acceptance". Record **AUDIBLE_REVIEW=NOT_VERIFIED** unless a human listened.
- **Machine reviewers get bounded context:**
  - Give them the exact brief, the expected claim states, and each frame's timestamp.
  - Accept or reject each finding with a reason in a disposition note.
  - Verify the fixes on the final encoded revision.
  - Machine reviewers have mis-timed frames and recommended out-of-scope operations; their output is advice, not approval.
- **Rubric (unchanged weights):**

  | Area | Weight |
  |---|---:|
  | Technical accuracy and clarity | 30 |
  | Visual art direction | 25 |
  | Motion, camera and continuity | 20 |
  | Narration, pacing and sound | 15 |
  | Readability and subtitles | 10 |

  - Speed, cost, tokens and API-call counts are reported separately and never earn points.
  - Unassessed areas stay **NOT_ASSESSED**: no neutral filler scores and no /100 total. A partial score names its denominator and is not comparable to a full one.
- **Blocking defects:** a technical falsehood; leaked private data; unlicensed assets; unreadable essential explanation; missing authorized mandatory media; a misleading live-success claim.
- **Comprehension test (closing check):** what happened? Why does it work? What is still limited or unproven?

---

## 7. Budget, usage and delivery

### 7.1 Spend ledger (one per film)
The goal must state the API/media cap. "$10 per film" is a template example, not standing authority. The ledger works as follows:
- Before each call, **reserve** a conservative estimate and stop if `committed + reserve` would exceed the cap. Bound the outputs (size, quality, max tokens).
- After the call, **settle** it with the cost computed from the returned usage. Label any estimate as an estimate.
- Record `CALLING` before the network call. A timeout or unknown result stays reserved: **no blind replay**. To resolve it:
  - the owner checks provider usage, or the call's request ID if one was returned
  - if the owner confirms no charge or no output, record that and release the reservation
  - a new attempt is a separately reserved call, made only after that confirmation or with an explicit owner instruction
  - until then, the affected media is blocked: report it and continue no-spend work
- Paid calls run serially. There are no automatic top-ups, and no spending just to use up credits.
- Do not rely on a provider billing alert to stop spending; the ledger is the stop.
- Rebuilding from cached outputs must make **zero** paid calls.

### 7.2 Usage and time record
- Actual agent and model, effort (if observable), and timezone-aware start and end.
- Elapsed time and the image, audio and render revision counts.
- Token counters with their scope. In Claude Code, the `/usage` Session block shows per-model input, output, cache read and cache write for the *session*. State whether the session spanned other work.
- Context-window occupancy is not tokens consumed. Reasoning is already inside output. Repeated cached context is not new content.
- A subscription or list-price estimate is not an invoice.
- If a counter is not observable, write UNAVAILABLE with the reason. Do not delay a film to invent numbers.

### 7.3 Delivery bundle
- **Media files:**
  - final MP4 (H.264/AAC; stay under the host's file limit, e.g. a web re-encode)
  - SRT and transcript
  - three to five keyframes taken from the final file
  - cached originals with provenance (prompts or prompt hashes, settings, usage, output hashes, rights)
- **Source and setup:** the editable composition, build scripts, lockfiles and setup steps.
- **Records:**
  - claim map and QA record with dispositions
  - spend ledger and usage summary
- **Links:** confirm the delivered or linked file is byte-identical to the reviewed one (hash). Give accessible links, such as a raw URL pinned to a commit. In a private repository these links work only for people with access, so state that. A `/Users/...` path is not a download.
- **Hosting:** do not enable public hosting or Git-LFS, or exceed storage limits, by assumption.
- **Fonts:** need a licence (e.g. OFL) and fallbacks. Never commit proprietary font binaries.
- **Hygiene:** never carry over source repos, project names, issue numbers, worktree paths, tariffs or spend approvals from an earlier film as defaults.

---

## 8. Templates

### 8.1 Future video GOAL (copy, fill, delete unused lines)

```markdown
GOAL — <film title> (<approved project name>)
Source of truth: <repo@revision | supplied files> (read-only; private stays private)
Output: <repo>/<dir> on new branch <name>; visibility <public|private>; PR target <branch>; merge: <not authorized>
Audience: <role + prior knowledge>    Remembered outcome (one sentence): <...>
Essential facts (state each): <fact — DOCUMENTED|IMPLEMENTED|DEMONSTRATED|ILLUSTRATIVE|PROPOSED|UNKNOWN>
Assets available: <logos/icons with licences, screenshots, prior media>
Script: <attached>; wording <locked | editorially adaptable — keep meaning>
Reference style: <links/adjectives>    Duration: <guide only | hard limit>
Media: OpenAI artwork <required|optional>; OpenAI narration <required|optional>; voice <preference>
Models: image <id>, narration <id + API: speech|realtime>; permitted successors <list|none>
API/media cap: USD <n> (credits count); paid QA <allowed|not allowed>
Required outputs: MP4 1080p, SRT, transcript, keyframes, source, ledger, QA record
Script author: <planner>; repository writer (only one): Claude (this session)    Owner gates: <none | after slice | other>
Not authorized: <cloud ops, deployment, credential changes, merge, public hosting, other>
```

### 8.2 Human listening checklist (owner, full playback, normal speed)

1. Voice: natural and warm? Any mispronounced name or acronym (list the timestamps)?
2. Pace: rushed or dragging anywhere? Any pause that feels cut off?
3. Words: does what you hear match the captions (spot-check the flagged lines)?
4. Mix: does music or any effect compete with speech? Any clipping, pops or silence gaps?
5. Picture: anything unreadable on your normal screen? Anything that looks like a slide?
6. Understanding: answer the comprehension test (§6.2) without the script.

### 8.3 Final status (post to the owning issue or PR)

```markdown
RESULT — <film> · PR <link> · commit <sha> · MP4 <pinned raw link> (sha256 <hash>, <duration>, <size>)
Claims: <n> mapped; states shown on screen; editorial changes: <list|none>
Checks: decode PASS · full playback <PASS|NOT_ASSESSED> · 720p <PASS> · final-mix ASR <WER, notable mismatches>
AUDIBLE_REVIEW=<NOT_VERIFIED|VERIFIED by human> · owner acceptance: pending
Spend: USD <x> of <cap> (<remaining>) · uncertain calls: <none|list>
Usage: model <id>, effort <x|UNAVAILABLE>, tokens <counters + scope|UNAVAILABLE: reason>, start/end <tz>
Not done / limits: <...>    Next action: <one>
```

---

## 9. Evidence index (why these rules exist)

| Source | Lesson |
|---|---|
| [Issue #14](https://github.com/amitkarpe/video-demo/issues/14), [independent review](https://github.com/amitkarpe/video-demo/blob/1fc1ea0691ef63d2070c1dfc8c705faf07bdee8f/docs/reviews/issue-14-independent-creative-review.md) | Inventory storytelling, panel-first design and narration frozen before the visuals worked caused the failure. Test a moving slice first. Technical assurance ≠ audience assurance |
| Round 1: [#17](https://github.com/amitkarpe/video-demo/pull/17), [#18](https://github.com/amitkarpe/video-demo/pull/18) | OpenAI narration with code-drawn visuals (no generated images in these two pilots). A spend estimate is needed when the API returns no usage |
| Round 2: [#21](https://github.com/amitkarpe/video-demo/pull/21), [#22](https://github.com/amitkarpe/video-demo/pull/22) | Keep Claude's spatial "row becomes the route" reveal and Codex's legibility and full-duration browser-playback proof |
| Round 3: [#26 @75aff57](https://github.com/amitkarpe/video-demo/pull/26), [#25 @468a21b](https://github.com/amitkarpe/video-demo/pull/25) | Generated art carries the world and code carries the claims. Dense or dim panels and card-on-background scenes regress clarity. Realtime narration worked, but the originals were not preserved untouched. Machine vision reviews needed written dispositions. ~2.7 s of player progress ≠ viewing. Codex's hash-verified cached speech, ≤2-line caption cues and independent transcription cross-check are good practice |

Historical scores from these rounds were not measured with full viewing and listening. Do not reuse them as benchmarks. More image calls, longer runtime, more tokens or a newer model are not proven causes of quality.

**Maintenance:** update the dated-defaults table (§3) and §2 versions when they are rechecked, and keep everything else stable. Do not copy this file into other repositories; link to it.
