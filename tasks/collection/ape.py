import brokers
from models import APE
from collections.abc import Sequence
from repositories.collection.ape import list_apes_repo, update_apes_repo


async def list_apes_task() -> Sequence[APE]:
    return await list_apes_repo()


@brokers.broker.task
async def update_apes_task(apes: list[APE]):
    return await update_apes_repo(apes=apes)
