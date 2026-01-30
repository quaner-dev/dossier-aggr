from sqlmodel import select

from models import Subscribe
import exceptions


class SubscribeService():
    async def batch_create_subscribe(self, subscribes: list[Subscribe]):
        for subscribe in subscribes:
            self.session.add(Subscribe.model_validate(subscribe))

        await self.session.commit()

    async def get_subscribe(self, subscribe_id: str) -> Subscribe:
        """根据SubscribeID查询订阅信息"""
        statement = select(Subscribe).where(Subscribe.SubscribeID == subscribe_id)
        subscribe = (await self.session.exec(statement)).first()
        if not subscribe:
            raise exceptions.DataNotFoundError(detail=f"{subscribe_id} not exist")
        return Subscribe.model_validate(subscribe)

    async def list_subscribes(self) -> list[Subscribe]:
        """查询所有订阅信息"""
        statement = select(Subscribe)
        subscribes = (await self.session.exec(statement)).all()
        if not subscribes:
            raise exceptions.DataNotFoundError(detail="No Subscribe data exist")
        return [Subscribe.model_validate(subscribe) for subscribe in subscribes]

    async def update_subscribe(
        self, subscribe_id: str, subscribe: Subscribe
    ) -> Subscribe:
        """更新订阅信息"""
        statement = select(Subscribe).where(Subscribe.SubscribeID == subscribe_id)
        db_subscribe = (await self.session.exec(statement)).first()
        if not db_subscribe:
            raise exceptions.DataNotFoundError(detail=f"{subscribe_id} not exist")

        for key, value in subscribe.model_dump(exclude={"id"}).items():
            setattr(db_subscribe, key, value)

        self.session.add(db_subscribe)
        await self.session.commit()
        await self.session.refresh(db_subscribe)
        return db_subscribe

    async def delete_subscribe(self, subscribe_id: str) -> None:
        """删除订阅信息"""
        statement = select(Subscribe).where(Subscribe.SubscribeID == subscribe_id)
        db_subscribe = (await self.session.exec(statement)).first()
        if not db_subscribe:
            raise exceptions.DataNotFoundError(detail=f"{subscribe_id} not exist")

        await self.session.delete(db_subscribe)
        await self.session.commit()
