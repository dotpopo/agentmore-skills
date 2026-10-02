# STE-Style Writing Rules

ASD-STE100 (Simplified Technical English) is a controlled-language specification originally developed for aerospace maintenance documentation. It has two parts: writing rules (~9 sections) and a dictionary (~900 approved words, one part of speech and one meaning per word). Its value: strict constraints force clear writing that is very hard to misread.

## Default strictness

Default to "roughly 80% strictness": keep short sentences, one meaning per word, and active voice, but allow some sentence variety so the text doesn't read like a service manual.

- Safety-related content, procedures, and anything requiring zero ambiguity: close to 100%.
- General explanations: about 80%.
- The user may specify directly, e.g. "explain it at 80% STE".
- "80%" denotes a looseness level, not a measurable compliance score.

## Compliance claims

Only claim "conforms to ASD-STE100" when you can check the applicable version, the dictionary, and the full rule set. Otherwise always say "STE style". For Chinese and other non-English output, borrow the principles only; never claim formal compliance.

## Rules

| Rule | How |
|---|---|
| Conclusion first | State the core conclusion in one to three sentences, then expand |
| Short sentences | One sentence carries one main idea |
| Consistent terminology | One word per concept throughout; define on first use |
| Active voice | Make explicit who performs the action |
| One instruction | Procedural sentences usually contain a single instruction; split different actions |
| Clear reference | Avoid ambiguous "it", "this", "the above" |
| Separate content | Keep facts, assumptions, inferences, examples, and limits apart |
| Preserve precision | Never drop negated conditions, risks, units, or scope for the sake of simplification |
| Controlled paragraphs | One topic per paragraph; do not restate the conclusion repeatedly |
| Warnings first | Say what NOT to do first, then the reason |
| Vertical lists | Use lists; never pack five things into one long sentence |

The original spec's English reference limits: procedure sentences ≤ 20 words, descriptive sentences ≤ 25 words, paragraphs ≤ 6 sentences, noun clusters ≤ 3 words. Do not mechanically apply word counts to Chinese; for Chinese aim for ≤ 30 characters per sentence.

## Examples

Original:
> 在启动操作之前，操作员应确保液压油箱已经被充满。
> (Before starting the operation, the operator should make sure the hydraulic tank has been filled.)

STE style:
> 先确认液压油箱是满的。然后开始操作。
> (First confirm the hydraulic tank is full. Then start the operation.)

Original:
> 该系统利用多层缓存来显著降低数据库查询的平均延迟时间。
> (The system uses multi-layer caching to significantly reduce the average latency of database queries.)

STE style:
> 系统有多层缓存。缓存保存常用数据。查询先找缓存，找不到才查数据库。所以查询更快。
> (The system has multi-layer caching. The cache holds hot data. Queries hit the cache first and only reach the database on a miss. So queries are faster.)
