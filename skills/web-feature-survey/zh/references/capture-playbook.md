# 双通道采集与抽查补盲操作手册

## 通道 A：服务端渲染直抓（快而全的底稿）

```bash
# 1. 从浏览器导出 Cookie（agent-browser 为例）
agent-browser cookies > cookies.txt
# 整理成 "k1=v1; k2=v2" 形式写入 cookie_header.txt

# 2. 逐页直抓
curl -s -H "Cookie: $(cat cookie_header.txt)" \
     -H "User-Agent: Mozilla/5.0" \
     "https://站点域名/common/xxx" -o page.html

# 3. 判据：page.html 内含 <label>、field: 'x', title: 'y'、<table> 等真实内容
#    → 服务端渲染，可批量抓；若只是 <div id="app"></div> 空壳 → 该页是 SPA，走通道 B
```

解析要点（Python 正则即可，参考 scripts/parse_ruyi_html.py）：
- `<label>(.*?)</label>` → 查询/筛选字段
- `field\s*:\s*['"]x['"]\s*,\s*title\s*:\s*['"]y['"]` → bootstrap-table 风格表格列
- `<th>` → 服务端渲染表格列
- `<a>/<button>` → 按钮（按 class 含 btn / 操作列特征过滤）

## 通道 B：浏览器渲染抽查（补盲，必做）

**源码解析的四类盲区（实证）**：
1. JS 渲染的表格列 —— 如 Vue 组件 columns 里动态生成，HTML 源码完全不含
   （实例：车牌类型管理漏了"是否允许续费""是否统计余位"两列）
2. 行级操作按钮 —— 只渲染在每行数据里（实例：临停收费标准漏了"模拟计费"）
3. 弹窗（新增/编辑）内字段 —— JS 动态创建，无静态结构
4. 交互行为与提示语 —— toast/confirm 文案、按钮点击后的行为，无结构承载

抽查流程（每个一级菜单至少 2~3 页）：
```js
// 浏览器渲染后执行
(function(){
  var ths=[...document.querySelectorAll('th')].map(e=>e.textContent.trim());
  var rowBtns=[...document.querySelectorAll('table a, table button, .el-table a')]
    .map(e=>e.textContent.trim()).filter(Boolean);
  return JSON.stringify({ths, rowBtns});
})()
```
- 与通道 A 结果做差集 → 差集项回填文档，并标注来源"渲染抽查补录 ➕"。
- 弹窗字段：点开"新增"（只看字段，**填完立即取消，绝不保存**）。

## 截图策略

- **优先直连 URL 截图**（与字段解析同源，绝不会拍错页面）：
  `open URL → wait 2.5s → screenshot`，逐页循环。
- 不要用"点击菜单导航"的方式截图：SPA 多面板 + iframe 下极易拍到旧页面/错误面板。
- 交付前用脚本核对文档里每个截图路径是否真实存在。

## 进度与可靠性

- 每完成一个一级菜单就落盘一次文档（追加式）。
- 批量任务后台化：双 fork 脱离会话 + 进度文件，主流程轮询进度，防环境抖动重试吃掉轮次。
- 结果文件里记录每页来源：nav_ok / srcs / 抽查状态，便于复查与续作。
