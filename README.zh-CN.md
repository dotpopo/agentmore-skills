# AgentMore Skills

一套从真实项目里提炼出来的 Agent 技能合集。每个技能都是"实战经验 → 可复用流程"的沉淀；本仓库以英文版为主（利于传播与检索），每个技能的 `zh/` 目录保留完整中文原版。

| 技能 | 一句话 | 来源 |
|---|---|---|
| [explain-format-picker](skills/explain-format-picker/) | 解释任何内容前，先选对输出形式（STE 风格文字 → 图表 → 交互网页 → 解释视频） | 方法论源自 Andrej Karpathy 关于 LLM 输出格式升级的公开分享，本技能为独立原创实现 |
| [web-feature-survey](skills/web-feature-survey/) | 对 Web 后台系统做字段级功能调研与对标清单，双通道采集（源码解析 + 浏览器抽查） | 从真实停车 SaaS 对标项目（84 页）提炼 |

同时发布于 [SkillHub](https://skillhub.cn)（搜索技能名）。

## 用法

把技能文件夹拷贝进你的 Agent 技能目录，或从 SkillHub 安装：

```bash
skillhub install explain-format-picker
skillhub install web-feature-survey
```

## 设计原则

- **流程而非口号**：每个技能沉淀的是已验证的陷阱清单与决策规则，不是泛泛建议。
- **内置诚实条款**：没测过不说测过，脚本不说成视频，不编数据。
- **双语**：英文优先利于触达；`zh/` 保留完整中文原版。

## 许可

MIT
