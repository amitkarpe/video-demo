# Specification

Status: ACTIVE
Context: not specified; local mock only
Environment: LOCAL macOS

## Objective and outcome

Produce and revise a 60–90 second, at least 720p, English narrated and captioned video of the fictional workflow in [Issue #1](https://github.com/amitkarpe/video-demo/issues/1). Deliver editable source and reproduction instructions in one PR, and retain a playable MP4 locally.

## Authorized

The accepted [project intent](intent/0001-project-bootstrap/intent.md), Issue #1, and current user instruction authorize local implementation and verification, installation of necessary free tools on the Mac, and creation of one PR in `amitkarpe/video-demo`. They do not authorize merge.

## Requirements and boundaries

- Show detection, AI investigation, human approval, simulated SSM remediation, and verification with audit evidence; label the video clearly as a simulation.
- Include English synthesized narration and readable English captions. Demonstrate a minor wording revision and re-export without paid credits or a watermark.
- Do not perform AWS calls or use credentials, real incident data, paid services, new infrastructure, or actual security changes.
- Keep editable sources, captions, and repeatable instructions in Git. Store the MP4 locally unless appropriate for Git.
- Preserve unrelated work and stop for unexpected permissions, sensitive data, or scope changes.

## Plan and verification

1. Preflight the actual Mac tools and desktop access.
2. Generate the five scenes, narration, captions and MP4 using free local tools.
3. Play the export, inspect readability and mock labeling, and repeat export after a wording revision.
4. Review the full diff and create one PR with evidence and limitations. Generated local artifacts are retained; no cleanup or merge is implied.
