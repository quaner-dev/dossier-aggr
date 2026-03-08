import brokers
from models import APS
from collections.abc import Sequence
from repositories.collection.aps import list_apss_repo, update_aps_repo


async def list_apss_task() -> Sequence[APS]:
    return await list_apss_repo()


@brokers.broker.task
async def update_aps_task(aps_id: str) -> APS:
    return await update_aps_repo(aps_id=aps_id)
