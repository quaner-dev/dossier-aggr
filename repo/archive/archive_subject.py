import asyncio
from collections.abc import Sequence
from typing import Any, cast

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core import exceptions, settings
from core.database import engine
from models import ArchiveSubject
from schemas import ArchiveSubjectQuery

_TABLE_INIT_LOCK = asyncio.Lock()
_TABLE_READY = False


async def _ensure_table() -> None:
    """保留 ArchiveSubject 表的启动期兼容兜底。

    正式 schema 已由 Alembic 迁移管理；这里的 `create_all` 只用于兼容
    尚未执行迁移的本地或测试环境。
    """

    global _TABLE_READY
    if _TABLE_READY:
        return
    if settings.ENV != "dev":
        _TABLE_READY = True
        return

    async with _TABLE_INIT_LOCK:
        if _TABLE_READY:
            return
        async with engine.begin() as conn:
            table = cast(Any, ArchiveSubject).__table__
            await conn.run_sync(
                SQLModel.metadata.create_all,
                tables=[table],
            )
        _TABLE_READY = True


async def query_archive_subjects_repo(
    query: ArchiveSubjectQuery | None = None,
) -> Sequence[ArchiveSubject]:
    """按 GA/T 2350.5 B.9 查询人员档案明细。

    `ArchiveIDList` 先在数据库侧过滤；以图像搜图的 `SubjectID`
    需要匹配明细对象中各类 ID 列表，因此在取回候选结果后做列表交集判断。
    """

    def _picture_subject_ids() -> list[str]:
        if query is None or query.PictureQueryCondition is None:
            return []
        return [
            condition.SubjectID
            for condition in query.PictureQueryCondition.PictureQueryConditionObject
            if condition.SubjectID
        ]

    def _matches_picture_subject(subject: ArchiveSubject, subject_ids: list[str]) -> bool:
        return any(
            set(ids or []) & set(subject_ids)
            for ids in (
                subject.PersonIDList,
                subject.FaceIDList,
                subject.GaitIDList,
                subject.MotorVehicleIDList,
                subject.NonMotorVehicleIDList,
            )
        )

    await _ensure_table()
    async with AsyncSession(engine) as session:
        statement = select(ArchiveSubject)
        if query and query.ArchiveIDList:
            statement = statement.where(
                cast(Any, ArchiveSubject.ArchiveID).in_(query.ArchiveIDList)
            )

        subjects = (await session.exec(statement)).all()
        picture_subject_ids = _picture_subject_ids()
        if picture_subject_ids:
            subjects = [
                subject
                for subject in subjects
                if _matches_picture_subject(subject, picture_subject_ids)
            ]
        if not subjects:
            raise exceptions.DataNotFoundError(detail="No ArchiveSubject data exist")
        return subjects


async def create_archive_subjects_repo(
    subjects: list[ArchiveSubject],
) -> Sequence[ArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        for subject in subjects:
            statement = select(ArchiveSubject).where(
                ArchiveSubject.ArchiveID == subject.ArchiveID
            )
            if (await session.exec(statement)).first():
                raise exceptions.DataAlreadyExistsError(
                    detail=f"{subject.ArchiveID} already exists"
                )
            session.add(subject)

        await session.commit()
        for subject in subjects:
            await session.refresh(subject)
    return subjects


async def update_archive_subjects_repo(
    subjects: list[ArchiveSubject],
) -> Sequence[ArchiveSubject]:
    await _ensure_table()
    async with AsyncSession(engine) as session:
        for subject in subjects:
            statement = select(ArchiveSubject).where(
                ArchiveSubject.ArchiveID == subject.ArchiveID
            )
            if not (await session.exec(statement)).first():
                raise exceptions.DataNotFoundError(detail=f"{subject.ArchiveID} not found")
            session.add(subject)

        await session.commit()
        for subject in subjects:
            await session.refresh(subject)
    return subjects


async def delete_archive_subjects_repo(
    archive_id: str | None = None,
    face_id_list: list[str] | None = None,
    person_id_list: list[str] | None = None,
    motor_vehicle_id_list: list[str] | None = None,
    non_motor_vehicle_id_list: list[str] | None = None,
) -> list[str]:
    """按 A.14 删除键删除人员档案明细并返回匹配的 ArchiveID。

    协议删除条件允许 `ArchiveID` 或多类对象 ID 列表；任一条件命中即删除
    对应明细，返回值用于 API 层生成逐项 `ResponseStatus`。
    """

    await _ensure_table()
    async with AsyncSession(engine) as session:
        subjects = (await session.exec(select(ArchiveSubject))).all()

        def _has_overlap(
            source: list[str] | None,
            target: list[str] | None,
        ) -> bool:
            return bool(source and target and set(source) & set(target))

        def _matches(subject: ArchiveSubject) -> bool:
            return any(
                (
                    archive_id is not None and subject.ArchiveID == archive_id,
                    _has_overlap(subject.FaceIDList, face_id_list),
                    _has_overlap(subject.PersonIDList, person_id_list),
                    _has_overlap(subject.MotorVehicleIDList, motor_vehicle_id_list),
                    _has_overlap(subject.NonMotorVehicleIDList, non_motor_vehicle_id_list),
                )
            )

        matched_subjects = [subject for subject in subjects if _matches(subject)]
        deleted_ids = [subject.ArchiveID for subject in matched_subjects]

        for subject in matched_subjects:
            await session.delete(subject)

        if deleted_ids:
            await session.commit()
        return deleted_ids
