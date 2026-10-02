# Web Feature Survey

Field-level feature inventory / competitive-benchmark documents for web admin systems and SaaS backends — with screenshots and provenance tags.

> Born from a real benchmarking project against a parking-management SaaS: 84 pages enumerated in ~1 minute via server-rendered menu HTML, and a spot check that empirically proved source parsing misses JS-rendered columns and row-level buttons — which became the skill's core dual-channel rule.

## What it does

1. **Logs in** (including slider-captcha auto-solve via image fitting, not eyeballing).
2. **Enumerates the menu tree** — three tricks, cheapest first (server-rendered menu HTML → JS variables/localStorage → click-through).
3. **Captures fields via dual channels**:
   - Channel A: `curl` + parse server-rendered HTML (labels, `field:'x', title:'y'` columns, buttons) — fast and complete draft.
   - Channel B: browser-rendered spot checks — **mandatory**, because source parsing provably misses JS-rendered columns, row-level buttons, dialog fields, and toast/confirm copy.
4. **Screenshots via direct URLs** (never click-navigation), then verifies every referenced path before delivery.
5. **Delivers** a structured inventory: menu tree → pages → fields/columns/buttons/notes → benchmarking hints → coverage report, with provenance tags (browser-verified ✅ / source-parsed 📄 / spot-check backfill ➕).

## Safety

Read-only throughout: never click delete/save/submit/approve/reset; "create" dialogs are opened to record fields only, then cancelled.

## Structure

```
SKILL.md                            # four-phase workflow + verified pitfall checklist
references/captcha-solver.md        # AJ-Captcha slider auto-solve (image fitting, ~100% success)
references/capture-playbook.md      # dual-channel capture + spot-check playbook
scripts/parse_ruyi_html.py          # server-rendered HTML field parser
scripts/screenshot_direct.py        # cookie-based direct-URL batch screenshots
zh/                                 # 完整中文原版 (original Chinese edition)
```

## License

MIT.
