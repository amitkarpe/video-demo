# Round 2 — Claude lane: "NO NAT. STILL S3." (ILLUSTRATIVE / SYNTHETIC)

A 58.3 s narrated, animated explainer for [Issue #20](https://github.com/amitkarpe/video-demo/issues/20).
It shows how an EC2 instance with no public IP, no NAT device and no internet gateway still reaches Amazon S3
in the same Region through an **S3 gateway VPC endpoint**. The film also says that the route does not grant access:
security groups, network ACLs, IAM, the endpoint policy and the bucket policy still decide access.
Everything shown is illustrative: invented IDs and masked IPs, with no live AWS environment and no AWS API call.

## Files

| File | What it is |
|---|---|
| `out/round2-claude-s3-gateway.mp4` | Final film: H.264 High 1920×1080, 30 fps, AAC 48 kHz stereo, 58.33 s |
| `out/round2-claude-s3-gateway-preview.mp4` | 15 s preview at 960×540 (17–32 s: DNS → route table → route) |
| `captions.srt`, `transcript.txt` | Generated from `script.json` and the measured clip lengths |
| `keyframes/01-hook.png`, `02-mechanism.png`, `03-payoff.png` | Frames taken from the final MP4 |
| `storyboard.md`, `RATIONALE.md` | Shot list, and creative decisions with the alternatives considered |
| `review/VERIFICATION.md` | Claims checked against sources, encode/decode/playback checks, 720p frames, spend, timing, self-evaluation |
| `src/index.template.html` | Editable composition (HyperFrames + GSAP). Edit this, not the generated `index.html` |
| `build.py` | Writes `cues.json`, the SRT, the transcript, `assets/mix.wav` (voice + synthesized sound design) and `index.html` |
| `script.json`, `tts_openai.py`, `tighten.py`, `timing.json`, `spend-ledger.json` | Narration script, paid TTS generator with a spend ledger, pause tightener, clip lengths, redacted spend record |
| `assets/voice-s01..s14.wav` | Final narration clips (OpenAI `gpt-4o-mini-tts`, voice `cedar`) |
| `assets/aws-icons/*.svg` | 11 official AWS Architecture Icons, unmodified |

## Rebuild

```bash
cd benchmarks/hyperframes && npm ci                    # hyperframes 0.9.20, gsap 3.15.0 (lockfile)
cd pilots/round2-claude-s3-gateway
python -m venv .venv && .venv/bin/pip install numpy==2.5.4 soundfile==0.14.0
# optional, PAID: regenerate the voice (needs OPENAI_API_KEY in the env or --env-file; stops at --ceiling USD)
#   .venv/bin/python tts_openai.py --env-file <path-to-.env> && .venv/bin/python tighten.py
.venv/bin/python build.py                              # cues, SRT, transcript, assets/mix.wav, index.html
cd ../.. && npx hyperframes check pilots/round2-claude-s3-gateway
npx hyperframes render pilots/round2-claude-s3-gateway -o pilots/round2-claude-s3-gateway/out/round2-claude-s3-gateway.mp4 -f 30 -q delivery
```

`assets/mix.wav` and `assets/gsap.min.js` are build outputs (gitignored), so run `build.py` before you check or render.
On the first render the HyperFrames compiler fetches Inter and JetBrains Mono (SIL OFL) from Google Fonts and caches them.

## Pins and provenance

- Base: `feat/10-engineering-deep-dive` @ `995e8287847b77f81707e485f9767700bc98c162` (verified).
- Node v26.12.1, FFmpeg/ffprobe 9.0.2, HyperFrames 0.9.20, GSAP 3.15.0, headless Chrome from `~/.cache/hyperframes/chrome`.
- Audio build: Python 3.12.16, numpy 2.5.4, soundfile 0.14.0. The sound design (pad, whooshes, blips, thunks, chimes, risers) is synthesized in `build.py` from a fixed seed. No sample libraries are used.
- **Narration: OpenAI `gpt-4o-mini-tts`, voice `cedar`, AI-generated.** This is disclosed on screen (an `AI-GENERATED VOICE` tag and the end credit). OpenAI lists this model for shutdown on 2027-01-06.
- AWS Architecture Icons, package `Icon-package_07312026`, used unmodified under the [AWS icon terms](https://aws.amazon.com/architecture/icons/). SHA-256 of each file:
  `Arch_Amazon-EC2_64.svg` 5a7a0cef…49ce9ec, `Arch_Amazon-Simple-Storage-Service_64.svg` b92c5101…750b36c6,
  `Arch_AWS-Identity-and-Access-Management_64.svg` 31357935…8f51b827, `Res_Amazon-VPC_Endpoints_48.svg` 08ca5b03…811fbf6,
  `Res_Amazon-VPC_Internet-Gateway_48.svg` d31cd837…7409659aa, `Res_Amazon-VPC_NAT-Gateway_48.svg` dcb6c564…bd768,
  `Res_Amazon-VPC_Elastic-Network-Interface_48.svg` 7d99b362…7db47e4dd0e5, `Res_Amazon-Route-53_Resolver_48.svg` 20836b5a…bc3e40,
  `Res_Amazon-Simple-Storage-Service_Bucket_48.svg` ac5ba6de…bbebe062f7d9e, `Virtual-private-cloud-VPC_32.svg` a2252869…ef98c,
  `Private-subnet_32.svg` 0666b2c8…ec614ba4 (full hashes are in `review/VERIFICATION.md`).
  The resource icons sit on a light disc so they read on the dark background; the icons themselves are not changed.
- Licences: HyperFrames Apache-2.0; GSAP under its [standard no-charge licence](https://gsap.com/standard-license/) (not committed; `build.py` copies it from `node_modules`).

## Spend

`OPENAI_API_SPEND_USD` ≤ **0.32**. That is a conservative pre-call upper bound of 0.31902 for 29 `gpt-4o-mini-tts` calls (two full narration passes), itemized in `spend-ledger.json`.
The API returns no usage counts, so the owner's OpenAI dashboard is authoritative. Cap: USD 5, so at least **USD 4.68 remains**.
There was no other paid service, no AWS call, no cloud render and no hosting. The API key was never printed, logged or committed.
