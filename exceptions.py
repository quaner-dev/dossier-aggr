class DataNotFoundError(Exception):
    """系统无所需数据"""

    def __init__(self, message: str = "系统无所需数据"):
        self.message = message
        super().__init__(message)
