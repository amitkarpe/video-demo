# Design rationale

**Core idea: a factory you can believe, with labels you can trust.**
The generative images build the world: the factory, the golden image, the machines, the test hangar and the night city. They carry mood, metaphor and continuity.
Every statement an engineer could check is deterministic code layered on top: lineage, gate names, CURRENT/PROPOSED status, states and blockers. This split is deliberate. Generative lettering is unreliable, and accuracy is the heaviest criterion.

| Decision | Why | Alternatives considered |
|---|---|---|
| One hero plate that already shows "gate → forge → three lines → three bays" | The establishing shot is the architecture. The camera opens on the golden disc, climbs out to the whole line and returns for the forge and the payoff | A generic data-centre still (rejected: no story); an animated diagram only (rejected: slide feel) |
| `hardened_core` generated as an *edit* of `golden_core` | The same object visibly becomes hardened, which keeps continuity across the forge transition | Two independent generations (rejected: they would not match) |
| Three machines from one generation, then cropped | One prompt gives a shared style and scale, and a shared blue "parent socket" that visually ties each child to the Hardened Base OS | Three prompts (rejected: style drift) |
| A CURRENT (solid teal) vs PROPOSED (dashed amber) visual grammar, used from the first proposal to the last | The brief's biggest accuracy risk is mixing current contracts with proposals: EventBridge discovery, the replica-set gate, ECS mock/ports/parameters, Phase B. The grammar makes the boundary visible in every frame | Only saying "proposed" in narration (rejected: frames get shared without audio) |
| "Selected CIS profile — not full benchmark compliance" and "package-only" stated in both picture and voice | These are the two easiest over-claims for a hardened-base story | Showing control IDs (rejected: precision without value for this audience) |
| A separate "states" beat (BUILT ≠ VERIFIED IN DEV ≠ ACCEPTED IN PROD) | It answers the brief's request to separate build success, DEV validation, PROD acceptance, approval and policy. It is repeated as five chips on the end card | Folding it into Phase A (rejected: the distinction got lost) |
| Phase B on a moonlit "celestial calendar" ring with a persistent PROPOSED chip | It makes "first Saturday night each month" memorable without claiming that it exists | A cron-style table (rejected: lecture) |
| A human engineer character only at the approval moment | A person makes "explicit human approval" concrete. Used once, so it does not turn into a cartoon | A mascot throughout (rejected: distracting) |
| Voice: `gpt-realtime-2.1`, `marin`, with a verbatim-reading instruction and a per-line transcript check | Realtime is OpenAI's documented successor for the deprecated TTS models. All 40 takes came back word for word. The instructions set a warm, assured documentary register | `gpt-4o-mini-tts` (works today, but is sunset on 2027-01-06); `gpt-realtime-2.1-mini` (cheaper, lower quality) |
| A synthesized score whose chord colour follows the chapters, an arpeggio pulse for the test section, and SFX tied to visual events, all ducked under the voice | Purposeful, reproducible, licence-free sound that tracks the story's energy | Stock music (rejected: licensing and reproducibility) |
| OpenAI vision and transcription as QA, applied with judgement | The vision review caught a stamp covering text, a weak subtitle and dim panels, and led to wording fixes. Two suggestions conflicted with the owner's brief ("Ops-approved" urgent release; upstream "baseline hardening") and were kept as the brief states them | Accepting every model suggestion (rejected: the reviewer saw only a summary of the rules) |

Known compromises: the DEV panels are dense in the overview shot, and the narration carries the detail. The film shows one candidate per family, so it does not depict retries, evidence storage or pointer names.
