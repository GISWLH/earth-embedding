# rs-embed 研究自动化规则

## Goal
在 `research_outputs/` 下持续产出一套可复用研究资产：
- `rs_embed_model_inventory.{json,md}`
- 详细参数总表与研究报告
- 论文 PDF 下载库
- PDF -> Markdown -> 图片提取 -> 图床链接产物
- Google Satellite Embedding / Earth embedding 月尺度插值可行性分析

## Fixed evaluator
- 以“交付物覆盖度 + 流程可复现性 + 证据可追溯性”为核心标准。
- 不修改上游 rs-embed 核心库代码来伪造成功；允许增加 `research_outputs/` 下的脚本、文档、日志。
- 对运行状态的判断以真实命令输出、下载文件、转换结果、日志为准。

## Editable surface
- `research_outputs/**`
- `program.md`
- `results.tsv`

## Off-limits
- 不改 `src/rs_embed/**` 以绕过真实依赖或隐藏问题。
- 不伪造论文、PDF、图床链接、运行结果。

## Budget / cadence
- 按阶段推进：清单 -> 跑通 -> 批量下载 -> 转换上传 -> 方法调研。
- 每一阶段都要留下脚本、日志、文档。
- 定时向用户回报阶段进度，不等待额外指令。

## Standard commands
- 运行验证：参考 `research_outputs/runtime_runbook.md`
- 论文处理脚本：`research_outputs/scripts/download_and_process_papers.py`
- 研究汇总脚本：后续写入 `research_outputs/scripts/`

## Keep / discard rule
- 只有当脚本让流程更稳定、更可复现、覆盖更多模型/论文时才保留。
- 无法复现、引入额外脆弱性、或隐藏真实错误的改动一律丢弃。

## Output expectations
- 每个阶段都要更新 `results.tsv`
- 所有关键结论要能追溯到本地文件、论文、或官方页面
