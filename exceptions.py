from typing import Union, List
from fastapi import HTTPException

import schemas
import main


class DataNotFoundError(HTTPException):
    """系统无所需数据"""

    def __init__(
        self,
        detail: Union[str, List[str]],
    ):
        super().__init__(status_code=200, detail=detail)


@main.app.exception_handler(DataNotFoundError)
async def data_not_found_exception_handler(request: Request, exc: DataNotFoundError):
    detail = exc.detail
    # TODO 这里的逻辑需要继续处理，当前exc.detail的数据永远是一个str，所以没办法通过type或者isinstance来判断数据类型
