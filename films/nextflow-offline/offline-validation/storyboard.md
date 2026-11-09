# Storyboard and design rationale

## Revision 2 (island look)

One daylight low-poly world with three islands, joined only by a private underwater pipe: the **connected mainland** (internet tower, the GitLab workshop with its repository, container registry and data buildings), the **vault** (AWS CodeCommit tower, Amazon S3 silo, Amazon ECR shelf) and the **sealed island** (a glass dome over the private EC2 host and its isolated container store). A journey rail (GitLab, Prepare, Verify, Run offline, Evidence) sits at the top from chapter 2. Every move is keyed to the spoken word: `build.py` passes each line's word times to the page, and the page looks them up by word (`A(line, word)`).

| Chapter | Picture (revision 2) |
|---|---|
| 0 The missing piece | Five coloured pieces orbit a crate at the dome; one falls into the sea; the dome flashes and "Run stopped" (*Illustration*); title card |
| 1 One real workflow | Release card (nf-core Sarek, germline test); the three islands named one by one; a dashed red arc marks "no bridge to the internet" |
| 2 One trusted home | The GitLab workshop; repository, registry and data buildings light as named; a scan ring sweeps; findings card |
| 3 Prepare the release | The runner; code flies to CodeCommit, images to the ECR shelf; the crate sails to the vault and S3 rings with fingerprints; "one self-contained release" card |
| 4 Verify before trust | A read-back ring scans the vault; two checks tick; REGISTERED stamp; a red mismatch cube bounces off (*Illustration*) |
| 5 A controlled run | Approved request card; the ten CodePipeline stages tick on their words; CodePipeline → CodeBuild → Systems Manager → private EC2 host; no-route arc; the private pipe glows |
| 6 Run offline | Inside the dome: re-check ring, the isolated container store fills, Nextflow offline mode, three offline controls tick |
| 7 Proof, not promises | Evidence card; PASS beside a greyed FAIL; then the failure drill (*Illustration*): a task's packet hits the dome, stage 8 fails, RESULT=FAIL, music dips |
| 8 Run with confidence | Golden pull-back over all three islands, journey rail lights end to end, closing card |

## Revision 1


**Remembered sentence:** *Prepare once. Verify everything. Run with confidence.*

**Audience and tone.** Management and engineers. High-level, generic and confident: one working flow, with no code, IDs, dates or status hedging (owner direction). Every service appears only when its role is spoken.

**World and continuity.** One illustrated world, generated with OpenAI `gpt-image-2.6-sunburst`, with two connected places:
- **The connected side:** a warm, orderly GitLab workshop where everything is hosted, scanned and prepared.
- **The sealed side:** cool, controlled AWS spaces, ending in a windowless clean-room host.

One **release case** carries the Sarek example through every scene: packed on the workbench, inspected on the plinth, carried over the ten-arch bridge, opened in the sealed lab, and resting at the evidence. The open case is a reference *edit* of the closed one, so it is the same object. A **journey rail** at the top (GitLab → Prepare → Verify → Run offline → Evidence) shows where the viewer is.

**Division of labour.** Generated art carries place, mood and objects. Every name, service, label, check and result is editable code (HTML/SVG). Service tiles are drawn in code with their names; no logos are generated.

| # | Chapter | Narration (gist) | Picture | Motion |
|---|---|---|---|---|
| 0 | The missing piece | A workflow needs images, plugins, references and data; with no internet, one missing piece stops it; Nextflow Offline prepares first | Corridor to a sealed vault door. The release case approaches with five labelled pieces orbiting it; one goes missing and the door stays shut (*Illustration*). Title | Slow push down the corridor; the pieces orbit; the stop is a held beat; then a rewind into the title |
| 1 | One real workflow | Sarek germline test, small public dataset; one release, start to finish | Release card over the warm workshop; the journey rail appears | Card unfolds; rail draws left to right |
| 2 | One trusted home | GitLab hosts code, container images, references and datasets; scanned, Ops reviews findings | Workshop atrium with three alcoves, each labelled as it is named; a teal scan sweep; findings slide to an Operations panel | Camera visits each alcove, then pulls back for the sweep |
| 3 | Prepare the release | The GitLab Runner prepares; code → CodeCommit, images → private ECR, bundle → S3 with fingerprints | Workbench with three lit arches, each labelled as a destination; items leave the case through the arches | Each lane draws when spoken; the three join into "one release" |
| 4 | Verify before trust | Read back, compare, register; a mismatch stops here | Inspection arch over the case; a checklist and ten image tiles turn teal; REGISTERED stamp; a brief rejected branch (*Illustration*) | The scan sheet passes; ticks land one by one; the stamp lands on a beat |
| 5 | A controlled run | An approved GitLab request starts a uniquely identified run; ten gated stages; CodeBuild, Systems Manager, a private host with no internet route, private endpoints | The ten-arch bridge, arches lighting stage by stage; then a clean architecture map | Camera travels along the bridge; the map builds service by service, then holds |
| 6 | Run offline | Re-check, load exact images into an isolated store, Nextflow offline, no network, no downloads | Sealed clean-room; the case opens; images settle into isolated pods; four steps light up | Push in to the plinth; each step lights on its words |
| 7 | Proof, not promises | Success, offline controls and expected outputs confirmed; clear PASS or FAIL; evidence report | Evidence panel builds check by check to PASS | Checks land before the result |
| 8 | Run with confidence | Hosted and scanned in GitLab, prepared and verified in AWS, executed offline, evidenced; tested end to end, repeatable | Dawn panorama across the bridge, the full journey along it; the closing line; credits | Slow pull back, ending on the line |

**Alternatives rejected:**
- Slides listing services: an inventory, not a story.
- Terminal or console footage: the owner asked for no code, and it would date the film.
- Status badges such as "proposed" or "current": owner direction is one confident, working flow.
- Generated logos or service icons: generated lettering is unreliable and not licensed artwork. Code-drawn named tiles are exact and editable.
