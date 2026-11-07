# Storytelling direction and evidence

Amit's feedback: the first benchmark looked like a presentation, even after a cinematic background was added. Future demonstrations should show people, emotions, cause and effect, and action—not just large headings, an anonymous silhouette, and a diagram. Kokoro is acceptable as an initial local voice, but the earlier Cedar sample was preferred. Keep voice, animation, captions and factual fidelity independently reviewable.

## Fictional story in this experiment

A fictional company discovers an intrusion. A CEO asks how it was missed. A CISO explains alert overload; an engineer asks for evidence instead of more noise. The narrator introduces the POC as an isolated training-lab workflow. A CISO asks who controls the tools; the engineer describes the fixed policy gate and tool-less model. The characters are fictional and the story does not claim the POC detected, blocked or repaired this invented incident. AI-assisted attacks are possible; do not claim most attackers use agents or that the POC replaces engineers.

## What the repository actually establishes

- [README](https://github.com/kcloud1/agentic-pentest-poc/blob/main/README.md): scanners operate on intentionally vulnerable targets in isolated Docker training environments; reporting contains OWASP mapping, scores, model verdicts and remediation.
- [Demo](https://github.com/kcloud1/agentic-pentest-poc/blob/main/docs/DEMO.md): the model has no tools, chooses among fixed actions, a policy gate checks choices, and audit records can be verified. A human-readable report enables review; do not imply a human approval step is implemented as the policy gate.
- [Recorded sample and accuracy](https://github.com/kcloud1/agentic-pentest-poc/blob/main/docs/sample/README.md): results and model latency vary, and the measured lab run did not find every known issue. These numbers are lab measurements, not a claim of production coverage or faster incident response.

## Production learning

HyperFrames provides deterministic HTML/media composition, not an actor generation model. A still-image shot with camera movement is a motion-comic, not a talking avatar or live-action scene. To approach a HeyGen-style human presenter, supply separately generated speaking footage or an audio-driven talking-face model, then use HyperFrames to edit the scenes and captions. Any additional model needs separate evaluation of commercial/model licenses, Mac compatibility, visual quality, latency, privacy, and voice synchronization. The [SadTalker project](https://github.com/OpenTalker/SadTalker) describes audio-driven talking faces and documents Mac installation; [LivePortrait](https://github.com/KlingAIResearch/LivePortrait) documents Apple Silicon support and uses a driving motion source. The follow-up used SadTalker on this Mac to animate each of the CEO, CISO and engineer dialogue lines using Kokoro audio and generated portraits. It required downloaded weights and compatibility patches for current NumPy, torchvision and Apple MPS; it took several minutes and showed a softer face than the source image. This single test does not establish production readiness or quality. LivePortrait was researched, not run.

Do not conflate an open-source renderer with HeyGen's separate hosted avatar generation product or its pricing. Record actual costs and obtain consent before services or paid model usage outside the approved scope.
