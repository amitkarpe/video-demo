# Storyboard — "NO NAT. STILL S3." (58.3 s)

One continuous world (Region → VPC → private subnet → gateway endpoint → AWS network → S3). A virtual camera moves over it.
Times come from `cues.json`. Captions match the narration word for word.

| # | Time (s) | Narration | Picture | Camera / transition |
|---|---|---|---|---|
| 0 | 0.0–1.4 | (title, sub boom) | "NO NAT. / STILL S3." kinetic type | Title punches through into the world (scale-out) |
| 1 | 1.4–4.4 | This EC2 instance has no public IP. | EC2 inside the private subnet; badge `✕ PUBLIC IPv4: none` | Slow push on the instance |
| 2 | 4.6–6.8 | No NAT. No internet gateway. | Badges `NAT: none`, `INTERNET GATEWAY: none`; ghost NAT and IGW icons struck out in coral | Pull back, slight roll |
| 3 | 7.1–10.0 | Yet it still reads from Amazon S3. | A packet streaks to S3 and a `200 OK` comes back. The path is not explained yet | Wide establishing shot |
| 4 | 10.4–11.8 | So what's the path? | `◀◀ REWIND`, scan lines; the streak rewinds; a big `?` | Time-reverse beat |
| 5 | 12.2–16.8 | DNS first: the bucket name resolves to Amazon S3's public IP addresses. | Query bubble `my-bucket.s3.ap-southeast-1.amazonaws.com ?` travels to Amazon DNS (Route 53 Resolver); answer `A 52.219.·.·, an Amazon S3 public IP`; the packet is born with `dst 52.219.·.·` | Move to the DNS corner |
| 6 | 17.1–19.0 | Then the route table decides. | Route-table chip | **Transform 1:** the camera dives into the chip and it unfolds into a full-screen route table |
| 7 | 19.3–26.2 | One route does it. Destination: the AWS-managed S3 prefix list for this Region. Target: the gateway endpoint. | Probe `dst 52.219.·.·` tests `10.0.0.0/16 → local` (✕), then `pl-0123abcd (com.amazonaws.ap-southeast-1.s3) → vpce-0a1b2c3d` (✓); the prefix list fans out into masked CIDR chips; ghost row `0.0.0.0/0 — none` | Destination cell (amber), then target cell (mint) |
| 8 | 26.5–30.6 | Matching traffic takes that route and stays on the AWS network. | The packet runs EC2 → gateway endpoint → AWS network → S3 | **Transform 2:** the matching row becomes the road; the table collapses into a glowing beam, then a wide shot |
| 9 | 31.1–36.8 | It's not an interface endpoint: no network interface, no private IP. Not a NAT either. | Ghost interface-endpoint ENI `10.0.1.57` struck out; card: not an interface endpoint / not a NAT / a route-table target; fine print: same Region, not usable from on-premises, other-Region peering or a transit gateway | Medium-wide |
| 10 | 36.9–38.7 | Just a route target. | The endpoint pulses; pill `pl-0123abcd → vpce-0a1b2c3d` | Push in on the endpoint |
| 11 | 39.3–41.8 | But a route is not a permission. | The packet runs again and a red shutter slams down at S3: `route ≠ permission` | Wide; impact sound |
| 12 | 42.1–46.6 | Security groups and network ACLs must still allow the traffic. | SG ring around EC2 (`out: TCP 443 → S3 prefix list`); NACL gate on the subnet edge (`443 to S3 ranges + return`) | Instance side |
| 13 | 46.8–51.7 | IAM, the endpoint policy and the bucket policy still decide access. | Endpoint policy (`default: full access`), IAM policy, bucket policy (`no Deny for this request`); the shutter lifts; `200 OK`; note `any explicit Deny → 403 AccessDenied` | S3 side |
| 14 | 52.4–55.3 | The route changed. The permissions didn't disappear. | World fades; two lines of type (mint, then amber) | Payoff |
| 15 | 55.3–58.3 | (music tail) | End card `NO NAT. STILL S3.`, sources, ILLUSTRATIVE / SYNTHETIC, AI-voice and icon credit | Fade to black |

Persistent: `ILLUSTRATIVE / SYNTHETIC` (top left), chapter chip 01–06 and `AI-GENERATED VOICE` (top right), burnt-in captions.
