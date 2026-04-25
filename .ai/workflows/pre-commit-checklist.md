# Pre-Commit Checklist

提交前检查：

- `git status --short`
- `git diff --check`
- `git ls-files -ci --exclude-standard`
- 搜索旧文档路径引用，确认没有指向已删除文档目录或旧计划目录的链接。
- `git ls-files .protocol`，确认原始协议文件未被 Git 跟踪。
- `pytest -q`

如果测试命令无法运行，记录具体原因。

不要提交：

- `.protocol/`
- `.codex/`
- `.vscode/`
- `.env*`
- `db.sqlite3`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- 日志、coverage、构建产物
