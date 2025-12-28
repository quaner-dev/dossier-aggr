import logging
import schemas
import brokers


@brokers.broker.task
async def create_face(face: schemas.Face):
    logging.info(face)


@brokers.broker.task
async def create_person(person: schemas.Person): ...


@brokers.broker.task
async def create_subscribe_notification(
    subscribe_notification: schemas.SubscribeNotification,
): ...
