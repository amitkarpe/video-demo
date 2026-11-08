# Sources and asset rights

Checked on 8 November 2026 before recording. This is an illustrative IPv4,
same-Region, general-purpose S3 bucket scenario. No AWS APIs were called.

| Film claim | Primary source and qualification |
| --- | --- |
| Private EC2 can access S3 without public IPv4, NAT or an internet gateway | [Gateway endpoints overview](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html). DNS and the relevant network/access configuration must work. |
| S3 DNS resolves to service IP addresses | [S3 endpoint comparison](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#types-of-vpc-endpoints-for-s3): gateway endpoints use S3 public service addresses and the same S3 DNS names. Public destination addressing does not mean the packet must use an internet gateway. |
| Regional AWS-managed S3 prefix-list destination targets the gateway endpoint | [Gateway endpoint routing](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html#gateway-endpoint-routing). The endpoint association installs the route in selected subnet route tables. Longest-prefix matching still applies. The film assumes no more-specific conflicting route. |
| Traffic stays on the AWS network | [S3 endpoint types](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#types-of-vpc-endpoints-for-s3). This is also true for certain other AWS paths; the film does not claim exclusivity. |
| Gateway is not an interface ENI/private endpoint IP or a NAT | [Endpoint comparison](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) distinguishes the route target from interface endpoints, which use ENIs and private IPs. [S3 gateway considerations](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#gateway-endpoint-considerations) describe the instance private source address reaching S3. |
| Instance security groups and subnet NACLs must allow traffic | [Gateway endpoint security](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html#gateway-endpoint-security). NACLs cannot reference a prefix list; they require service CIDRs and suitable return traffic. The video does not show a misleading NACL prefix-list rule. |
| IAM, endpoint policy and bucket policy still govern object access | [S3 gateway endpoint access policies](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html). These policies are evaluated together; the drawing does not mean every layer must independently contain an explicit Allow. Endpoint routing does not grant permissions. |
| Scope is one Region and this VPC | [S3 gateway considerations](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#gateway-endpoint-considerations). The endpoint cannot extend through on-premises, peering, VPN, Direct Connect or a transit gateway. No such path is depicted. |

The animated packet, gateway ring and 2.5D map are explanatory symbols, not
physical appliance placement, an AWS execution trace, or a deployment recipe.
The DNS name is the documented regional naming form; no account, bucket,
subnet, address or endpoint ID is taken from a real environment.

## Original and third-party assets

- All composition, diagram geometry, transitions and soundtrack are original
  to this Round-2 lane. No rival implementation was opened or reused.
- `assets/ec2.svg` and `assets/s3.svg` are unmodified official AWS SVGs from the
  July 2026 [architecture icon package](https://aws.amazon.com/architecture/icons/).
  AWS permits these assets for architecture diagrams and presentation material.
  The download URL, archive hash and individual hashes are in
  [assets/aws-icons-provenance.json](assets/aws-icons-provenance.json).
  The icons retain AWS ownership; they are not relicensed as original art.
- Arial and Menlo are installed system fonts. Their binaries are not distributed.
- HyperFrames 0.9.20 is Apache-2.0. GSAP 3.15.0 uses its
  [standard no-charge license](https://gsap.com/standard-license/).
  The existing parent npm lockfile pins both. No additional package was introduced.
- `assets/score.wav` is generated deterministically from elementary oscillators
  by `build.py`. There are no external music samples or stock-audio obligations.

## Speech

OpenAI `tts-1-hd`, `nova`, WAV, speed 1.0. The film visibly identifies the voice
as AI-generated. [Speech model price](https://developers.openai.com/api/docs/models/tts-1-hd):
USD 30 per million input characters. Twelve calls used 669 characters, USD
0.02007 at list price, regardless of credits. Each call was reserved before
submission and has a request ID and input/output hash in `openai-spend.json`.

The model is deprecated but was available for this authorized one-off run.
Cached WAVs make the film rebuild independent of future model availability.
[Deprecation information](https://developers.openai.com/api/docs/deprecations).
There is no ongoing service dependency or automatic paid regeneration.
