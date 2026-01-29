from sqlmodel import select

from models import Archive
import exceptions
from services.common.common import BaseService


class ArchiveService(BaseService):
    async def list_archives(self):...
        # statement = select(Archive).where(**archive_query.model_dump())
        # archives = (await self.session.exec(statement)).all()
        # return [Archive.model_validate(archive) for archive in archives]

    async def batch_create_archive(self, archives: list[Archive]):
        for archive in archives:
            self.session.add(Archive.model_validate(archive))

        await self.session.commit()

    async def delete_archive(self, archive_id: str) -> None:
        """删除档案信息"""
        statement = select(Archive).where(Archive.ArchiveID == archive_id)
        db_archive = (await self.session.exec(statement)).first()
        if not db_archive:
            raise exceptions.DataNotFoundError(detail=f"{archive_id} not exist")

        await self.session.delete(db_archive)
        await self.session.commit()
