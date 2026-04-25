# Project Overview

更新时间：2026-03-11

`dossier-aggr` 是一个 VIID 协议服务，当前包含两类能力：

- GA/T 1400：系统注册、保活、注销、采集系统与设备、人员、人脸、订阅与通知。
- GA/T 2350.5：档案库、档案、档案明细、档案核验等主链路。

技术栈：

- API 框架：`FastAPI`
- 数据层：`SQLModel` + `SQLAlchemy AsyncSession`
- 任务队列：`Taskiq`
- 迁移：`Alembic`

当前 2350 主链路已可运行，但与正式版 GA/T 2350.5-2025 仍存在差异。协议相关判断必须先查 `.ai/protocols/`，必要时回到本地 `.protocol/` 原始文件核验。
