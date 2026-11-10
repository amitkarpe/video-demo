# Showcase site

**Purpose:** one public, searchable page for every film released so far. Each film is embedded and playable, with its summary, source repository, look, length, date, lineage, key frames and transcript. Built with Astro + Starlight; search is Starlight's built-in Pagefind.

**Live:** https://amitkarpe.github.io/video-demo/

## Inputs
| File | What it is |
|---|---|
| `src/data/videos.json` | The inventory of every **published** film, with its repository, family, look, length, date, release and lineage (`series`, `order`). Films that are not approved for publication are listed in the private `amitkarpe/video-factory` `docs/showcase-pending.json`, never here (this repository is public). |
| `public/frames/<slug>-1..4.jpg` | Four small JPG frames per public film (640 px, 12/37/63/88 %); frame 2 is the card poster. Made by `scripts/frames.py` from the release MP4. |
| `src/data/transcripts/<slug>.txt` | Transcripts of factory films (public copies). Archived films use `../films/<repo>/<film>/transcript.txt` or `captions.srt`. |

## Outputs
`dist/` (static site, about 3 MB, no video), published to the `gh-pages` branch. Videos stream from this repository's public GitHub Releases. No MP4 is in Git or in Pages.

## Run
```bash
cd site && npm ci                     # once
python3 scripts/frames.py             # after adding a public film (needs ffmpeg)
npx astro dev                         # local preview at http://localhost:4321/video-demo/
./deploy.sh                           # build and publish to gh-pages (fast-forward push, never force)
```

## Add a released film
1. Publish its MP4 as a public release in this repository (`film-<repo>-<film>`, the factory's `publish_showcase.sh`).
2. Add one entry to `src/data/videos.json` with `public: true`, the `mp4` and `release` URLs, `durationSec`, `series` and `order` (optional: `repos`, other repositories the film shows, each listed in `repos` at the top). Use neutral names (no model or vendor names) and no exact identifiers.
3. `python3 scripts/frames.py <slug>`, then `./deploy.sh`.

## Verify
- `npx astro build` reports 0 errors, and Pagefind indexes every page.
- On the live site, a video page plays and seeks in Chrome and Safari.
- `deploy.sh` refuses to publish any MP4, MOV or WAV file, and any file over 2 MB.

## Limits
- **Safari needs `<source type="video/mp4">`.** GitHub serves release assets as `application/octet-stream`. Safari (macOS and iOS) refuses that with a bare `<video src>`, but with the type hint it streams and seeks (tested in Safari 26.1). Keep the `<source>` element.
- Release downloads redirect to a signed URL that lasts about an hour. The player reloads once and continues if a long pause outlives it.
- GitHub Pages limits: 1 GB site, 100 GB a month of soft bandwidth (the videos are not counted: they come from Releases).
- `deploy.sh` exists because the agents' token cannot push workflow files. `pages-workflow.yml.example` is the Actions version: copy it to `.github/workflows/` to switch.
