# Verification — Round 2, Claude lane ("NO NAT. STILL S3.")

**VERIFIED** means measured here. **NOT_VERIFIED** means it was not done or cannot be done here. A mechanical pass is not owner acceptance.

## 1. Revision and identity
- Repo `amitkarpe/video-demo`, branch `feat/round2-claude-s3-gateway`. It was created from `995e8287847b77f81707e485f9767700bc98c162`, which equals `origin/feat/10-engineering-deep-dive` (verified before starting). The pilot commit is the PR head.
- Worktree `/Users/apple/git/worktree/video-demo-20-claude-s3-gateway`. I did not open the rival's Round-2 work.
- Model that actually ran: `claude-opus-5-5`. The owner switched to it with `/model` just before this Issue. Effort setting: **UNAVAILABLE** (not observable from inside the session).

## 2. Claims checked against the official AWS pages (read 2026-11-08)
Sources: [Gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html), [Gateway endpoints for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html), and the comparison table in [AWS PrivateLink for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html).

| Film claim | AWS wording it rests on |
|---|---|
| Reaches S3 with no NAT and no internet gateway | "access Amazon S3 from your VPC, without requiring an internet gateway or NAT device" |
| DNS resolves the bucket name to Amazon S3 public IPs | Gateway endpoints "Use Amazon S3 public IP addresses" and "Use the same Amazon S3 DNS names"; instances "access the service using its public endpoint" |
| One route: destination is the AWS-managed S3 prefix list for this Region, target is the gateway endpoint | "The destination is a prefix list for the service owned by AWS and the target is the gateway endpoint"; "prefix lists are specific to a Region" |
| Traffic stays on the AWS network | "A gateway endpoint is a gateway that you specify in your route table to access Amazon S3 from your VPC over the AWS network"; "your network traffic remains on the AWS network" |
| Not an interface endpoint (no ENI, no private IP); a route target | "Gateway endpoints do not use AWS PrivateLink, unlike other types"; interface endpoints "are represented by one or more elastic network interfaces (ENIs) that are assigned private IP addresses" |
| Not a NAT | It is a route-table target to the service and replaces the need for a NAT device (above). No address translation is claimed |
| SG and NACL must still allow the traffic (SG may reference the prefix list; NACL uses the S3 ranges plus return traffic) | "The security groups … must allow traffic to and from the service … references the ID of the prefix list"; "You can't reference prefix lists in network ACL rules, but you can get the IP address ranges" |
| The endpoint policy (default full access), IAM and the bucket policy still decide access | "The default policy allows full access"; endpoint policy "controls access to Amazon S3 from the VPC through the endpoint"; bucket-policy examples with `aws:sourceVpce` |
| Same Region; not from on-premises, other-Region peering or a transit gateway | "do not allow access from on-premises networks, from peered VPCs in other AWS Regions, or through a transit gateway" |

Not claimed: that the bucket lives in the VPC (the film labels S3 "outside your VPC"), any live environment, real prefix-list contents (IPs and CIDRs are masked), or real account, VPC or endpoint IDs.
Simplifications: one request is drawn as one packet and one response. "IAM, the endpoint policy and the bucket policy still decide access" is deliberately not phrased as "all must allow", because same-account IAM and bucket-policy grants are evaluated together and an explicit Deny anywhere wins.

## 3. File, decode, playback (VERIFIED)
- `out/round2-claude-s3-gateway.mp4`: 23,418,188 bytes, SHA-256 `13e055ba94152f4e3e889244eaaf5d2ff83fea3d2e518f5d26062c63d01b57f0`.
  ffprobe: H.264 High, yuv420p, **1920×1080**, 30 fps, 58.333 s, 1,750 frames; AAC LC 48 kHz stereo, 58.333 s.
- `out/round2-claude-s3-gateway-preview.mp4`: 716,384 bytes, 960×540, 15.0 s, SHA-256 `cfab86f8b41ea6896cd5859babf5d24f2e9f872be2024264f88119af2bbde7cb`.
- Full decode, `ffmpeg -v error -i <file> -f null -`: exit 0 with no errors for both files.
- Changing frames: `mpdecimate` keeps 1,033 of 1,750 frames as distinct. The other frames are short holds. A 20-frame contact sheet confirmed a visual change on every narration line.
- Loudness (`ebur128`): integrated −19.0 LUFS, LRA 2.6 LU, true peak −1.1 dBFS.
- QuickTime Player opened the final file with a duration of 58.33 s and advanced during playback (0 → 2.68 s).
- `npx hyperframes check`: **0 errors**. 74/74 text checks pass WCAG AA contrast. The remaining warnings are file size (one composition), the title's subtitle time on screen, two `line_unread` timings, and type-floor notes on secondary mono labels.

