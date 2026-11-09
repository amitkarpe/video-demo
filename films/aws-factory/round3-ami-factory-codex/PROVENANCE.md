# Asset provenance and rights

No stock photo, third-party video clip, music recording, private architecture asset or private source-code excerpt is used.

| Asset | Origin | Inputs / edits | Rights and receipt |
| --- | --- | --- | --- |
| `assets/factory-day.png` | OpenAI Images API, requested `gpt-image-2.6-sunburst`, 1536×1024 high | Exact original prompt in `prompts/factory-day.txt`; no reference image | Generated project output under the account's applicable OpenAI terms; request ID, token usage, CLI hash and output hash in `api-spend.json` |
| `assets/factory-night.png` | Same model, Images edits endpoint | Day image plus `prompts/factory-night.txt`; same geometry, night lighting | Same terms; reference-image hash and output hash recorded |
| `assets/voice-*.wav` | OpenAI Speech API, `gpt-4o-mini-tts`, `cedar` | Exact text, voice instructions, PCM output and usage in ledger; expanded acronyms in `script.json` | Synthetic built-in voice; no voice cloning or impersonation |
| Original machine SVGs, labels and paths | Code-authored for this film | Editable deterministic overlay in `scene.html.template` | Original project work; these are not represented as generated image assets or official AWS icons |
| Score and transition chimes | Procedural synthesis in `build.py` | Original deterministic oscillators and envelope design; no samples | Original project work |
| Caption text | Approved original display script | Anchored to Whisper timestamps, with explicit editorial alignment log | Transcription is a QA aid; public display wording remains source-grounded |
| Fonts | Host Arial/Helvetica/sans-serif stack | Rendered into output pixels | Font binaries are not redistributed |

This record states asset origin, not a new blanket license grant. Generated media is provided as this project's output under the applicable service/repository terms. It does not claim exclusivity, third-party endorsement or that generated imagery depicts an actual facility.

## Tooling

HyperFrames 0.9.20 is declared Apache-2.0 in the installed package. GSAP 3.15.0 uses the [Standard No Charge License](https://gsap.com/standard-license/), which permits commercial code-authored use. Runtime dependencies are installed from the repository lockfile, not copied into this commit. The bundled imagegen CLI is used without modification. Python API dependency versions are pinned in `requirements-api.lock`; no environment or authentication state is distributed.

## API accounting

| Model | Calls | Usage-priced USD |
| --- | ---: | ---: |
| `gpt-image-2.6-sunburst` | 2 | 0.096968 |
| `gpt-4o-mini-tts` | 26 | 0.0737538 |
| `whisper-1` | 1 | 0.0268 |
| `gpt-4o-transcribe` | 1 | 0.0011875 |
| `gpt-4.1-mini` | 1 | 0.0096444 |
| **Total** | **31** | **0.2083537** |

Every request reserved budget before dispatch. Automatic retries were disabled. No uncertain request was repeated. No Sora, video-generation or GPT Live request was made. Prices and the available-model checks are dated 2026-11-08; the ledger contains token/duration evidence and calculation bases. Credits count as spend. The remaining allowance is $9.7916463.
