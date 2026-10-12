#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_draft.py — self-check a content draft before turning it into text / diagram / page / video.

Zero dependencies. Rules inspired by ASD-STE100 (Simplified Technical English) and the
Simplified Technical Chinese word list (https://github.com/mzopedia/simplified-technical-chinese).
This is an independent implementation for the explain-format-picker skill.

Usage:
    python3 lint_draft.py draft.md [--lang zh|en|ja|auto]

Output: one finding per line, machine-parseable:
    L<line> [<rule>] <message> -> <suggestion>
Exit code: 0 = clean, 1 = findings (style warnings), 2 = usage error.

Skipped text: fenced code blocks, inline code, math ($$ / $...$), ~~strikethrough~~
(counter-examples on purpose), table rows marked no/✗, headings, html tags, image syntax.
"""
import re
import sys

# ---------- limits ----------
# zh: characters per sentence (procedural / descriptive); en: words per sentence.
LIMITS = {
    "zh": {"procedural": 35, "descriptive": 45},
    "en": {"procedural": 20, "descriptive": 25},
    "neutral": {"procedural": 40, "descriptive": 50},  # words, unknown language
}
MAX_SENT_PER_PARA = 6

# ---------- zh word lists (independent curation, public-spec inspired) ----------
ZH_LIGHT_VERBS = [
    (re.compile(r"进行(?!中|时)了?([一-龥]{2})"), "use the verb directly"),
    (re.compile(r"(?:加以|予以)([一-龥]{2})"), "use the verb directly"),
    (re.compile(r"[做作]出了?([一-龥]{2})"), "use the verb directly"),
]
ZH_CLICHES = [
    "赋能", "抓手", "闭环", "打通", "全方位", "多维度", "深度融合", "显著提升",
    "至关重要", "不可或缺", "综上所述", "总而言之", "众所周知", "毋庸置疑",
    "一站式", "底层逻辑", "颗粒度", "方法论", "值得注意的是", "与此同时",
]
ZH_TYPOS = {
    "登陆": "登录", "帐号": "账号", "阀值": "阈值", "布署": "部署",
}
ZH_VAGUE = {
    "尽快": "write the concrete deadline", "若干": "write the number",
    "大概": "use 约 in descriptions, a value in steps",
    "大约": "use 约 in descriptions, a value in steps",
    "多次": "write the count",
}
ZH_UNIFY = {
    "单击": "点击", "点按": "点击", "键入": "输入", "登出": "退出登录",
    "入参": "参数", "出参": "返回值", "缺省": "默认",
}
RE_NUM_BELOW = re.compile(r"\d\s*(?:以上|以下)")
RE_NUM_WITHIN = re.compile(r"\d[^。，；\n]{0,6}以内")

EN_PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(\w+ed|done|given|taken|shown|made|known|sent|kept|held|built|set|run|found)\b", re.I)
EN_WORDS = {
    r"\butilize[sd]?\b": "use",
    r"\bin order to\b": "to",
    r"\bprior to\b": "before",
    r"\bsubsequent to\b": "after",
    r"\bin the event that\b": "if",
    r"\bwith the exception of\b": "except",
    r"\bit is recommended that\b": "say who recommends",
    r"\bmake a decision\b": "decide",
}

CJK = re.compile(r"[\u4e00-\u9fff]")
KANA = re.compile(r"[\u3040-\u30ff]")
ZH_SENT_SPLIT = re.compile(r"[。！？；!?;]")
EN_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\u4e00-\u9fff\"'(])")
ABBR = re.compile(r"\b(?:e\.g|i\.e|etc|vs|cf|approx|Fig|Dr|Mr|Mrs|Ms|St|No)\.$", re.I)
INLINE_CODE = re.compile(r"`[^`]*`")
STRIKE = re.compile(r"~~.*?~~", re.S)
MATH_INLINE = re.compile(r"\$[^$\n]+\$")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
EMPH = re.compile(r"\*\*?([^*]+)\*\*?")
FRONT_LANG = re.compile(r"^lang:\s*(\S+)\s*$", re.M)


def strip_spans(text):
    """Remove text that must NOT be checked; keep line structure."""
    text = INLINE_CODE.sub("\u0000", text)      # placeholder keeps length, no words
    text = MATH_INLINE.sub("", text)
    text = STRIKE.sub("", text)
    text = IMAGE.sub("", text)
    text = LINK.sub(r"\1", text)
    text = HTML_TAG.sub("", text)
    text = EMPH.sub(r"\1", text)
    return text


def detect_lang(text):
    declared = FRONT_LANG.search(text)
    if declared and declared.group(1) not in ("auto", "und"):
        return declared.group(1).lower()
    cjk = len(CJK.findall(text))
    latin = len(re.findall(r"[A-Za-z]+", text))
    if KANA.search(text):
        return "ja"
    if cjk >= max(4, latin // 3):
        return "zh"
    return "en"


def sentence_lang(sentence):
    """Per-sentence script check: >=4 Han chars -> zh counting, else en/word counting."""
    return "zh" if len(CJK.findall(sentence)) >= 4 else "en"


def split_sentences(text, lang):
    if lang == "zh":
        return [p.strip() for p in ZH_SENT_SPLIT.split(text) if p.strip()]
    parts = EN_SENT_SPLIT.split(text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        out.append(p)
    return out


def check_sentence_lengths(text, lang, line_no, is_list, out):
    sents = split_sentences(text, lang)
    for s in sents:
        sl = sentence_lang(s) if lang in ("zh", "en", "ja") else "neutral"
        kind = "procedural" if is_list else "descriptive"
        if sl == "zh":
            n = len(CJK.findall(s))
            cap = LIMITS["zh"][kind]
            if n > cap:
                out.append((line_no, "sentence-length",
                            f"{n} Chinese characters (max {cap} for {kind})",
                            "split into two sentences"))
        elif sl == "en":
            n = len(re.findall(r"[A-Za-z0-9']+", s))
            cap = LIMITS["en" if lang != "ja" else "neutral"][kind]
            if n > cap:
                out.append((line_no, "sentence-length",
                            f"{n} words (max {cap} for {kind})",
                            "split into two sentences"))


def check_zh(text, line, out):
    for rx, msg in ZH_LIGHT_VERBS:
        for m in rx.finditer(text):
            out.append((line, "light-verb", f"{m.group(0)}", msg))
    for w in ZH_CLICHES:
        if w in text:
            out.append((line, "cliche", f"'{w}'", "replace with a concrete fact"))
    for bad, good in ZH_TYPOS.items():
        if bad in text:
            out.append((line, "non-approved-word", f"'{bad}'", f"use '{good}'"))
    for bad, fix in ZH_VAGUE.items():
        if bad in text:
            out.append((line, "vague-quantity", f"'{bad}'", fix))
    for bad, good in ZH_UNIFY.items():
        if bad in text:
            out.append((line, "one-meaning-one-word", f"'{bad}'", f"use '{good}'"))
    for m in RE_NUM_BELOW.finditer(text):
        out.append((line, "ambiguous-boundary", "number + 以上/以下",
                    "name the endpoint: 大于/不小于/小于/不大于"))
    for m in RE_NUM_WITHIN.finditer(text):
        out.append((line, "ambiguous-boundary", "number + 以内", "use 不超过"))
    for m in re.finditer(r"(?:\s*的){4,}", text):
        out.append((line, "de-chain", "more than 3 的 in a row",
                    "split the sentence or drop particles"))


def check_en(text, line, out):
    for m in EN_PASSIVE.finditer(text):
        out.append((line, "passive-voice", f"'{m.group(0)}'", "say who does it"))
    for rx, fix in EN_WORDS.items():
        m = re.search(rx, text, re.I)
        if m:
            out.append((line, "non-approved-word", f"'{m.group(0)}'", f"use '{fix}'"))


def lint(text):
    lang = detect_lang(text)
    out = []
    lines = text.split("\n")
    in_code = in_math = False
    para_buf, para_no = [], 0

    def flush_para():
        nonlocal para_buf, para_no
        if para_buf:
            joined = " ".join(para_buf)
            plang = "zh" if sentence_lang(joined) == "zh" else "en"
            n_sents = len(split_sentences(joined, plang))
            if n_sents > 6:
                out.append((para_no, "paragraph-length",
                            f"{n_sents} sentences (max 6)", "split the paragraph"))
            para_buf, para_no = [], 0

    for i, raw in enumerate(lines, 1):
        t = raw.strip()
        if t.startswith("```") or t.startswith("~~~"):
            in_code = not in_code
            flush_para()
            continue
        if in_code:
            continue
        if t.startswith("$$"):
            in_math = not in_math
            continue
        if in_math or not t or re.match(r"^#{1,6}\s", t) or re.match(r"^(-{3,}|[*_]{3,})$", t) \
           or t.startswith(">") or t.startswith("lang:"):
            continue
        if t.startswith("|"):
            flush_para()
            if re.match(r"^\|?[\s:|-]+\|?$", t):
                continue
            cells = [c.strip() for c in t.strip("|").split("|")]
            if any(re.match(r"^(no|✗|✘)(\s|$)", c) for c in cells):
                continue
            for c in cells:
                c = re.sub(r"^(ok|warn|✓|✔|⚠)(\s|$)", "", c)
                body = strip_spans(c)
                check_sentence_lengths(body, lang, i, True, out)
                if sentence_lang(body) == "zh":
                    check_zh(body, i, out)
                else:
                    check_en(body, i, out)
            continue
        m = re.match(r"^(?:[-*+]|\d+[.)])\s+(.*)$", t)
        if m:
            flush_para()
            body = strip_spans(m.group(1))
            check_sentence_lengths(body, lang, i, True, out)
            if sentence_lang(body) == "zh":
                check_zh(body, i, out)
            else:
                check_en(body, i, out)
            continue
        body = strip_spans(t)
        if not para_buf:
            para_no = i
        para_buf.append(body)
        if sentence_lang(body) == "zh":
            check_zh(body, i, out)
        else:
            check_en(body, i, out)
        joined = " ".join(para_buf)
        plang = "zh" if sentence_lang(joined) == "zh" else "en"
        if len(split_sentences(joined, plang)) > 6:
            out.append((para_no, "paragraph-length",
                        f"more than 6 sentences", "split the paragraph"))
            para_buf, para_no = [], 0
    flush_para()
    return lang, out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    text = open(path, encoding="utf-8", errors="ignore").read() if path != "-" else sys.stdin.read()
    lang, findings = lint(text)
    for line, rule, msg, fix in findings:
        print(f"L{line} [{rule}] {msg} -> {fix}")
    print(f"# lang={lang}, findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
