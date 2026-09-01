# Domain、Model 与 Schema 分层实现说明

本文记录 `domain/`、`models/` 和 `schemas/` 的实现边界及本次重构步骤。
本次只移动和提取现有代码，不改变 HTTP 协议、数据库结构或业务行为。

## 1. 目标与约束

本次改动必须满足：

1. 不增加或删除现有协议字段和数据库列。
2. 不修改字段名称、大小写、类型、默认值、必填性、枚举、长度限制和日期格式。
3. 不修改 HTTP 方法、路径、查询参数、外层对象和 JSON 序列化形状。
4. 不增加索引、唯一约束、外键、迁移或依赖。
5. 不保留旧的 `models.*Schema` 兼容导出。
6. 不提前实施列表 JSON 字段的关系表拆分。

## 2. 分层职责

### 2.1 `domain/`

domain 使用非表 `SQLModel` 定义可被其他层继承的实体字段和共享值对象，包括：

- Archive、VehicleArchive、ArchiveSubject 等实体的共有标量字段。
- APE、APS、Person、Face、Subscribe 等实体的共有标量字段。
- FeatureInfo、SubImageInfo、ResponseStatus 等共享值对象。
- 枚举、日期时间校验和序列化类型。

domain 不包含：

- `table=True`、数据库主键和表级约束。
- 任何 `*List` 列表容器。
- HTTP 外层 `*Schema` 包装。
- 查询请求、查询结果和分页参数。
- SQLAlchemy JSON 列配置。

domain 不依赖 models 或 schemas。

### 2.2 `schemas/`

schemas 使用非表 `SQLModel`，负责 FastAPI 请求和响应校验。它包含：

- 所有 `*List` 列表容器。
- Archive、Person、Face 等实体的协议列表字段。
- ArchiveQuery、ArchiveSubjectQuery、查询结果和 FaceQueryParams。
- `ArchiveListSchema`、`ResponseStatusListSchema` 等 HTTP 外层包装。

带列表字段的协议实体继承对应 domain 实体，只增加当前协议已经存在的列表字段：

```python
class Person(PersonDomain):
    SubImageList: SubImageInfoList | None = Field(
        default=None,
        description="图像列表",
    )


class PersonList(SQLModel):
    PersonObject: list[Person]
```

schemas 不定义数据库表，不导入 table model。

schemas 的目录和实体文件按业务与 domain、models 一一对应。例如：

```text
domain/archive/archive.py
models/archive/archive.py
schemas/archive/archive.py

domain/person/person.py
models/person/person.py
schemas/person/person.py
```

同一实体对应的 `*List` 和 HTTP 外层 `*Schema` 放在该实体的 schema 文件中；
只属于请求或结果协议的对象使用同一业务目录下的独立同名文件，例如
`schemas/archive/archive_query.py` 和
`schemas/archive/archive_query_result.py`。不再使用单个聚合文件集中保存所有 schema。

### 2.3 `models/`

models 只保存 PostgreSQL 表实体。表模型直接继承 domain，不重复继承
`SQLModel`：

```python
class Person(PersonDomain, table=True):
    __table_args__ = (UniqueConstraint("PersonID"),)

    id: int | None = Field(default=None, primary_key=True, exclude=True)
```

model 只增加当前数据库映射需要的内容：

- `table=True`。
- 现有 `id` 主键。
- 现有唯一约束。
- 当前仍存在的 JSON 列及其 SQLAlchemy 配置。

不能写成 `class Person(PersonDomain, SQLModel, table=True)`，因为
`PersonDomain` 已经继承 SQLModel；再次继承是多余的基类声明。

## 3. List 与 JSON 列的过渡边界

所有列表容器都属于 schemas，即使当前某些列表对象仍被保存到 JSON 列，例如：

- `Archive.SubImageList`。
- `Archive.CenterFeatureList`。
- `ArchiveSubject.PersonObjectList`。
- `SubscribeNotification.ArchiveObjectList`。

本次不能删除这些现有列，也不能提前拆表。因此，过渡期内 table model 为声明现有
JSON 列，可以引用 schemas 中的列表容器：

```text
domain entity
     ▲
     ├──────── schemas list/entity validation
     │
models table ──────── schemas list type（仅现有 JSON 列）
```

这项依赖只服务于现有 JSON 映射。后续把列表元素拆成独立 table model 和关系后，
应从 table model 中移除相应 JSON 字段及对 schemas 列表类型的依赖，并单独提供
Alembic 迁移。该后续工作不属于本次重构。

## 4. 数据流

写入路径：

```text
HTTP JSON
  -> schemas SQLModel 校验
  -> service 转换
  -> models table entity
  -> repository
  -> PostgreSQL transaction
```

读取路径：

```text
PostgreSQL
  -> models table entity
  -> schemas 响应校验和列表包装
  -> HTTP JSON
```

事务边界保持不变：写请求只能在 PostgreSQL 提交成功后返回协议成功；批量请求仍
保持单次事务一致性。

## 5. 实现步骤

1. 使用非表 SQLModel 建立 domain 实体和共享值对象。
2. 按照与 domain、models 一一对应的业务目录和文件，将所有 `*List`、查询对象和
   HTTP 包装迁入 schemas。
3. 让需要列表字段的 schema 实体继承对应 domain 实体。
4. 让 table model 直接继承 domain，并仅保留主键、约束和当前 JSON 映射。
5. 更新 API、service、repository 和测试导入。
6. 删除 models 中旧的协议对象和兼容导出。
7. 对比协议字段、JSON 外形和 SQLModel metadata。
8. 运行静态检查和测试。

## 6. 验收标准

完成后必须满足：

1. `domain/` 中不存在 `*List` 类。
2. schemas 中的实体继承 domain，列表及 HTTP 包装只在 schemas 定义。
3. table model 的直接基类只有对应 domain 类，不重复继承 SQLModel。
4. models 只导出 table model，不导出 `*Schema`。
5. 现有表、列、主键、唯一约束和 JSON 列保持不变。
6. 现有请求和响应 JSON 外形保持不变。
7. 没有 Alembic 迁移，因为本次没有数据库 schema 变化。
8. 不存在旧 `models.*Schema` 兼容路径。
9. schemas 不存在集中定义全部协议对象的聚合模块，业务目录和实体文件与
   domain、models 一一对应。

验证命令：

```bash
git diff --check
ruff check .
pyright
pytest -q
```

若协议字段快照或数据库 metadata 对比出现差异，应先修正本次重构，不把差异解释为
后续列表拆表的一部分。
