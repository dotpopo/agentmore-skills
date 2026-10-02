# Explain Format Picker

Pick the right **output format** before explaining anything: STE-style text → diagram → interactive HTML page → explainer video.

> Methodology distilled from Andrej Karpathy's note *"Stop making your LLM write long prose"* — as models get better at code, upgrading the output format (charts, pages, videos) is almost free, and our job moves up to supervision and understanding. This skill turns that idea into an executable routing procedure.

## What it does

Instead of defaulting to long prose, the agent:

1. **Identifies the comprehension blocker** — is the difficulty a relationship? a parameter to play with? a continuously unfolding process?
2. **Routes to a format** — short STE-style text, a diagram, an interactive HTML page, or an explainer video (3b1b-style).
3. **Runs the pre-upgrade checklist** — a higher tier must solve a concrete blocker, with cost proportional to benefit.
4. **Combines formats honestly** — each format carries a different part of the explanation; never one essay stuffed into three media.

## Structure

```
SKILL.md                        # routing procedure, checklists, examples
references/ste.md               # ASD-STE100-style writing rules (~80% strictness)
references/diagrams-and-pages.md# chart selection matrix + interactive page requirements
references/video.md             # explainer video pipeline (script → storyboard → render)
zh/                             # 完整中文原版 (original Chinese edition)
```

## Install

```bash
# SkillHub (search "explain-format-picker" after review completes)
skillhub install explain-format-picker

# Manual: copy the folder into your agent's skills directory
```

## License

MIT. The methodology idea is credit to Andrej Karpathy's public sharing; this skill is an independent, original implementation.
