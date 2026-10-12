# AgentMore Skills

A collection of battle-tested agent skills — each one distilled from a real project into a reusable procedure. English editions live here; complete Chinese originals ship in each skill's `zh/` folder.

| Skill | One-liner | Origin |
|---|---|---|
| [explain-format-picker](skills/explain-format-picker/) | Pick the output format (STE text → diagram → interactive page → explainer video) before explaining anything; draft-first workflow with a machine-checked draft linter | Methodology distilled from Andrej Karpathy's note on upgrading LLM output formats; v2 mechanics absorbed from [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html); original implementation |
| [web-feature-survey](skills/web-feature-survey/) | Field-level feature inventory + benchmark docs for web admin systems, via dual-channel capture (HTML parsing + browser spot checks) | Distilled from a real parking-SaaS benchmarking project (84 pages) |

Also published on [SkillHub](https://skillhub.cn) (search the skill names).

## Usage

Copy a skill folder into your agent's skills directory, or install from SkillHub:

```bash
skillhub install explain-format-picker
skillhub install web-feature-survey
```

## Design principles

- **Procedures, not vibes**: every skill encodes verified pitfalls and decision rules, not generic advice.
- **Honesty rules built in**: never claim tested what wasn't tested, never present scripts as videos, never invent data.
- **Bilingual**: English first for reach; `zh/` keeps the complete original Chinese edition.

## License

MIT
