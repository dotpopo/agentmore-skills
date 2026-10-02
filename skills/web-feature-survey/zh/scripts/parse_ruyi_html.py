#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务端渲染后台页面（RuoYi/bootstrap-table 风格）字段解析
用法: python3 parse_ruyi_html.py page.html [--json]
输出: 页面标题、查询字段、表格列(field:title 配置或 <th>)、按钮清单
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
    # bootstrap-table /datatable 风格: field:'x', title:'y'
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
        print('标题:', r['title'])
        print('查询字段:', '、'.join(r['labels']))
        print('表格列(配置):', '、'.join(c[1] for c in r['cols']))
        print('表格列(<th>):', '、'.join(r['ths']))
        print('按钮:', '、'.join(r['btns']))
        if r['is_spa_shell']:
            print('⚠️ 该页是 SPA 空壳，需走浏览器渲染通道采集！')
