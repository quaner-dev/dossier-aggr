# VIID 服务系统

基于 FastAPI 构建的的视图库应用（协议为 GA/T 1400 - 2017 和 GA/T 1400 2018 试行）以及目标聚档（GA/T 2305 2025）协议实现，提供视频图像信息数据库的标准接口服务。

## 项目简介

VIID 服务系统实现了公安部视频图像信息数据库（VIID）协议，提供标准化的视频图像数据采集、管理和查询接口。系统采用现代 Python 技术栈构建，支持高并发处理和异步任务队列。

## 技术栈

- **后端框架**: FastAPI + SQLModel
- **任务队列**: Taskiq + RabbitMQ
- **数据库**: SQLite
- **部署**: Kubernetes + Docker

## 迁移数据库

alembic revision --autogenerate -m "init"
alembic upgrade head

## 启动服务

uvicorn main:app --host 0.0.0.0 -p 8000

taskiq worker broker:broker
