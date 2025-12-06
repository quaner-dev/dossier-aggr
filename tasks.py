from typing import Any, Dict, List
import arq

REDIS_SETTINGS = arq.connections.RedisSettings()


async def test(ctx: Dict[str, Any], notification: str):
    print(type(ctx))
    print(notification)


class WorkerSettings:
    functions: List[Any] = [test]
    redis_settings = REDIS_SETTINGS
