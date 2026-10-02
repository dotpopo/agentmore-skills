#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field parser for server-rendered admin pages (RuoYi / bootstrap-table style)
Usage: python3 parse_ruyi_html.py page.html [--json]
Output: page title, query fields, table columns (field:title config or <th>), button list
"""
import re, sys, json

def clean(x):
    return re.sub(r'<[^>]+>|\s+', '', x or '')

def parse(path):
    h = open(path, encoding='utf-8', errors='ignore').read()
    d = {}
    t = re.findall(r'<title>(.*?)</title>', h)
    d['title'] = t[0].strip() if t else ''
    labels = [clean(x).rstrip('：:').strip() for x in re.findall(r'<label[^>]*>(.*?)</label>', h, re.S)]
    d['labels'] = [l for l in labels if l][:40]
    # bootstrap-table / datatable style: field:'x', title:'y'
    cols = re.findall(r'field\s*:\s*[\x27"]([^\x27"]+)[\x27"]\s*,\s*title\s*:\s*[\x27"]([^\x27"]+)[\x27"]', h)
    d['cols'] = cols[:60]
    ths = [clean(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', h, re.S)]
    d['ths'] = [x for x in ths if x][:60]
    btns = [clean(a) or clean(b) for a, b in re.findall(r'<a[^>]*>(.*?)</a>|<button[^>]*>(.*?)</button>', h, re.S)]
    d['btns'] = [b for b in btns if b and len(b) < 30][:40]
    d['is_spa_shell'] = ('<div id="app"' in h or '<div id="root"' in h) and not d['labels'] and not d['cols'] and not d['ths']
    return d

if __name__ == '__main__':
    r = parse(sys.argv[1])
    if '--json' in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print('Title:', r['title'])
        print('Query fields:', ' | '.join(r['labels']))
        print('Table columns (config):', ' | '.join(c[1] for c in r['cols']))
        print('Table columns (<th>):', ' | '.join(r['ths']))
        print('Buttons:', ' | '.join(r['btns']))
        if r['is_spa_shell']:
            print('WARNING: this page is an SPA shell — use the browser-rendered channel to collect it!')
