# NO NAT. STILL S3.

**Watch:** [pilot.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-concepts-s3-gateway-round2-codex/pilot.mp4) (sha256 `697839bab05d…`) · [preview.mp4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-concepts-s3-gateway-round2-codex/preview.mp4) (sha256 `abc9b46ec335…`) — video files live on the film's [GitHub Release](https://github.com/amitkarpe/video-demo/releases/tag/film-aws-concepts-s3-gateway-round2-codex), not in git. Paths such as `out/*.mp4` below are where a local build writes them.


A 46-second, 1080p/30 fps technical animation for [issue #19](https://github.com/amitkarpe/video-demo/issues/19).
An amber packet travels from private EC2, through the route-table decision and
S3 gateway endpoint, to a same-Region S3 bucket outside the VPC. The film then
separates connectivity from access authorization.

**Review:** [Full MP4](https://github.com/amitkarpe/video-demo/releases/download/film-aws-concepts-s3-gateway-round2-codex/pilot.mp4) · [12-second mechanism preview](https://github.com/amitkarpe/video-demo/releases/download/film-aws-concepts-s3-gateway-round2-codex/preview.mp4) ·
[Captions](captions.srt) · [Transcript](transcript.txt) · [Local player](player.html)

**Status:** delivered for human review. `AUDIBLE_REVIEW=NOT_VERIFIED`.
No AWS environment was accessed. The persistent on-screen label identifies
the film as illustrative. No first-round or rival creative assets were used.

## Storyboard and creative choices

| Time | Image and movement | Purpose |
| --- | --- | --- |
| 0–7.6s | Large two-line hook; 2.5D EC2 and S3 enter a single regional map. Three missing internet components remain visible. | Establish the apparent contradiction immediately. |
| 7.6–12.2s | Camera moves toward EC2; a DNS callout maps the service name to S3 service IPs. | Separate name resolution from route selection. |
| 12.2–22.1s | The route-table symbol expands into a destination/target row. The regional S3 prefix list highlights. A colored path draws toward the gateway. | Make the matching rule tangible without invented IPs or IDs. |
| 22.1–30.2s | Camera follows the same amber packet to S3. A green return packet crosses the route. The complete VPC boundary returns to view. | Preserve spatial continuity and distinguish the gateway from an interface endpoint/NAT. |
| 30.2–41.3s | S3 arrival expands into two access-check groups. A moving indicator crosses traffic rules and policy evaluation. | Prevent network reachability from being mistaken for authorization. |
| 41.3–46s | The access panel contracts back to the map; the packet runs the path again beneath the payoff. | Leave the viewer with one route and one precise qualification. |

The palette uses warm paper, dark ink, teal networking, amber compute/packets,
and green storage. A continuous world was selected over scene-by-scene cards
so the viewer retains the endpoints' locations. A network-console recording
was rejected because it would obscure the routing concept and suggest live
evidence. Abstract IP labels avoid false precision. Gateway geometry is a
route symbol, not a depicted ENI or physical appliance.

The original 98 BPM harmonic pulse is quiet under the speech. Brief tonal
accents coincide with key transitions. The OpenAI Nova narration is cached
per complete caption unit. No stock music or generated background images are
needed. See [source claims and licenses](SOURCES.md).

## Rebuild without API calls

From this repository's `benchmarks/hyperframes` directory:

```sh
npm ci --ignore-scripts --no-audit --no-fund
sh pilots/round2-codex-s3-gateway/render.sh
python3 pilots/round2-codex-s3-gateway/check_voice_budget.py
python3 pilots/round2-codex-s3-gateway/verify.py
```

Requires Node/npm, Python 3, FFmpeg/ffprobe, a supported local Chromium, Arial
and Menlo. The parent `package-lock.json` pins HyperFrames 0.9.20 and GSAP 3.15.0.
The verified host used Node 26.12.1, npm 11.20.0, Python 3.15.2, FFmpeg 9.0.2,
and HyperFrames' cached Chrome 152 renderer on Apple Silicon macOS.
No extra Python package is required. No new dependency was added to the lockfile.

`scene.html.template` owns the editable SVG artwork and GSAP choreography.
`script.json` owns narration/caption text. `build.py` verifies the cached speech
receipts, derives the cue timing, generates the original score and writes
`index.html`, `timing.json`, `captions.srt` and `transcript.txt`.
`render.sh` renders locally and normalizes the final AAC mix while copying the
video stream unchanged. The pipeline does not contact speech APIs on a rebuild.

For a local player, run `python3 -m http.server 8769 --bind 127.0.0.1` in this
pilot directory and open `http://127.0.0.1:8769/player.html`. The server is local
only. The MP4 also plays independently in a normal media player.

## Spend guard

Twelve OpenAI `tts-1-hd` / `nova` requests used **669 input characters**:
**USD 0.02007**, leaving **USD 4.97993** of this lane's USD 5 media cap.
This is the character-metered amount at the published USD 30/million rate;
invoice reconciliation is unavailable. Credits do not discount the recorded
usage. No paid image, video, transcription or review call was made.

`generate_voice.py` requires `--approved-issue-19` and an existing authorized
environment credential. It reserves cost atomically before each request,
stops before the next call would breach the cap, and refuses to proceed after
an uncertain call. It never automatically retries. Completed narration is
reused by hash. Streaming WAV headers are finalized locally without changing
PCM samples. The dated per-call receipts are in `openai-spend.json`.

`check_voice_budget.py` verifies both stop cases with networking mocked to fail
if called. `budget-test-fixture.json` is synthetic test input, not a spend receipt.
Do not regenerate speech merely to rebuild the movie; new text needs a fresh
budget review and an explicit ledger decision.

## Verification and self-assessment

See [machine results](verification.json), [production record](production.json)
and the selected [hook](keyframes/hook.png), [mechanism](keyframes/mechanism.png)
and [payoff](keyframes/payoff.png) frames.

| Scorecard area | Evidence and remaining judgment |
| --- | --- |
| Accuracy / 30 | Official AWS claim map; region and VPC boundaries remain distinct; routing and permissions are separate. No live execution claim. |
| Art direction / 25 | Original 2.5D paper/ink visual system and official unmodified service icons. Aesthetic quality remains Amit's judgment. |
| Motion / 20 | Camera moves, route-table expansion, drawn path, forward/return packets and S3-to-access transition. Encoded crop differences confirm real motion. |
| Narration / 15 | OpenAI Nova plus original restrained score; measured final loudness and peak; cue timing comes from actual WAV lengths. Pronunciation, naturalness and sound balance require human listening. |
| Readability / 10 | Burned-in captions, 12 nonoverlapping cues, maximum 19.52 characters/second. Encoded 720p inspection covers hook, DNS, route, packet, policies and payoff. |

There were three full renders: initial composition, route/packet/readability
corrections, and a final DNS framing correction. The spoken script had one
recorded version and no regeneration. One disposable one-second render
established actual browser/encoder capability before any paid speech request.

The original first-round work remains at its original branch/worktree. This
lane uses `feat/round2-codex-s3-gateway`, based on pinned benchmark commit
`995e8287847b77f81707e485f9767700bc98c162`. Issue #19 explicitly authorizes this
separate Round-2 scope and its bounded speech spend; the older root spec and
issue #15 phase gate do not describe this authorized round. Nothing is merged.
