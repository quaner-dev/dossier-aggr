"""add vehicle archive table

Revision ID: ba1f5f1f8b9e
Revises: a272a22d0455
Create Date: 2026-03-01 02:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ba1f5f1f8b9e"
down_revision: str | Sequence[str] | None = "a272a22d0455"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "vehiclearchive",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "ArchiveID", sqlmodel.sql.sqltypes.AutoString(length=48), nullable=False
        ),
        sa.Column(
            "ArchiveLibraryID",
            sqlmodel.sql.sqltypes.AutoString(length=48),
            nullable=True,
        ),
        sa.Column("PlateNo", sqlmodel.sql.sqltypes.AutoString(length=16), nullable=True),
        sa.Column(
            "PlateColor",
            sa.Enum(
                "Black",
                "White",
                "Gray",
                "Red",
                "Blue",
                "Yellow",
                "Orange",
                "Brown",
                "Green",
                "Purple",
                "Cyan",
                "Pink",
                "Transparent",
                "Other",
                name="colortypeenum",
            ),
            nullable=True,
        ),
        sa.Column(
            "VehicleClass", sqlmodel.sql.sqltypes.AutoString(length=3), nullable=True
        ),
        sa.Column(
            "VehicleBrand",
            sa.Enum(
                "other",
                "volkswagen",
                "buick",
                "bmw",
                "honda",
                "peugeot",
                "toyota",
                "ford",
                "nissan",
                "audi",
                "mazda",
                "chevrolet",
                "citroen",
                "hyundai",
                "chery",
                "kia",
                "roewe",
                "mitsubishi",
                "skoda",
                "geely",
                "zhonghua",
                "volvo",
                "lexus",
                "fiat",
                "geely_emgrand",
                "dongfeng",
                "byd",
                "suzuki",
                "jinbei",
                "haima",
                "wuling",
                "jac",
                "subaru",
                "londinium",
                "greatwall",
                "hafei",
                "qingling_isuzu",
                "southeast",
                "changan",
                "foton",
                "xiali",
                "benz",
                "faw",
                "iveco",
                "lifan",
                "faw_besturn",
                "crown",
                "renault",
                "jmc",
                "mg",
                "kema",
                "zotye",
                "changhe",
                "kinglong",
                "shanghai_huijong",
                "kinglong_suzhou",
                "haige",
                "yutong",
                "sinotruk",
                "north_ben_twin",
                "camc",
                "yuejin",
                "huanghai",
                "porsche",
                "cadillac",
                "infiniti",
                "geely_gleagle",
                "jeep",
                "land_rover",
                "changfeng_hunter",
                "shidai",
                "changan_car",
                "shaanxi_heavy_truck",
                "ankai",
                "shenlong",
                "daewoo",
                "zhongtong",
                "baojun",
                "baic_weiwang",
                "gac_trumpchi",
                "lufeng",
                "baic",
                "weilin",
                "opel",
                "karry",
                "huapu",
                "acura",
                "qichen",
                "baic_making",
                "luxgen",
                "yema",
                "zhongxing",
                "chrysler",
                "gac_geomobile",
                "ruilin",
                "jaguar",
                "tata_daewoo",
                "fudi",
                "lotus",
                "dualis",
                "yongyuan",
                "jiangnan",
                "dodge",
                "daton_auto",
                "northern_bus",
                "klt",
                "bentley",
                "shuchibust",
                "red_flag",
                name="vehiclebrandtypeenum",
            ),
            nullable=True,
        ),
        sa.Column(
            "VehicleModel", sqlmodel.sql.sqltypes.AutoString(length=32), nullable=True
        ),
        sa.Column(
            "VehicleColor",
            sa.Enum(
                "Black",
                "White",
                "Gray",
                "Red",
                "Blue",
                "Yellow",
                "Orange",
                "Brown",
                "Green",
                "Purple",
                "Cyan",
                "Pink",
                "Transparent",
                "Other",
                name="colortypeenum",
            ),
            nullable=True,
        ),
        sa.Column(
            "VehicleStyles", sqlmodel.sql.sqltypes.AutoString(length=16), nullable=True
        ),
        sa.Column("CreateTime", sa.DateTime(), nullable=False),
        sa.Column("UpdateTime", sa.DateTime(), nullable=False),
        sa.Column("ImageID", sqlmodel.sql.sqltypes.AutoString(length=41), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ArchiveID"),
    )


def downgrade() -> None:
    op.drop_table("vehiclearchive")
