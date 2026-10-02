---
name: explain-format-picker
description: >
  Before explaining, teaching, demonstrating, or comparing anything, decide
  which output format will be easiest for the user to understand — STE-style
  text, a diagram, an interactive HTML page, or an explainer video — then
  produce it in that format, combining formats when one is not enough. Use
  whenever the user asks you to explain a concept, system, paper, codebase,
  process, dataset, or decision; or says "help me understand", "walk me
  through", "how does X work", "compare X and Y", or asks for an explanation
  as a diagram, web page, or video — even if they don't specify a format.
  Methodology distilled from Andrej Karpathy's note on upgrading LLM output
  formats (prose → diagrams → web pages → explainer videos).
version: 1.0.0
license: MIT
---

# Pick the Format Before You Explain

## Why this exists

The default way to explain is writing long prose. Prose is good for precision, but it struggles with structure and relationships, can't show what happens when you change something, and is worst at processes that unfold over time. LLMs can now generate diagrams, pages, and videos so cheaply that switching formats when prose isn't enough is nearly free. The user's work is increasingly supervision and understanding rather than hands-on doing — so how fast the output can be understood matters more than how polished the output is.

The goal is user understanding — not defaulting to prose, and not showing off media capabilities.

## Boundaries and priorities

- If the user explicitly specifies a format, use it, plus a short text addendum when needed. If the user wants a short answer, plain text, or low-bandwidth output, do not escalate on your own.
- Do not ask the user "which format do you want?". Unless missing information affects correctness, choose sensible defaults yourself.
- Judge the format yourself using this skill; do not call external classification or recommendation services. Verifying facts and generating artifacts may use tools the host allows.
- Follow the host's permission and safety rules. This skill grants no extra tool permissions.

## The four formats

| Format | Good for | Not good for |
|---|---|---|
| Text (STE style) | Conclusions, definitions, precise constraints, steps, warnings, short Q&A | Long paragraphs describing complex relationships or continuous change |
| Diagrams / images | Structure, relationships, flows, comparisons, data, spatial layout | When there is little information and drawing costs more effort than prose |
| Interactive HTML | Tuning parameters, comparing options, layered inspection, active exploration | When there is only a layout need and no interaction benefit |
| Explainer video | Abstract mechanisms, continuous change, spatial transformation, complex topics that need to be watched in sequence | When a static diagram suffices, or the user mainly wants precise reference info |

The ladder expresses expressive power and production cost, not quality ranking. Further down is more intuitive, and more time-consuming.

## Routing: find the comprehension blocker first, then pick

Decide silently; do not output your reasoning and do not make the user fill a questionnaire. First ask: what is the user's main obstacle to understanding?

| Main obstacle | Default choice |
|---|---|
| None — a short answer or a few steps suffices | Text |
| Relationships, structure, comparison, data, spatial layout | Text + diagram |
| User needs to change conditions and see results to get it | Text + interactive HTML (chart embedded in the page) |
| Abstract, and the key is a change unfolding over time that must be watched in order | Text + video |
| Both exploration and a guided view of one key change | HTML or video as primary, the other as supplement |

Three common misjudgments:

- **Having a timeline does not mean needing a video.** Historical events get a timeline. Only continuous rotation, phase change, algorithm state evolution — where "the change itself is the explanation" — need dynamic demo.
- **Complex does not mean video.** Complex taxonomies usually suit a structure diagram; parameter sensitivity usually suits an interactive page.
- **When both HTML and video fit, ask who holds control.** If the user needs to change conditions themselves, choose HTML. If the user needs to be guided through a change, choose video.

When unsure, pick one tier lower. If the user finds it insufficient, escalate.

## Pre-upgrade checklist

Before moving up one tier, confirm all five hold — otherwise stay at the current tier:

1. The new format solves a specific comprehension blocker.
2. A simpler format cannot do the job equally clearly.
3. Production time, viewing time, and interaction burden are proportional to the benefit.
4. You can actually generate a usable artifact, not merely describe one.
5. No user constraint on format, duration, device, or accessibility is violated.

For custom artifacts that pass the checklist, go boldly. One-time use is no reason to cut corners. Video is the most expensive: when the signal is weak (the user is just casually asking), deliver text and a diagram first, then offer in one sentence "I can make this into a video if you'd like".

## Combining formats: each carries a different job

The default is "one primary format + short text". Add another format only when it brings an independent benefit. Never stuff the same essay into a diagram, a page, and a video.

| Combination | Division of labor |
|---|---|
| Text + diagram | Text gives conclusions and limits; the diagram shows relationships or evidence |
| Text + HTML | Text gives the core rule; the page lets the user operate and verify |
| Text + video | Text gives searchable conclusions; the video shows the key change |
| HTML + video | Video builds intuition first; the page lets the user change conditions to test it |

Text is almost always kept: even when the primary artifact is a diagram or video, attach a short text conclusion preserving formulas, parameters, steps, and applicability limits. It is the fastest and the most searchable.

## Generation

Read the detailed rules for each format on demand:

- Text: `references/ste.md`
- Diagrams and pages: `references/diagrams-and-pages.md`
- Video: `references/video.md`

## Delivery and honesty

- Conclusion first, then the artifact. For a non-text primary artifact, say in one sentence why — e.g. "the key is the relationship between parameters, so I made it an adjustable page". For simple questions just answer; do not narrate routing.
- Only report what is done and evidenced. No test run, no "tested and passing". No video actually produced, no "video generated". A silent video must not be called narrated; a script must not be called a video.
- Downgrade gracefully when capability is missing: keep the key explanation, switch to a form you can verify (short clips, a captioned version, a runnable animation), and state what was actually delivered.
- Never invent data. Simulated data for teaching must be labeled.
- Never ask for plaintext API keys in the conversation.
- When the current combination explains things clearly, stop — no appended theory dump, and no "would you also like a page or video?" after every answer.

## Routing examples

| User request | Choice | Reason |
|---|---|---|
| "What is idempotency?" | Text | Short definition plus one repeated-request example |
| "How do the OAuth roles relate?" | Text + sequence diagram | The difficulty is message passing between roles |
| "Compare these three plans" | Text + comparison table | The user needs to look up exact differences; no animation needed |
| "How do rate and years affect compound interest?" | Text + HTML | Tuning parameters beats staring at fixed examples |
| "Why can the Fourier transform decompose a signal?" | Text + video | Dynamic superposition and rotating phasors connect formula to intuition |
| "List the history of this technology" | Text + timeline | Time-ordered, but not a reason to make a video |

## Common mistakes

- Defaulting to long prose — the biggest problem this skill exists to fix.
- Defaulting to the flashiest format — making a video for a simple question wastes the user's time.
- Formats that carry no information: a page with no interaction, a video that just reads text aloud, a diagram that is just boxed prose.
- Redundant combinations — each format must explain a different part.
