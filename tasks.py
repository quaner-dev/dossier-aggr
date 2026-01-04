import logging
import schemas
import brokers


@brokers.broker.task
async def create_face(face: schemas.face.Face):
    logging.info(face)


@brokers.broker.task
async def create_person(person: schemas.person.Person): ...


@brokers.broker.task
async def create_subscribe_notification(
    subscribe_notification: schemas.subscribe_notification.SubscribeNotification,
): ...
