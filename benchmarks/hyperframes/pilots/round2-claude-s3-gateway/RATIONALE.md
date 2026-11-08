# Creative decision rationale

**Core idea: "the map is the route table."** Engineers already know VPC diagrams, but the surprising fact here lives in one route-table row.
So the film builds one continuous map, dives into the route-table chip, and then turns the matching row back into the road the packet travels.
That gives the two transformational transitions, chip → table and row → beam, and keeps the route as one continuous story instead of separate slides.

| Decision | Why | Alternatives considered |
|---|---|---|
| Open on a mystery (three struck-out badges, then a `200 OK` with no explained path, then a rewind) | The Issue's hook is a contradiction. Showing the result first and rewinding makes the viewer want the mechanism | Start with a labelled architecture diagram (rejected: lecture feel); a terminal `aws s3 cp` shot (rejected: implies a live run) |
| DNS beat before routing | The AWS docs say gateway endpoints use the same S3 DNS names and S3 public IPs. Showing the A record first explains why the route matches on a prefix list and not on a private IP | Skipping DNS (rejected: then the "not an interface endpoint" contrast has no setup) |
| Route table as a full-screen, large-type overlay | It is the key fact, so it gets the largest type (38 px rows) for 720p reading | Annotating the tiny chip in place (rejected: illegible at 720p) |
| Masked IPs and CIDRs (`52.219.·.·`), invented IDs, persistent `ILLUSTRATIVE / SYNTHETIC` | Avoids claiming real prefix-list contents or a live account; the docs' rule is about structure, not exact ranges | Real-looking full CIDRs (rejected: they could be mistaken for evidence) |
| "What it isn't" uses ghosts: a struck ENI with a private IP, and a struck NAT | Contrast teaches faster than definition, and the ghost sits where an interface endpoint's ENI would sit, in your subnet | A side-by-side comparison table (rejected: too slow inside 60 s) |
| Permissions split into the network layer (SG, NACL at the instance and subnet) and the policy layer (endpoint policy, IAM, bucket policy at the endpoint and S3) | Places each control where it acts. "Still decide access" is accurate: IAM and the bucket policy are evaluated together; any explicit Deny wins | "All must allow" (rejected: wrong for same-account IAM/bucket-policy evaluation) |
| Payoff as pure type over a faded world | The Issue's payoff line is the thesis, so nothing should compete with it | Overlaying it on the busy map (rejected) |
| Palette: night-blueprint ink, AWS group colours (VPC violet, subnet teal), mint/cyan route, amber for AWS-managed data, coral for absence/deny | Colour carries meaning consistently across the film | Single-hue monochrome (rejected: weaker semantics) |
| Voice: OpenAI `gpt-4o-mini-tts` `cedar` with a style prompt (warm senior engineer, brisk), long internal pauses tightened to ≤ 0.30 s | A natural, expressive voice within budget; tightening kept the film under 60 s without speeding up the speech | Kokoro offline voice (kept out: flatter delivery); time-stretching (rejected: artefacts) |
| Sound design synthesized in code (pad ducked under the voice, whooshes on camera moves, blips on data, thunks on gates, chimes on match and payoff) | Reproducible, licence-free, and every effect is tied to a visual event | Stock SFX libraries (rejected: licensing and reproducibility) |

Known compromises: a few secondary labels (sub-captions in cards) are small at 720p, but the burnt-in captions and the large table carry every essential statement.
The film simplifies one request into one packet and one response.
