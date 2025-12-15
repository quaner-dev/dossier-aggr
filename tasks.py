import schemas
import brokers


@brokers.broker.task
async def create_face(face: schemas.Face): ...


@brokers.broker.task
async def create_person(person: schemas.Person): ...
