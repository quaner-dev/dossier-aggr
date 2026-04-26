# Protocol Change Workflow

1. 先查 `.ai/protocols/` 的索引、映射和已知差异，定位协议、章节、接口或对象。
2. 再查本地 `.protocol/` 原始协议资料；若存在 DOCX 等可检索副本，优先用于文字检索和章节定位。
3. 涉及接口契约、字段语义、表格边界或疑似转换/OCR 误差时，回到 PDF/原始文件核验。
4. 不使用当前代码行为覆盖协议原意。
5. 修改协议模型时同步检查 `models/`、`api/`、`services/`、`repo/`、`tasks/`。
6. 更新协议相关测试，优先覆盖路径、包装对象、时间格式、枚举和错误语义。
7. 更新 `.ai/protocols/` 中的 `interface-index.md`、`model-index.md`、`implementation-map.md`、`known-gaps.md`。
8. 按 `.ai/workflows/pre-commit-checklist.md` 完成验证。
