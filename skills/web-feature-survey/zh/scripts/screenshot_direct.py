#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie 直连 URL 批量截图（内容与源码解析同源，不会拍错页）
用法: python3 screenshot_direct.py
配置: 同目录 url_shots.json  [{"url": "/common/xxx", "out": "截图/一级菜单/页面.png"}]
依赖: agent-browser CLI（可替换为任意 playwright 实现）
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
