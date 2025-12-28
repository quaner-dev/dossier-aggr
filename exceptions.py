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
