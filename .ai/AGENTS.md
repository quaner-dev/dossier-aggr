# AGENTS

本文件定义本仓库内 AI/代码代理的执行约束。目标是：快速、可验证、低回归地完成改动。

## 1. 文件定位与目标

- 用途：约束代理在本仓库中的改动行为、验证流程与文档同步规则。
- 原则：分层清晰、协议一致、可追踪验证、最小改动面。
- 根目录 `AGENTS.md` 只作为薄入口，完整规则以本文件为准。

## 2. 仓库事实基线

- 技术栈：`FastAPI` + `SQLModel` + `Taskiq` + `Alembic`
- 入口：`main.py`
- 关键目录：
  - `api/`：路由与协议编排层
  - `services/`：业务逻辑层
  - `repo/`：数据访问层
  - `tasks/`：任务与数据访问处理
  - `models/`：协议模型与数据模型
  - `tests/`：测试用例
  - `alembic/`：数据库迁移
  - `.ai/`：AI 协作上下文、协议导航、测试说明和历史计划摘要
  - `.protocol/`：本地原始协议资料，已被 `.gitignore` 忽略，不纳入仓库跟踪

## 3. 协议与文档优先级

当需求、代码实现与文档存在冲突时，优先级如下：

1. 本地 `.protocol/` 原始协议文件。
2. `.ai/AGENTS.md` 与根 `AGENTS.md`。
3. `.ai/project`、`.ai/protocols`、`.ai/testing`、`.ai/workflows` 中的整理文档。
4. 当前代码实现现状。

代理在解释协议时，不得仅依据当前代码行为覆盖协议原意。

## 4. 标准开发命令

- 安装依赖：`pip install -r requirements.txt`
- 启动 API：`uvicorn main:app --host 0.0.0.0 --port 8000`
- 启动 worker：`taskiq worker core.brokers:broker`
- 代码质量检查：`ruff check .`
- 代码质量自动修复：`ruff check . --fix`
- 类型检查：`pyright`
- 运行测试：`pytest -q`
- 生成迁移：`alembic revision --autogenerate -m "<message>"`
- 执行迁移：`alembic upgrade head`

## 5. 编码与改动约束

- 保持分层边界：不把业务逻辑直接塞进 `api/`。
- 新增接口时遵循：
  - 在 `api/` 定义路由函数与请求/响应编排。
  - 在 `services/` 实现业务逻辑。
  - 涉及异步写入时在 `tasks/` 增加任务处理。
  - 数据访问放在 `repo/`。
- 模型变更优先复用 `models/` 现有对象与校验方式，优先使用 `model_validate`。
- 变更尽量小步提交，避免无关重构。
- 不修改与任务无关的文件。

## 6. 测试与验证约束

- 每次修改后按 `.ai/workflows/pre-commit-checklist.md` 至少尝试完成质量检查、类型检查和测试。
- 改动涉及 API 行为时，优先补充或更新 `tests/` 下对应测试。
- 改动涉及数据库 schema 时，必须同时提供 Alembic 迁移，并验证 `alembic upgrade head` 可执行。
- 若环境缺少质量检查、类型检查或测试依赖，必须在输出中说明具体失败原因。

## 7. 文档同步约束

当接口契约、架构分层或测试流程发生变化时，同步更新：

- `.ai/project/`
- `.ai/protocols/`
- `.ai/testing/`
- `.ai/workflows/`（涉及流程变化时）

历史计划摘要在 `.ai/plans/archive/`，只在需要追溯决策时查看或更新。

## 8. 上下文读取约束

- 默认只读取 `.ai/AGENTS.md` 和当前任务相关入口，不全量读取 `.ai/`。
- 协议任务先从 `.ai/protocols/README.md` 进入，再按协议和接口选择具体索引文件。
- 测试、流程、编码规范分别从对应目录 README 进入。
- `.ai/plans/` 不属于默认上下文；只有追溯历史决策、设计来源或迁移背景时才读取。
- 常规 `.ai` 检索可使用：`rg "<keyword>" .ai --glob '!.ai/plans/archive/**'`

## 9. 禁止事项

- 不在未说明的情况下修改部署模板（`dossier-aggr/templates/`）或 Helm 配置（`dossier-aggr/values.yaml`）。
- 不引入与当前任务无关的新依赖。
- 不进行大规模格式化导致噪音 diff。
- 不提交 `.protocol/`、`.codex/`、`.vscode/`、缓存、本地数据库、日志、`.env*` 等本地文件。

## 10. 输出与协作约定

- 提交结果时说明本次改动文件清单。
- 明确说明验证命令是否执行。
- 若未执行或执行失败，提供具体原因。
