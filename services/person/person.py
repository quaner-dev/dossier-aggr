from collections.abc import Sequence
from typing import Any
from fastapi import Request
from core import settings
from message.kafka import publish_message
from message.dispatch import MessageUnavailableError
from services.image_upload import transform_images

from domain import Person as PersonData
from models import Person
from repo.person.person import (
    create_person_repo,
    create_persons_repo,
    delete_person_repo,
    delete_persons_repo,
    get_person_repo,
    list_persons_repo,
    update_person_repo,
    update_persons_repo,
)
from services.model_conversion import to_table_model, to_table_models


class PersonService:
    """编排 GA/T 1400 人员资源业务链路。

    读写请求统一委托 repo，保证请求完成时数据已经持久化。
    """

    async def get_person(self, person_id: str) -> Person:
        """根据PersonID查询人员信息"""
        return await get_person_repo(person_id=person_id)

    async def list_persons(self) -> list[Person]:
        """查询所有人员信息"""
        return list(await list_persons_repo())

    async def create_person(self, person: PersonData) -> Person:
        """创建人员信息"""
        return await create_person_repo(person=to_table_model(Person, person))

    async def create_persons(self, persons: Sequence[PersonData], *, request: Request | None = None, payload: dict[str, Any] | None = None) -> list[Person]:
        """创建多个人员信息"""
        if request is not None:
            storage = getattr(request.app.state, "object_storage", None)
            producer = getattr(request.app.state, "kafka_producer", None)
            bucket = getattr(request.app.state, "object_storage_bucket_prefix", settings.OBJECT_STORAGE_BUCKET_PREFIX)
            if storage is None or producer is None or not bucket:
                raise MessageUnavailableError()
            body = payload if payload is not None else await request.json()
            await transform_images(body, storage=storage, bucket=bucket)
            await publish_message(producer=producer, topic="viid.persons.v1", payload=body)
            return []
        return await create_persons_repo(persons=to_table_models(Person, persons))

    async def update_person(self, person: PersonData) -> Person:
        """更新人员信息"""
        return await update_person_repo(person=to_table_model(Person, person))

    async def update_persons(self, persons: Sequence[PersonData]) -> list[Person]:
        """批量更新人员信息"""
        return await update_persons_repo(persons=to_table_models(Person, persons))

    async def delete_person(self, person_id: str) -> str:
        """删除人员信息"""
        return await delete_person_repo(person_id=person_id)

    async def delete_persons(self, person_ids: list[str]) -> list[str]:
        """批量删除人员信息"""
        return await delete_persons_repo(person_ids=person_ids)
