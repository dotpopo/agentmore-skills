---
name: web-feature-survey-agentmore
description: >
  After logging into a web admin system or SaaS backend, produce a
  field-level, site-wide feature inventory / competitive-benchmark document
  with screenshots, using a dual-channel approach: server-rendered HTML
  parsing (fast, complete draft) + browser-rendered spot checks (mandatory,
  closes blind spots). Ships battle-tested recipes for slider-captcha
  solving, menu enumeration, DOM-visibility pitfalls, and a source-parsing
  blind-spot checklist (JS-rendered columns, row-level buttons, dialog
  fields, interactive toast/confirm copy).
version: 1.0.0
license: MIT
---

# Web Feature Survey (Benchmark Inventory Generation)

Perform a **field-level feature survey** of a web admin / SaaS system (parking SaaS, ERP, CRM, ...), producing a structured feature inventory document (menu tree → pages → query fields / table columns / buttons / notes) + per-page screenshots + a coverage report.

Use cases: competitive benchmarking, requirements research, pre-migration feature audits.

## Core Workflow (Four Phases)

### Phase 0: Preparation and safety boundary

1. Set the safety boundary and write it at the top of the document: **read-only throughout**. Never click delete / save / submit / approve / enable-disable / reset-password; for "create" dialogs, open only to record fields, then close; skip anything uncertain and mark it "unverified".
2. After each top-level menu is done, **append-save the document incrementally** (don't wait for everything) so an interrupted run can resume.
3. Maintain a task list (TodoWrite / progress table) with one status node per top-level menu.

### Phase 1: Login (including captcha)

See [references/captcha-solver.md](references/captcha-solver.md). Key points:

- Screenshot first to identify the captcha type; for AJ-Captcha-style slider puzzles, prefer **image analysis + fitting** over eyeballing or blind dragging.
- After login, export cookies immediately (`agent-browser cookies` or equivalent) for reuse in fetching.
- Forced pop-ups may appear after login (e.g. "password too simple"): click cancel only; change nothing.

### Phase 2: Menu enumeration (three tricks, cheapest first)

Try in order; stop at first hit:

1. **Check whether the homepage/frame HTML server-renders the menu** (RuoYi, JeeSite and other Chinese frameworks often do): `curl -H "Cookie: ..."` the homepage and look for menu items shaped like `li[...] href="/xxx"` —
   you get the full "menu → URL" mapping in one shot. **This is the highest-yield path** (84 pages enumerated in 1 minute on a real project).
2. Menu data in a JS variable / localStorage: grep page source and storage for menu/route/routes.
3. Neither works: click each top-level menu and extract sub-panels from the DOM (mind the visibility pitfalls below).

### Phase 3: Page field collection (dual channel — use BOTH)

**Channel A: server-rendered HTML parsing (primary — fast and complete)**
- With cookies + page URL, `curl` the HTML directly and parse:
  - `<label>` → query/filter fields
  - `field: 'x', title: 'y'` (bootstrap-table-style config) → table columns
  - `<a>/<button>` → action buttons
  - `<title>` → page title
- Criterion: if the fetched HTML contains real content like `<label>` / `field:`, the page is server-rendered — safe to batch-fetch.

**Channel B: browser-rendered spot checks (mandatory — closes blind spots)**
- **Source parsing alone WILL miss things** (a spot check of 84 pages empirically missed 2):
  - JS-rendered table columns (e.g. a `columns` array generated dynamically in a Vue component: "renewal allowed", "count remaining slots")
  - Row-level action buttons (e.g. "simulate billing" on each table row)
- Sample at least 2–3 pages per top-level menu: open in browser, then run
  `document.querySelectorAll('table th, .el-table__header th, .ivu-table th')` plus
  row-button containers, diff against Channel A results, and backfill the diff into the document.
- Fields inside dialogs (create/edit), interactive behaviors, and toast/confirm copy have no structural carrier in source — verify page-by-page in the browser; if you can't cover everything, honestly list it under "uncovered" in the document.

### Phase 4: Screenshots and documentation

- Do NOT navigate page-by-page via clicks for screenshots (SPA multi-panel/iframe setups easily shoot the wrong page).
  If page URLs are directly reachable: browser `open URL → screenshot` per page — same origin as the parsed fields, therefore trustworthy.
- Document structure: menu-tree overview → chapters per top-level menu (page → feature points) → benchmarking hints → coverage report.
- **Verify before delivery**: check every screenshot path referenced in the document with `os.path.exists`, one by one. Wrong paths are a high-frequency failure (first version of the real project had them).
- Declare format deviations: e.g. if you turned tables into structured lists (information-equivalent, tidier), note "format adaptation" in the document so readers don't mistake it for raw survey data.

## Verified Pitfall Checklist (must read)

1. **SPA multi-panel visibility**: when several menu panels coexist in the DOM, `getComputedStyle` still returns `block` for children of a `display:none` ancestor —
   visibility must be judged via `offsetParent !== null` or `getBoundingClientRect().width > 0`.
   Blind clicks land on the wrong panel, manifesting as "click does nothing / screenshot shows the old page".
2. **iframe architecture**: page bodies often live in iframes (e.g. RuoYi tabs). When the top document shows nothing, read via `iframe.contentDocument` (same-origin); each newly opened page may **append a new iframe** rather than reuse — probe for the last one.
3. **Click-navigation confirmation**: after clicking a menu, poll for iframe src change (or URL change) to confirm navigation; retry on timeout. Never click-and-collect: slow SPA loads will collect the previous page.
4. **Handle-based drag coordinate offset**: slider handles usually "center-follow the mouse" — element left = mouse x − half width. Don't forget the half width when computing the drop point.
5. **Modal overlay blocks clicks**: layui-layer overlays block clicks (agent-browser reports "covered") — click cancel/close first, or `display:none` the overlay before operating.
6. **Session expiry**: captcha images and login cookies expire; script the whole "re-login + solve captcha" flow (image analysis + trajectory drag) so it can be re-run anytime.
7. **Source-parsing blind spots** (repeated on purpose): JS-dynamic columns, row-level buttons, dialog fields, interactive copy —
   all four must be spot-checked/verified in the browser; treat source parsing as a "fast, complete draft" only.
8. **Long-task execution environment**: when network/session flakiness is high, run batch fetches as background scripts (double-fork out of the session + progress-file polling) so tool-call rounds aren't eaten by retries.

## Deliverable Spec

- `<name>-feature-inventory.md`: menu-tree overview → chapters (page → action path/URL/title/query fields/table columns/buttons/notes) → benchmarking hints (observations only, no conclusions) → coverage report (including uncovered items and why).
- Screenshot directory: `screenshots/<top-level menu>/<page>.png`, exactly matching paths referenced in the document.
- Tag every data point with provenance: browser-verified ✅ / source-parsed 📄 / spot-check backfill ➕.

## Reference Files

- [references/captcha-solver.md](references/captcha-solver.md) — slider/jigsaw captcha auto-solve recipe
- [references/capture-playbook.md](references/capture-playbook.md) — dual-channel capture and spot-check playbook
- [scripts/parse_ruyi_html.py](scripts/parse_ruyi_html.py) — server-rendered HTML field parser (labels / field:title config / buttons)
- [scripts/screenshot_direct.py](scripts/screenshot_direct.py) — cookie-based direct-URL batch screenshots
