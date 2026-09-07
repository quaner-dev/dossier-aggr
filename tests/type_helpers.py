from datetime import datetime
from typing import Any

from core.settings import CHINA_TZ
from domain import (
    FeatureInfo,
    ResponseStatus,
    SubImageInfo,
    enums,
)
from schemas import FeatureInfoList, SubImageInfoList


class FakeRequest:
    def __init__(self, payload: dict[str, Any]):
        self.payload = payload

    async def json(self) -> dict[str, Any]:
        return self.payload


class FakeMessageManager:
    def __init__(self):
        self.enqueued: list[dict[str, Any]] = []

    def enqueue(self, **kwargs: Any) -> None:
        self.enqueued.append(kwargs)


def as_service(service: object) -> Any:
    return service


def as_status_list(
    value: ResponseStatus | list[ResponseStatus],
) -> list[ResponseStatus]:
    if isinstance(value, list):
        return value
    return [value]


def dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%d%H%M%S").replace(tzinfo=CHINA_TZ)


def sample_feature_info(tag: str) -> FeatureInfo:
    return FeatureInfo(
        Vendor=f"vendor-{tag}",
        AlgorithmVersion="v1",
        FeatureData=f"feature-{tag}",
    )


def sample_feature_info_list(tag: str) -> FeatureInfoList:
    return FeatureInfoList(FeatureInfoObject=[sample_feature_info(tag)])


def sample_sub_image_info(
    image_id: str,
    image_type: enums.ImageTypeEnum,
    tag: str,
) -> SubImageInfo:
    return SubImageInfo(
        ImageID=image_id,
        ImageSource="1",
        Type=image_type,
        FileFormat=enums.ImageFormatEnum.JPEG,
        Width=128,
        Height=256,
        Data=f"image-data-{tag}",
        FeatureInfoObject=sample_feature_info(tag),
    )


def sample_sub_image_list(
    image_id: str,
    image_type: enums.ImageTypeEnum,
    tag: str,
) -> SubImageInfoList:
    return SubImageInfoList(
        SubImageInfoObject=[sample_sub_image_info(image_id, image_type, tag)]
    )
