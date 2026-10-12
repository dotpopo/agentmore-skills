# STE-Style Writing Rules (v2)

ASD-STE100 (Simplified Technical English) is a controlled-language specification originally developed for aerospace maintenance documentation: writing rules (~9 sections) plus a dictionary (~900 approved words, one part of speech and one meaning per word). Chinese rules are additionally inspired by the Simplified Technical Chinese word list. Strict constraints force clear writing that is very hard to misread.

v2 change: the rules below are **machine-checked** by `scripts/lint_draft.py` — run it on the draft instead of proofreading by eye. This file explains what the linter checks and why.

## Default strictness

Default to "roughly 80% strictness": keep short sentences, one meaning per word, and active voice, but allow some sentence variety so the text doesn't read like a service manual.

- Safety-related content, procedures, anything needing zero ambiguity: close to 100%.
- General explanations: about 80%.
- The user may specify directly ("explain it at 80% STE").
- "80%" denotes a looseness level, not a measurable compliance score. Only claim "conforms to ASD-STE100" when you can check the applicable version, dictionary, and full rule set; otherwise say "STE style".

## Exact limits (what the linter enforces)

| Rule | Limit | Applies to |
|---|---|---|
| Sentence length, Chinese | 35 chars (list items / steps) · 45 chars (descriptions) | sentences with ≥4 Han characters |
| Sentence length, English | 20 words (steps) · 25 words (descriptions) | other sentences |
| Paragraph length | ≤ 6 sentences | all languages |
| `的` chain | ≤ 3 consecutive | Chinese |
| Passive voice | avoid, say who does it | English |
| Light verbs | 进行X / 加以X / 予以X / 做出X → use X directly | Chinese |
| Clichés | 赋能、抓手、闭环、打通、全方位、多维度、深度融合、显著提升、至关重要、不可或缺、综上所述、总而言之、众所周知、毋庸置疑、一站式、底层逻辑、颗粒度、方法论、值得注意的是、与此同时 → replace with a concrete fact | Chinese |
| Typos | 登陆→登录、帐号→账号、阀值→阈值、布署→部署 | Chinese |
| Vague quantities | 尽快、若干、大概、大约、多次 → write the number (约 is allowed in descriptions) | Chinese |
| Ambiguous boundaries | number+以上/以下 → name the endpoint; number+以内 → 不超过 | Chinese |
| One meaning, one word | 单击/点按→点击、键入→输入、入参→参数、出参→返回值、缺省→默认 | Chinese |
| Padding words | utilize→use, in order to→to, prior to→before, in the event that→if, it is recommended that→(say who) | English |

Counter-examples shown on purpose are exempt: wrap them in `~~strikethrough~~` or put them in a table row whose status is `no`. Code, math, and headings are skipped automatically.

## Rules the linter can't check (self-enforce)

- Conclusion first: state the core conclusion in 1–3 sentences, then expand.
- One sentence, one main idea; one instruction per step.
- Terms stay consistent: same concept, same word; explain at first use.
- References stay explicit: no ambiguous 它/这个/"the above".
- Separate facts, assumptions, inferences, examples, and limits — don't blend them in one sentence.
- Keep precision when simplifying: don't drop negations, risks, units, or applicability.
- Warnings first: say what NOT to do, then why.
- Complex content goes vertical (lists), never into one long sentence.

## Examples

Original:
> 在启动操作之前，操作员应确保液压油箱已经被充满。

STE style:
> 先确认液压油箱是满的。然后开始操作。

Original (linter findings: 赋能 cliché, 进行优化 light verb, 至关重要 cliché):
> 新引擎赋能数据处理管道，对查询模块进行优化，这一步至关重要。

STE style:
> 新引擎加速数据处理。查询模块做了三处优化：索引、缓存、批量写入。步骤 3 依赖这一步。
