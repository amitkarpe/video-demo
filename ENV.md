# Environment

Status: READY (local macOS film production)

Machine facts live in `~/.config/agent/HOST.md` when available. This file records what the films need.

## Runtime
- Host: Apple Silicon macOS (observed: Node 26.12.1, FFmpeg 9.0.2, Python 3.15)
- Working directory: the repository root; each film builds from `films/<source-repo>/<film>/`

## Development Tools
- Node.js 22+ and npm: `npm ci` installs the pinned HyperFrames 0.9.20 and GSAP 3.15.0 (`package.json`, `package-lock.json`); HyperFrames downloads its own Chrome on first use
- Python 3 venv at `.venv/`: `numpy==2.5.4`, `soundfile==0.14.0`, `pillow==13.0.0`, `websockets==15.0.1`
- FFmpeg / FFprobe
- Three.js 0.187.0 is vendored per 3D film (`lib/three/`, MIT), so there is no CDN at render time

## Cloud
- Provider: none. No AWS or cloud operation is part of film work.

## External Dependencies
- OpenAI API: narration (Realtime `gpt-realtime-2.1`, voice `marin`), images (`gpt-image-2.6-sunburst`), QA (`gpt-transcribe`, `gpt-5.5`). Pricing and model availability are rechecked per film.
- GitHub: issues, PRs and Releases (the MP4 deliverables) in `amitkarpe/video-demo`.

## Optional Codex Cloud Development Setup
See [the repository-owned setup contract](docs/CLOUD_SETUP.md). Setup state: `UNCONFIGURED` (film work runs locally).

## Credentials And Secrets
`OPENAI_API_KEY` comes from the environment or an ignored `.env` passed as `--env-file`. Never commit or print it. Toolkit scripts read it only inside the paid call.
