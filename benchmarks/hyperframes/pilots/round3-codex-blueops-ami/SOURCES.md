# Source and claim boundaries

The controlling public brief is [video-demo #24](https://github.com/amitkarpe/video-demo/issues/24). Its Round 3 authority covers this original local film, metered media APIs, validation, one draft PR and a final issue report. No infrastructure action was performed.

The authorized private implementation source was inspected read-only at a pinned revision on 2026-11-08. Its architecture direction, validation contracts and DEV-to-PROD acceptance distinctions informed this synthesis. No private source text, identifiers, diagrams, evidence logs, assets or vendor inventory is distributed here. The private repository's operational authority was not adopted as film-production authority. This package contains original explanations of the public requested story.

| Film claim | Evidence class | What it does not assert |
| --- | --- | --- |
| Golden AL2023 → Hardened Base OS → three direct child families | Public brief plus current architecture contract | No extra container-runtime parent or fourth core family |
| Selected hardening and package-only agents | Current source boundary | No full CIS compliance, zero-vulnerability finding or baked-in PROD registration |
| GitLab workflow gates | Required acceptance, with limited current cold-boot/reboot scope | No authenticated repository workflow or PROD cutover proved by this film |
| MongoDB process/CRUD/dump-restore | Standalone smoke scope | No healthy replica set, cluster recovery or complete PROD backup policy |
| Higher-confidence MongoDB replication/recovery | Proposed gate | No current cluster-ready claim |
| ECS nonzero placement on exact image | Required category gate | No task placement on the candidate proved by a build badge |
| Mock workloads, network flows, scoped Parameter Store reads | Proposed illustrative demo suite | No live test receipts |
| Private launch, encryption, launch permission, usable backing snapshots/KMS | Required effective-access proof | No blanket claim that every shared AMI needs a separate snapshot-sharing operation |
| Phase A DEV → PROD acceptance → Ops approval | Controlled release contract | No automatic promotion from DEV validation |
| Phase B weekly candidates / first Saturday night monthly promotion | Proposed future operating policy from public brief | No current unattended PROD rollout; governance approval remains prerequisite |
| Urgent critical-vulnerability release | Ops-approved exception in public story | No bypass of evidence or approval |
| Prior known-good plus tested data recovery | Required recovery discipline | Image rollback alone does not restore application data |

## Public technical references

- [EC2 Image Builder overview](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html): image pipeline concepts.
- [Image Builder workflows](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-image-workflows.html): distinct build, test and distribution workflows. Generic service capability is not proof of project implementation.
- [Share an AMI with specific accounts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharingamis-explicit.html): launch permissions, backing storage and encrypted-key considerations. Effective launch proof matters more than a policy observation alone.
- [Parameter Store access setup](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-setting-up.html): authorized scoped access. The demo proposes these reads; it does not make them.

## API references, checked 2026-11-08

- [GPT Image 2.6 Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst) and [image generation](https://developers.openai.com/api/docs/guides/image-generation).
- [Speech API](https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create), [text to speech](https://developers.openai.com/api/docs/guides/text-to-speech), and [GPT-4o mini TTS](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts).
- [Whisper](https://developers.openai.com/api/docs/models/whisper-1), [GPT-4o Transcribe](https://developers.openai.com/api/docs/models/gpt-4o-transcribe), and [GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

The requested image model and selected speech/QA models were checked through the authenticated model endpoint before use. The speech model remains available at production time but is deprecated with an announced 2027-01-06 shutdown. Cached WAVs make the offline rebuild independent of future API availability. Do not infer indefinite model support from this successful run.
