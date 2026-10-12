# Languages in Drafts

One decision per draft; everything downstream reads it and never re-decides.

## Decision order

1. **Declared** — a `lang:` line in the draft frontmatter (`lang: zh-Hant`, `lang: fa`, …). A declared tag is kept as written; `zh` is written out as `zh-CN`.
2. **Kept** — when updating an existing artifact, it keeps its language unless the new draft declares one.
3. **Detected** — from the text, by script:

| Script in the text | Language |
|---|---|
| Kana present | `ja` |
| Han characters, Simplified-only forms present | `zh-CN` |
| Han characters, Traditional-only forms present | `zh-Hant` |
| Han characters, only shared forms | stays `zh-CN` (declare if Traditional) |
| Hangul | `ko` |
| Cyrillic | `ru` (declare `uk` when Ukrainian) |
| Arabic | `ar` (declare `fa` when Persian) |
| Hebrew | `he` |
| Thai | `th` |
| Greek | `el` |
| Latin | `en` (declare when another Latin-script language) |

Han detection counts the characters that exist in only one form; a short or plain Chinese text may not contain any — it stays Simplified unless declared. Declare the language when the script alone cannot decide: Arabic script also writes Persian, Cyrillic also Ukrainian, Latin also French/German/Vietnamese.

## What the language decides

- **Sentence-length counting**: sentences with ≥4 Han characters count characters; others count words. Mixed text is measured per sentence, not per draft.
- **Rule family for the writing check**: `zh` and `en` get the full checks (length, passive/light verbs, word lists, clichés, typos); `ja` gets length checks only (Japanese `的` is a suffix, not a structural particle — the Chinese `的` rules do not transfer); **any other language gets only the language-neutral checks** (length, paragraph length). Do not pretend a word list you don't have.
- **Text direction**: Arabic and Hebrew are RTL — set `dir` on the page, mirror alignment, and test that diagrams still read correctly.
- **HTML metadata**: `<html lang>` follows the decided tag; page UI labels follow it too. A language without its own label set falls back to English labels — say so in the page footer only if the user needs to know.
- **Narration and video beats**: same language as the draft. Never auto-translate a draft into another language for delivery; translate only when the user asks.

## Typographic details worth enforcing

- Add a thin space between CJK and Latin/numbers ("使用 3 台服务器"), use full-width punctuation for Chinese/Japanese prose, half-width inside code and units.
- One terminology per draft per language: pick 数字/number, 配置/config once and keep it.
- When the user mixes languages, keep quoted terms in the source language and add the translation once at first mention.
