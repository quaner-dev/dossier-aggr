import schemas
from brokers import broker


@broker.task
async def my_redis_task(face: schemas.Face):
    print(face)
