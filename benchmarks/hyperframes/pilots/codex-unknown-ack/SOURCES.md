# Source-to-claim and asset record

All AWSOps source links use reviewed commit `15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9`. AWSOps and Manager were read only. The film depicts a synthetic lost-acknowledgement policy branch, not the separate positive/all-ACK branch.

| Film claim | Pinned evidence |
| --- | --- |
| Durable CALLING and UNKNOWN exist before SDK boundary | [`s3_canary.py`, `_attempt`, lines 249–287](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/src/awsops/execution/s3_canary.py#L249-L287): transaction commits CALLING and candidate result before callback returns. |
| No blind mutation retry | [`boto3_s3_canary.py`, lines 66–71](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/src/awsops/aws/boto3_s3_canary.py#L66-L71): total SDK attempts 1. |
| Reconcile the same run; unresolved CALLING stays UNKNOWN | [`s3_canary.py`, lines 353–379](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/src/awsops/execution/s3_canary.py#L353-L379). Reconciliation reads provider state and persists evidence locally; “read-only” means no provider mutation, not no SQLite write. |
| MATCH does not prove Config compliance or freshness | [`_result` / `_readback`, lines 322–347](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/src/awsops/execution/s3_canary.py#L322-L347). MATCH describes evaluated observed policy; compliance stays UNKNOWN, freshness NOT_VERIFIED, run NEEDS_REVIEW. |
| Four evidence dimensions remain separate | [Contract README](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/contracts/defence-factory/README.md), [v1 schema](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/contracts/defence-factory/v1.schema.json). |
| Control logic, not completed live acceptance | [S3 adapter limitations](https://github.com/amitkarpe/awsops/blob/15c12fb5362dd05fc4d8aaf10ebd31d3ce2935d9/docs/current/S3_CANARY_ADAPTER.md) and [Manager #19 transfer inventory](https://github.com/amitkarpe/manager/issues/19). Ledger/deployment/login and genuine human-decision acceptance remain pending in that record. |

Production brief: [#15](https://github.com/amitkarpe/video-demo/issues/15). Parent owner decisions: [#14](https://github.com/amitkarpe/video-demo/issues/14). Complete [independent creative review](https://github.com/amitkarpe/video-demo/blob/1fc1ea0691ef63d2070c1dfc8c705faf07bdee8f/docs/reviews/issue-14-independent-creative-review.md) read before design. [#12](https://github.com/amitkarpe/video-demo/issues/12) and [draft #13](https://github.com/amitkarpe/video-demo/pull/13) supplied factual limits and the failed-aesthetic reference; no storyboard, narration, layouts or captions copied. No competitor materials inspected.

## Official AWS icons

Original, unmodified SVGs from the [AWS Architecture Icons page](https://aws.amazon.com/architecture/icons/), downloaded 8 November 2026. AWS permits architecture/explanatory use under its published asset and trademark conditions; these assets are not relicensed as project-original artwork. No AWS endorsement implied. Display size changes preserve SVG content and aspect ratio.

[Official archive](https://d1.awsstatic.com/onedam/marketing-channels/website/public/shared/architecture-icon-release/Icon-package_07312026.5846e92413caa21490223536cc97f1269e44fa92.zip), SHA-256 `d2d166c453526471749d520e0db022c459abef759d2946cf2dd1d1c992dc6526`.

- `assets/s3.svg`: `Architecture-Service-Icons_07312026/Arch_Storage/64/Arch_Amazon-Simple-Storage-Service_64.svg`; SHA-256 `b92c5101cc6565dd12df37655802279f8fba0c719279f62f93106d26750b36c6`.
- `assets/config.svg`: `Architecture-Service-Icons_07312026/Arch_Management-Tools/64/Arch_AWS-Config_64.svg`; SHA-256 `6e6ee0b691d7ef2f71d81b508daa21dd154512a4e101ecc8113e161870bdb9a4`.

Custom ledger, paths, motion and typography composition are newly authored editable SVG/HTML. No generated bitmap or stock footage used.

## Software and voice

- [HyperFrames](https://github.com/heygen-com/hyperframes): Apache-2.0, pinned 0.9.20 in parent lock.
- [GSAP](https://gsap.com/standard-license/): standard no-charge license with its own restrictions; not represented as Apache. Runtime copied unchanged from pinned 3.15.0 npm distribution.
- v2 narration: [OpenAI TTS-1 HD](https://developers.openai.com/api/docs/models/tts-1-hd), Onyx, through the [Speech API](https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create). Current published rate: USD 30 per million input characters. [Deprecation notice](https://developers.openai.com/api/docs/deprecations): retirement 6 January 2027. Returned audio is cached; no API use is required for video rebuilds. AI narration is disclosed on screen. No custom voice cloning.
- v1 used Apache-2.0 Kokoro weights and MIT kokoro-onnx; its full source/provenance and voice dependencies remain preserved at commit ccc0807153da93006b55ce48b934351978ad78ed. V2 uses no Kokoro synthesis.
- FFmpeg provides local H.264/AAC encode/decode. No music or sound library used; the sound is the new OpenAI synthesized voice plus deliberate pauses.
