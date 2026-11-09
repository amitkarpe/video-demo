# Video Intake Card

Status: active · Owner: Amit Karpe · Use for **every** new film or major revision in this repository.

**Why it exists:** films went wrong when an agent guessed: an unapproved brand name, wrong group names, or a brand-new theme nobody asked for. This card makes the agent confirm the few things that change the film, **once, at the start**, with a recommended default for each.

## How to run it
1. Read the request, the source repository and [the style catalog](STYLE_CATALOG.md) first. Pre-fill every answer you can.
2. Ask the owner **only what is still unknown or risky**, as answer cards with the default first (for example Claude Code's `AskUserQuestion`, up to 4 questions per card). Usually that is 2–3 cards. Never drip questions over several turns.
3. Always confirm **Q5 (style)** and **Q4 (names)**, even when you think you know them.
4. Record the answers at the top of the owning issue under "Intake" before Phase 1 starts.
5. A reply such as "go" or "default" accepts every recommended default.

## The card

### A. Topic and truth
| # | Question | Default if the owner says "default" |
|---|---|---|
| 1 | Which source repository and revision does the film explain? | The repository named in the request, at its current `main`, read-only |
| 2 | What is the **one sentence** the viewer must remember? | The agent proposes one in Phase 1 |
| 3 | Who is the audience? | 50% technical, 50% non-technical (engineers plus managers) |
| 4 | Which **names** must appear exactly (products, families, teams), and how are they pronounced? | Names from the source's README. For AWS Factory, the three families are **GitLab, MongoDB, CloudOS workspace (on ECS)**. Never invent a brand (an earlier film used an unapproved "BlueOps") |

### B. Look (reuse first)
| # | Question | Default |
|---|---|---|
| 5 | Which **house style**? | **`toy-world-3d`**: the bold toy-block Three.js world. Alternatives: `swiss-grid` (native HyperFrames 2D), with `clay-diorama` spot art on top of either. `cinematic-night` is archived and used only if named. **Do not create a new theme** unless the owner literally asks for a "new theme/style" |
| 6 | For 3D: which real objects or families must appear, and what should each one *do* (moving parts)? | Each group gets its own building, colour and idle motion (see `styles/toy-world-3d/README.md`) |
| 7 | Any colour or brand rule (company colours, logos)? | None. No logos, no generated lettering; labels are code |

### C. Story
| # | Question | Default |
|---|---|---|
| 8 | Length? | 2.5–3 min (about 400 words of narration) |
| 9 | How deep? Which step-by-step flow must be shown? | One mechanism chapter with a visible step strip (as in the SSM film's patch flow) |
| 10 | Claim stance: present everything as **working**, or mark proposed or unproven parts? | Owner's choice. If "working", mark those claims `OWNER DIRECTION` in `CLAIMS.md`; never invent results, counts or dates |

### D. Delivery and safety
| # | Question | Default |
|---|---|---|
| 11 | Public or private output? | Public `amitkarpe/video-demo`, generic: no account IDs, host names, instance or image IDs, exact times, dates, patch counts or credential details |
| 12 | Anything that must **not** be shown (production gaps, exceptions, people)? | Real production gaps are taught as a generic lesson, never as a fact about production |
| 13 | OpenAI budget? | **USD 5 per film**; the ledger stops at 90% of the cap. Recent films cost USD 0.6–1.5 |
| 14 | Phase 1 depth? | **Storyboard only** (6–10 frames in the chosen house style, plus a 10 s voice sample). A 2–3 style comparison only when the owner asks for a new look |
| 15 | Voice and disclosure? | OpenAI Realtime `marin`, disclosed on screen ("AI narration") |
| 16 | After approval: what counts as done, and who merges? | The film, captions, keyframes and QA record in one PR; the MP4 on a GitHub Release; the owner merges |

## Extra questions when the owner says "Three.js" or "3D"
- Reuse the toy-world kit (fast: about 50–60 s per full render), or build a new world? **Default: reuse the kit.** A new world costs a full design pass.
- Which chapter is the "camera tour", and which shows the mechanism up close?
- Should the families' buildings stay the same as in the last film? **Default: yes, for continuity.**

## Extra questions when the owner says "new theme"
- Confirm the extra time (a new look took several hours in earlier films, against minutes when reusing).
- Show 2–3 options as real rendered frames before any production.
- When accepted, add the new look to `styles/` and to [the catalog](STYLE_CATALOG.md), so it becomes reusable.
