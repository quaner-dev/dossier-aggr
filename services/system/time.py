from datetime import datetime

from core.settings import CHINA_TZ
from domain import SystemTime


class SystemTimeService:
    async def get_system_time(self) -> SystemTime:
        """返回系统当前时间"""
        return SystemTime(LocalTime=datetime.now(tz=CHINA_TZ))
