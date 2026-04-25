# Protocol Change Workflow

1. 先查本地 `.protocol/` 原始协议文件。
2. 再查 `.ai/protocols/` 的索引、映射和已知差异。
3. 不使用当前代码行为覆盖协议原意。
4. 修改协议模型时同步检查 `models/`、`api/`、`services/`、`repo/`、`tasks/`。
5. 更新协议相关测试，优先覆盖路径、包装对象、时间格式、枚举和错误语义。
6. 更新 `.ai/protocols/` 中的 `interface-index.md`、`model-index.md`、`implementation-map.md`、`known-gaps.md`。
7. 至少尝试运行 `pytest -q`。
