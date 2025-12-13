import schemas
from brokers import broker


@broker.task
async def create_face(face: schemas.Face): ...


@broker.task
async def create_person(person: schemas.Person): ...
