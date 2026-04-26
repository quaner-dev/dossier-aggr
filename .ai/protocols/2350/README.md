# GA/T 2350.5 Notes

若本文与本地 `.protocol/` 原始协议冲突，以 `.protocol/` 为准。

协议基线：`GA-T 2350.5-2025.pdf`，封面信息为 `2025-10-13` 发布，`2026-02-01` 实施。

本地同时保留由 PDF 转换得到的 `GA-T 2350.5-2025.docx`。后续文字检索、章节定位和初步分析优先查看 DOCX；涉及接口契约、字段语义、表格边界或疑似转换/OCR 误差时，回到 PDF 原文核验。DOCX 是检索副本，不改变 PDF 作为协议基线的地位。

## 覆盖范围

当前仓库覆盖 A.5-A.18 中的主链路，A.6 `/VIAS/Tasks` 已纳入 `api -> services -> tasks -> repo -> models` 实现链路。

## 阅读入口

- `source-files.md`：原始协议文件位置。
- `interface-index.md`：附录 A 接口索引和当前状态。
- `implementation-map.md`：接口到代码层的映射。
- `model-index.md`：附录 B 对象到模型的映射。
- `testing-map.md`：相关测试入口。
- `known-gaps.md`：当前已确认差异。
