# Database Migration Workflow

1. 修改 `models/` 中的表模型。
2. 检查 `alembic/env.py` 是否能通过 `sqlmodel.SQLModel.metadata` 发现模型。
3. 生成迁移：

```bash
alembic revision --autogenerate -m "<message>"
```

4. 审核迁移文件，确认无无关 schema 变更。
5. 执行迁移：

```bash
alembic upgrade head
```

6. 更新或新增 `tests/migrations/` 测试。
7. 同步更新 `.ai/project/data-models.md`。
