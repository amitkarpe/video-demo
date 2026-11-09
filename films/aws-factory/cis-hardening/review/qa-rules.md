Film: "CIS Hardening in AWS Factory — Fix What We Can, Accept What We Must", a public explainer for engineers and managers (about 50% technical).
Style: the native HyperFrames Swiss Grid look (grey grid paper, navy and gold, Helvetica, hard offset shadows) with three small AI clay illustrations. Labels and diagrams are code.
Public-output rule (deliberate): no CIS control numbers, no account/instance/image IDs, no dates, no credential details.
Accuracy rules:
- CIS = Center for Internet Security; the Amazon Linux 2023 benchmark has 243 checks across Level 1 (essential) and Level 2 (stricter).
- AWS Factory line: GovTech parent image -> base image (CIS fixes, security agents, latest patches) -> ECS, MongoDB and GitLab images -> test and share; reruns on a new parent image or new patches.
- Every check the scanner can test lands in one of three buckets: hardened upstream by GovTech; fixed by us in the base image (login lockout and password rules, file and log permissions, audit rules, unused networking off, signed package sources); accepted risk approved by the owner (separate disk partitions x5 and one user start-up file permission check: 6 controls, named in code). Square counts in the first two buckets are illustrative and labelled so; the accepted bucket is exactly 6.
- Accepted exceptions are approved by the owner, not by a security authority; the film must not imply otherwise.
- Each release reboots a test host and scans it against CIS Level 2 plus HCR checks; a failure not on the approved list stops the release; scanner FAILED labels are never relabelled.
- AI disclosure shown top right; chapter counter 01/06..06/06.
