"""align 2350 official models

Revision ID: 7f7fb248ab04
Revises: c2a4d9f73c51
Create Date: 2026-03-11 18:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7f7fb248ab04"
down_revision: str | Sequence[str] | None = "c2a4d9f73c51"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _table_exists(table_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    with op.batch_alter_table("archive", recreate="always") as batch_op:
        batch_op.add_column(sa.Column("SourceIDList", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("CenterFeatureList", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("Similaritydegree", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("Confidence", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("SubImageList", sa.JSON(), nullable=True))
        batch_op.drop_column("IDType")
        batch_op.drop_column("IDNumber")
        batch_op.drop_column("Name")
        batch_op.drop_column("BirthTime")
        batch_op.drop_column("ImageID")

    with op.batch_alter_table("vehiclearchive", recreate="always") as batch_op:
        batch_op.add_column(sa.Column("SourceIDList", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("SubImageList", sa.JSON(), nullable=True))
        batch_op.drop_column("ImageID")

    with op.batch_alter_table("subscribenotification", recreate="always") as batch_op:
        batch_op.add_column(sa.Column("ArchiveObjectList", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("VehicleArchiveObjectList", sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column("ArchiveSubjectList", sa.JSON(), nullable=True))

    if _table_exists("archivesubject"):
        with op.batch_alter_table("archivesubject", recreate="always") as batch_op:
            batch_op.add_column(sa.Column("GaitIDList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("MotorVehicleIDList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("NonMotorVehicleIDList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("GaitObjectList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("MotorVehicleObjectList", sa.JSON(), nullable=True))
            batch_op.add_column(
                sa.Column("NonMotorVehicleObjectList", sa.JSON(), nullable=True)
            )
            if "ImageID" in {
                column["name"] for column in sa.inspect(op.get_bind()).get_columns("archivesubject")
            }:
                batch_op.drop_column("ImageID")
    else:
        op.create_table(
            "archivesubject",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column(
                "ArchiveID", sqlmodel.sql.sqltypes.AutoString(length=48), nullable=False
            ),
            sa.Column("PersonIDList", sa.JSON(), nullable=True),
            sa.Column("FaceIDList", sa.JSON(), nullable=True),
            sa.Column("GaitIDList", sa.JSON(), nullable=True),
            sa.Column("MotorVehicleIDList", sa.JSON(), nullable=True),
            sa.Column("NonMotorVehicleIDList", sa.JSON(), nullable=True),
            sa.Column("PersonObjectList", sa.JSON(), nullable=True),
            sa.Column("FaceObjectList", sa.JSON(), nullable=True),
            sa.Column("GaitObjectList", sa.JSON(), nullable=True),
            sa.Column("MotorVehicleObjectList", sa.JSON(), nullable=True),
            sa.Column("NonMotorVehicleObjectList", sa.JSON(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("ArchiveID"),
        )

    if _table_exists("vehiclearchivesubject"):
        with op.batch_alter_table("vehiclearchivesubject", recreate="always") as batch_op:
            batch_op.add_column(sa.Column("PersonIDList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("FaceIDList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("GaitIDList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("PersonObjectList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("FaceObjectList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("GaitObjectList", sa.JSON(), nullable=True))
            batch_op.add_column(sa.Column("MotorVehicleObjectList", sa.JSON(), nullable=True))
            batch_op.add_column(
                sa.Column("NonMotorVehicleObjectList", sa.JSON(), nullable=True)
            )
            if "ImageID" in {
                column["name"]
                for column in sa.inspect(op.get_bind()).get_columns("vehiclearchivesubject")
            }:
                batch_op.drop_column("ImageID")
    else:
        op.create_table(
            "vehiclearchivesubject",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column(
                "ArchiveID", sqlmodel.sql.sqltypes.AutoString(length=48), nullable=False
            ),
            sa.Column("MotorVehicleIDList", sa.JSON(), nullable=True),
            sa.Column("PersonIDList", sa.JSON(), nullable=True),
            sa.Column("FaceIDList", sa.JSON(), nullable=True),
            sa.Column("GaitIDList", sa.JSON(), nullable=True),
            sa.Column("NonMotorVehicleIDList", sa.JSON(), nullable=True),
            sa.Column("PersonObjectList", sa.JSON(), nullable=True),
            sa.Column("FaceObjectList", sa.JSON(), nullable=True),
            sa.Column("GaitObjectList", sa.JSON(), nullable=True),
            sa.Column("MotorVehicleObjectList", sa.JSON(), nullable=True),
            sa.Column("NonMotorVehicleObjectList", sa.JSON(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("ArchiveID"),
        )


def downgrade() -> None:
    if _table_exists("vehiclearchivesubject"):
        with op.batch_alter_table("vehiclearchivesubject", recreate="always") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "ImageID",
                    sqlmodel.sql.sqltypes.AutoString(length=41),
                    nullable=True,
                )
            )
            batch_op.drop_column("PersonIDList")
            batch_op.drop_column("FaceIDList")
            batch_op.drop_column("GaitIDList")
            batch_op.drop_column("PersonObjectList")
            batch_op.drop_column("FaceObjectList")
            batch_op.drop_column("GaitObjectList")
            batch_op.drop_column("MotorVehicleObjectList")
            batch_op.drop_column("NonMotorVehicleObjectList")

    if _table_exists("archivesubject"):
        with op.batch_alter_table("archivesubject", recreate="always") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "ImageID",
                    sqlmodel.sql.sqltypes.AutoString(length=41),
                    nullable=True,
                )
            )
            batch_op.drop_column("GaitIDList")
            batch_op.drop_column("MotorVehicleIDList")
            batch_op.drop_column("NonMotorVehicleIDList")
            batch_op.drop_column("GaitObjectList")
            batch_op.drop_column("MotorVehicleObjectList")
            batch_op.drop_column("NonMotorVehicleObjectList")

    with op.batch_alter_table("subscribenotification", recreate="always") as batch_op:
        batch_op.drop_column("ArchiveObjectList")
        batch_op.drop_column("VehicleArchiveObjectList")
        batch_op.drop_column("ArchiveSubjectList")

    with op.batch_alter_table("vehiclearchive", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column(
                "ImageID",
                sqlmodel.sql.sqltypes.AutoString(length=41),
                nullable=True,
            )
        )
        batch_op.drop_column("SourceIDList")
        batch_op.drop_column("SubImageList")

    with op.batch_alter_table("archive", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("IDType", sqlmodel.sql.sqltypes.AutoString(length=3), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "IDNumber", sqlmodel.sql.sqltypes.AutoString(length=30), nullable=True
            )
        )
        batch_op.add_column(
            sa.Column("Name", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True)
        )
        batch_op.add_column(sa.Column("BirthTime", sa.DateTime(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "ImageID",
                sqlmodel.sql.sqltypes.AutoString(length=41),
                nullable=True,
            )
        )
        batch_op.drop_column("SourceIDList")
        batch_op.drop_column("CenterFeatureList")
        batch_op.drop_column("Similaritydegree")
        batch_op.drop_column("Confidence")
        batch_op.drop_column("SubImageList")
