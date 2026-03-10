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

taskiq worker core.brokers:broker

当前的架构中使用api来接收请求，使用service来处理业务逻辑，使用task来进行异步处理
当前对于api中的检索操作，准确来说是对于service中的处理，检索其实是要使用service中进行处理，但是task需要使用的是异步处理，我的想法是在task中实现相关检索的逻辑，但是不处理异步任务，只处理同步任务，这样保证task中完全实现检索的逻辑，防止删除、更新和检索的路径不同

从设计层面来讲，当前所有的schema和model其实都是同根同源的，都是来源于一个base，因此在这里，其实就可以将两者的转换问题给解决，直接使用model_validate就可以解决转换问题