## 4. 720p readability (VERIFIED by viewing)
`review/frame-720p-{dns,routetable,isnt,permissions,payoff}.jpg` are scaled to 1280×720.
- Captions: 40 px at 1080p, about 27 px at 720p, on a dark box.
- Route table: 38 px rows (≈ 25 px at 720p).
- Gate cards: 26 px titles × camera zoom 1.25 (≈ 22 px at 720p).
- Payoff: 96 px.
- Secondary sub-labels inside cards are small at 720p. Every essential statement is also in the caption.

## 5. Narration and sound — **AUDIBLE_REVIEW=NOT_VERIFIED**
Claude cannot hear audio, and no human has reviewed this mix yet.
Machine diagnostic only: faster-whisper `base.en` on the final MP4 audio transcribed all 14 lines correctly, including "IPv4", "NAT", "DNS", "AWS-managed S3 prefix list", "network ACLs" and "IAM". Speech segments line up with the planned cues.
The sound design (ducked pad, whooshes, blips, gate thunks, chimes) has not been listened to by anyone. Please judge the voice and the effects balance.

## 6. Spend, time, tokens
- **OPENAI_API_SPEND_USD ≤ 0.32**: 29 `gpt-4o-mini-tts` calls (pass 1 with 15 lines, then pass 2 with 14 tightened lines), all ACK. This is a conservative pre-call estimate, 0.31902, itemized in `spend-ledger.json`; the owner's dashboard is authoritative. Cap USD 5, so **≥ USD 4.68 remains**. No other paid service, AWS call, cloud render or hosting.
- **STARTED_AT_SGT 2026-11-08 17:12:58.** The finish time and elapsed minutes are in the Issue #20 result comment, because this file is committed before the finish time exists.
- Provider input/output tokens: **UNAVAILABLE**. The app reports only context-window size (≈ 282k tokens in this whole session, which also includes Round 1) and plan-percent use on a Pro subscription.
- Inference cost: **UNAVAILABLE**. A subscription plan has no per-token bill visible to the agent.
- Revisions: script 2 (15 lines at 69 s → 14 lines at 58 s), narration passes 2 plus a pause-tightening step, renders 4 (3 drafts at standard quality, 1 delivery render), layout fix rounds 4.

## 7. Self-evaluation against the scorecard (evidence, not a verdict)
| Metric | Evidence | Known weakness |
|---|---|---|
| Technical accuracy (30) | §2 claim table; masked IDs; S3 shown outside the VPC; "decide access" wording | One-packet simplification; NAT/IGW shown as ghosts, not as real alternatives |
| Visual beauty (25) | Keyframes; consistent semantic palette; official icons | Some dense mid-scenes (permissions) at wide zoom |
| Motion and continuity (20) | One continuous world with camera moves; chip → table and row → beam transforms; rewind beat | Camera moves are eased tweens, not physically simulated |
| Narration and sound (15) | ASR-clean script; AI voice with a style prompt; synthesized SFX on every event | **Not audibly reviewed** |
| Readability (10) | §4 720p frames; contrast 74/74 | Small secondary labels |

Final judgement is Amit's side-by-side viewing.

## 8. Icon SHA-256 (unmodified, Icon-package_07312026)
```
3135793557c065d0481a3985ccc0574b36278d56a2e2c5d59107d0d28f51b827  Arch_AWS-Identity-and-Access-Management_64.svg
5a7a0cef7a9f44ccdd544564ce9076abec3024090be0d6454504c49d149ce9ec  Arch_Amazon-EC2_64.svg
b92c5101cc6565dd12df37655802279f8fba0c719279f62f93106d26750b36c6  Arch_Amazon-Simple-Storage-Service_64.svg
0666b2c8784d303a850c7cd1b40236f3d6d97012b4f4d2bad65a28c6ec614ba4  Private-subnet_32.svg
20836b5ab91e9c684dbb9f956038a3bd6472e20388829150f8aff48d12bc3e40  Res_Amazon-Route-53_Resolver_48.svg
ac5ba6de5ce1e914c9b9606cad1800692fe52ca308ef5bf3556bbebe062f7d9e  Res_Amazon-Simple-Storage-Service_Bucket_48.svg
7d99b362ba58c2382a48dcc627c573400a2fe5255db62e2b36e75db47e4dd0e5  Res_Amazon-VPC_Elastic-Network-Interface_48.svg
08ca5b0393a5df5a5342d0d9612ff27df86b413087ed15222530c3add811fbf6  Res_Amazon-VPC_Endpoints_48.svg
d31cd837a33508372a7d43a556daa0138b6e2004c94a76e2f7f8b977409659aa  Res_Amazon-VPC_Internet-Gateway_48.svg
dcb6c564523dd54b0a7475e99f926d92001b7295413b598f766922efc07bd768  Res_Amazon-VPC_NAT-Gateway_48.svg
a225286901ea59f74d52c37ccaa2660f9e2728a76cd4ee0892c29c7a386ef98c  Virtual-private-cloud-VPC_32.svg
```
