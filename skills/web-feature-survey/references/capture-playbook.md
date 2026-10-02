# Dual-Channel Capture and Spot-Check Playbook

## Channel A: server-rendered direct fetch (fast, complete draft)

```bash
# 1. Export cookies from the browser (agent-browser example)
agent-browser cookies > cookies.txt
# Reformat into "k1=v1; k2=v2" and save to cookie_header.txt

# 2. Fetch pages directly, one by one
curl -s -H "Cookie: $(cat cookie_header.txt)" \
     -H "User-Agent: Mozilla/5.0" \
     "https://<site-domain>/common/xxx" -o page.html

# 3. Criterion: page.html contains real content such as <label>,
#    field: 'x', title: 'y', <table> → server-rendered, batch-fetch allowed.
#    If it's just an empty <div id="app"></div> shell → SPA page, use Channel B.
```

Parsing notes (plain Python regex; see scripts/parse_ruyi_html.py):
- `<label>(.*?)</label>` → query/filter fields
- `field\s*:\s*['"]x['"]\s*,\s*title\s*:\s*['"]y['"]` → bootstrap-table-style columns
- `<th>` → server-rendered table columns
- `<a>/<button>` → buttons (filter by class containing btn / action-column traits)

## Channel B: browser-rendered spot checks (closes blind spots — mandatory)

**The four empirically proven blind spots of source parsing:**
1. JS-rendered table columns — generated dynamically in e.g. a Vue `columns` array, entirely absent from HTML source
   (real case: plate-type management missed the "renewal allowed" and "count remaining slots" columns)
2. Row-level action buttons — rendered only inside each data row (real case: drop-in parking rates missed "simulate billing")
3. Dialog (create/edit) fields — created dynamically by JS, no static structure
4. Interactive behaviors and copy — toast/confirm text and post-click behavior have no structural carrier

Spot-check procedure (at least 2–3 pages per top-level menu):
```js
// run after browser rendering
(function(){
  var ths=[...document.querySelectorAll('th')].map(e=>e.textContent.trim());
  var rowBtns=[...document.querySelectorAll('table a, table button, .el-table a')]
    .map(e=>e.textContent.trim()).filter(Boolean);
  return JSON.stringify({ths, rowBtns});
})()
```
- Diff against Channel A results → backfill diff items into the document, tagged "spot-check backfill ➕".
- Dialog fields: open "Create" (record fields only, **cancel immediately — NEVER save**).

## Screenshot strategy

- **Prefer direct-URL screenshots** (same origin as field parsing; never shoots the wrong page):
  `open URL → wait 2.5s → screenshot`, looped per page.
- Do not screenshot by click-navigation: with SPA multi-panel + iframes you will easily capture an old page / wrong panel.
- Before delivery, script-verify that every screenshot path referenced in the document actually exists.

## Progress and reliability

- Append-save the document after every completed top-level menu (incremental persistence).
- Push batch jobs to background: double-fork out of the session + progress file; the main flow polls progress — protects tool rounds from flaky-environment retries.
- Record per-page provenance in the results file: nav_ok / srcs / spot-check status, for review and resumption.
