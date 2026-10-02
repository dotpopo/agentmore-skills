#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch screenshots via direct URLs + cookies (same origin as source parsing — never shoots the wrong page)
Usage: python3 screenshot_direct.py [workdir]
Config: url_shots.json in workdir, e.g. [{"url": "/common/xxx", "host": "site.example", "out": "screenshots/menu/page.png"}]
Requires: agent-browser CLI (replaceable with any Playwright implementation)
"""
import json, subprocess, time, os, sys

BASE = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else ".")
CONF = os.path.join(BASE, "url_shots.json")
PROG = os.path.join(BASE, "shot_progress.txt")

def ab(*args, timeout=50):
    try:
        r = subprocess.run(["agent-browser"] + list(args), capture_output=True, text=True, timeout=timeout)
        return (r.stdout or "").strip()
    except Exception:
        return ""

items = json.load(open(CONF))
ok = fail = 0
for it in items:
    full = it["url"] if it["url"].startswith("http") else "https://" + it["host"] + it["url"]
    ab("open", full)
    time.sleep(2.5)
    os.makedirs(os.path.dirname(it["out"]), exist_ok=True)
    r = ab("screenshot", it["out"])
    if "✓" in r or "saved" in r:
        ok += 1
    else:
        fail += 1
    open(PROG, "a").write(f"{ok+fail}/{len(items)} {it['out']}\n")
print(f"DONE ok={ok} fail={fail}")
