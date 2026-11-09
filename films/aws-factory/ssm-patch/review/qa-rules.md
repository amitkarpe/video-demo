Film: "Patching Running Servers in AWS Factory — Scanned Is Not Patched", a public explainer for engineers and managers (about 50% technical).
Style: a 3D toy-block world built with Three.js (green island, primary colours, hard sun), with HTML cards, pinned labels, a patch-flow strip and captions in Nunito.
Public-output rule (deliberate): generic only; no account, host names, IDs, schedule times, dates or patch counts. The owner directed that the flow is presented as working.
Accuracy rules:
- Two roads: build fresh (the factory bakes the latest patches into a new image) and patch in place (AWS Systems Manager Patch Manager on running servers).
- AWS Factory builds one hardened base image and from it three families: GitLab (orange towers with a pipeline), MongoDB (green vault members in a replica ring), CloudOS workspace on ECS (blue worker nodes with containers and a crane). Each server's tag names its family; that tag is its patch group.
- Baseline: security updates at once; other updates after 7 days; database and container-engine packages never patched in place (rolling upgrade or new image only).
- Patch flow: scan every weekend night; if nothing is missing the group is compliant (MongoDB shown); if updates are missing they install early next morning in that group's own window, one group after another (GitLab, then CloudOS); most updates need no reboot (GitLab); a new kernel's reboot waits for the group's planned downtime window (CloudOS), then the server comes back green.
- The trap: a server whose tag matches no group is scanned but never installed. "Scanned is not patched."
- Reports list each server's patch result and flag any server with no patch data. Rule changes go to one server first, then every group; the owner approves every production change.
- AI disclosure top right; chapter counter 01/07..07/07 (hidden on the close).
