Film: an animated explainer, "Nextflow Offline — Prepare Once, Run with Confidence", for managers and engineers.
Takeaway: prepare once, verify everything, run with confidence.
Owner rules for this film (deliberate, not defects):
- High-level, generic language. No code, scripts, file names, commands, IDs, hashes or dates anywhere on screen.
- GitLab is the only repository service named or shown; no other code-hosting service may appear.
- The flow is presented as one working solution with no "proposed" or status badges. The only tag allowed is "ILLUSTRATION", used on two reconstructed moments (a missing piece stopping a run; a release rejected for a fingerprint mismatch).
Accuracy rules (the film must not break these):
- Example: a germline variant-calling test from nf-core Sarek on a small public test dataset.
- GitLab hosts the workflow code repository, container registry and datasets; content is security-scanned and the operations team reviews findings. A GitLab Runner prepares the release: code to AWS CodeCommit, container images to private Amazon ECR (exact identity), and one bundle (workflow, plugins, references, data, a fingerprint per file) to Amazon S3.
- Every file and image is read back and compared before the release is registered; a mismatch stops it.
- An approved run request in GitLab starts a uniquely identified run. AWS CodePipeline has ten gated stages; AWS CodeBuild does each stage's work; AWS Systems Manager sends commands to a private EC2 host with no internet route; private endpoints connect it only to S3 and ECR.
- On the host: the bundle is checked again, exact images are loaded into an isolated store, Nextflow runs offline, plugin downloads are off, tasks have no network, no image can be pulled.
- The pipeline confirms success, offline controls and expected outputs; the answer is PASS or FAIL with an evidence report.
- Service tiles are drawn in code with names (no logos). Artwork is AI-generated and labels are code. Frames are intentionally dark and cinematic.
