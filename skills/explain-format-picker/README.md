# Explain Format Picker (v2)

Pick the right **output format** before explaining anything: STE-style text → diagram → interactive HTML page → explainer video — then draft, render, self-check, and deliver in 2–3 lines.

> Methodology distilled from Andrej Karpathy's note *"Stop making your LLM write long prose"*; v2 workflow mechanics (quantified decision gate, draft-first rendering, machine-checked drafts, reply protocol, per-sentence multilingual rules) absorbed from the open-source project [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html). Independent implementation.

## What's new in 2.0.0

| v1.0.0 | v2.0.0 |
|---|---|
| Route by "comprehension blocker" (qualitative) | **Quantified gate**: ≥3 interrelated concepts / any flow / ≥3-dimension comparison / hierarchy-or-evolution → page; plus optional always-on mode |
| Render directly | **Draft first**: content draft before rendering, panel budget 3–8 |
| "Check your work" prose | **Machine check**: `scripts/lint_draft.py` (zero-dependency) emits `L<line> [rule] … -> fix`; 2-round fix budget |
| One "language: match user" line | **Multilingual mechanism**: script-based detection, Simplified/Traditional character sets, per-sentence rule families (zh/en/ja vs neutral), RTL, `lang:` declaration rules |
| Video = heavy pipeline | **Two tiers**: video-as-page step player (default, no encoding) / full render pipeline (only when explicitly asked) |
| No feedback loop | **Reply protocol** (render first, 2–3 lines, no tool call after reply) + **ask panels** (reply-is-data security) |

## Structure

```
SKILL.md                         # decide → draft → build → self-check → reply protocol
references/ste.md                # exact limits + wordlists + exemptions
references/diagrams-and-pages.md # chart matrix, page assembly, ask panels, patching
references/video.md              # video-as-page (tier 0) + render pipeline (tier 1)
references/languages.md          # detection table, declaration rules, RTL
scripts/lint_draft.py            # zero-dependency draft linter (zh/en/ja rules)
zh/                              # 完整中文原版 (full original Chinese edition)
```

## Install

```bash
# SkillHub (search "explain-format-picker")
skillhub install explain-format-picker

# Manual: copy the folder into your agent's skills directory
```

## License

MIT.
