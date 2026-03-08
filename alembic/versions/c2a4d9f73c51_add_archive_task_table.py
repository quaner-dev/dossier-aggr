"""add archive task table

Revision ID: c2a4d9f73c51
Revises: ba1f5f1f8b9e
Create Date: 2026-03-01 02:40:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "c2a4d9f73c51"
down_revision: Union[str, Sequence[str], None] = "ba1f5f1f8b9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "archivetask",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("TaskID", sqlmodel.sql.sqltypes.AutoString(length=48), nullable=False),
        sa.Column(
            "TaskName", sqlmodel.sql.sqltypes.AutoString(length=128), nullable=True
        ),
        sa.Column(
            "ArchiveLibraryID",
            sqlmodel.sql.sqltypes.AutoString(length=48),
            nullable=True,
        ),
        sa.Column("EventType", sqlmodel.sql.sqltypes.AutoString(length=8), nullable=True),
        sa.Column("Status", sqlmodel.sql.sqltypes.AutoString(length=32), nullable=True),
        sa.Column("CreateTime", sa.DateTime(), nullable=False),
        sa.Column("UpdateTime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("TaskID"),
    )


def downgrade() -> None:
    op.drop_table("archivetask")
