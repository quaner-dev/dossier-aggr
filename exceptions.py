from fastapi import HTTPException


class DataNotFoundError(HTTPException):
    """系统无所需数据"""

    def __init__(
        self,
        detail: str | list[str],
    ):
        super().__init__(status_code=404, detail=detail)


class InvalidParameterError(HTTPException):
    """无效参数错误"""

    def __init__(
        self,
        detail: str | list[str],
    ):
        super().__init__(status_code=400, detail=detail)


class DataAlreadyExistsError(HTTPException):
    """数据已存在"""

    def __init__(
        self,
        detail: str | list[str],
    ):
        super().__init__(status_code=409, detail=detail)


class TaskExecutionError(HTTPException):
    """任务执行失败"""

    def __init__(
        self,
        detail: str | list[str],
    ):
        super().__init__(status_code=503, detail=detail)
