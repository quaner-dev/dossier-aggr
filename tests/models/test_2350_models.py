from models import (
    Archive,
    ArchiveQuery,
    ArchiveSubject,
    Gait,
    SubImageInfo,
    VehicleArchive,
    enums,
)
from models.common.common import FieldsType


def _sub_image_payload(image_id: str, image_type: enums.ImageTypeEnum) -> dict:
    return SubImageInfo(
        ImageID=image_id,
        Type=image_type,
        FileFormat=enums.ImageFormatEnum.JPEG,
        Width=128,
        Height=256,
        Data="aW1hZ2UtYnl0ZXM=",
        FeatureInfoObject={
            "Vendor": "vendor-a",
            "AlgorithmVersion": "v1",
            "FeatureData": "ZmVhdHVyZQ==",
        },
    ).model_dump(mode="json")


def test_archive_model_validate_roundtrip():
    payload = {
        "ArchiveID": "A-001",
        "ArchiveLibraryID": "LIB-001",
        "CreateTime": "20260101120000",
        "UpdateTime": "20260101120000",
        "SourceIDList": ["PERSON-001", "FACE-001"],
        "CenterFeatureList": {
            "FeatureInfoObject": [
                {
                    "Vendor": "vendor-a",
                    "AlgorithmVersion": "v1",
                    "FeatureData": "ZmVhdHVyZQ==",
                }
            ]
        },
        "Similaritydegree": 0.92,
        "Confidence": 0.83,
        "SubImageList": {
            "SubImageInfoObject": [
                _sub_image_payload("IMG-A-001", enums.ImageTypeEnum.PersonImage)
            ]
        },
    }

    model = Archive.model_validate(payload)
    dumped = model.model_dump(mode="json")

    assert dumped["ArchiveID"] == "A-001"
    assert dumped["SourceIDList"] == ["PERSON-001", "FACE-001"]
    assert dumped["CenterFeatureList"]["FeatureInfoObject"][0]["Vendor"] == "vendor-a"
    assert dumped["SubImageList"]["SubImageInfoObject"][0]["ImageID"] == "IMG-A-001"


def test_vehicle_archive_model_validate_roundtrip():
    payload = {
        "ArchiveID": "VA-001",
        "ArchiveLibraryID": "LIB-001",
        "PlateNo": "ABC123",
        "PlateColor": enums.ColorTypeEnum.Blue,
        "VehicleClass": "K11",
        "CreateTime": "20260101120000",
        "UpdateTime": "20260101120000",
        "SourceIDList": ["MV-001"],
        "SubImageList": {
            "SubImageInfoObject": [
                _sub_image_payload("IMG-VA-001", enums.ImageTypeEnum.VehicleLargeImage)
            ]
        },
    }

    model = VehicleArchive.model_validate(payload)
    dumped = model.model_dump(mode="json")

    assert dumped["ArchiveID"] == "VA-001"
    assert dumped["ArchiveLibraryID"] == "LIB-001"
    assert dumped["PlateNo"] == "ABC123"
    assert dumped["PlateColor"] == enums.ColorTypeEnum.Blue
    assert dumped["SourceIDList"] == ["MV-001"]
    assert dumped["SubImageList"]["SubImageInfoObject"][0]["ImageID"] == "IMG-VA-001"


def test_archive_query_model_validate_supports_picture_query_condition():
    payload = {
        "QueryID": "Q-2350-001",
        "PictureQueryCondition": {
            "PictureQueryConditionObject": [
                {
                    "SubImage": SubImageInfo(
                        ImageID="IMG-001",
                        Type=enums.ImageTypeEnum.PersonImage,
                        FileFormat=enums.ImageFormatEnum.JPEG,
                        Width=128,
                        Height=256,
                        Data="aW1hZ2UtYnl0ZXM=",
                        FeatureInfoObject={
                            "Vendor": "vendor-a",
                            "AlgorithmVersion": "v1",
                            "FeatureData": "ZmVhdHVyZQ==",
                        },
                    ).model_dump(mode="json"),
                    "Threshold": 0.91,
                    "SubjectID": "FACE-001",
                }
            ]
        },
    }

    model = ArchiveQuery.model_validate(payload)
    dumped = model.model_dump(mode="json")

    assert dumped["QueryID"] == "Q-2350-001"
    assert dumped["PictureQueryCondition"]["PictureQueryConditionObject"][0]["SubjectID"] == (
        "FACE-001"
    )
    assert dumped["PictureQueryCondition"]["PictureQueryConditionObject"][0]["Threshold"] == 0.91


def test_fields_type_schema_matches_official_b14_fields():
    schema = FieldsType.model_json_schema()
    props = schema.get("properties", {})

    assert set(props) == {
        "ArchiveLibraryID",
        "ArchiveIDList",
        "PlaceCode",
        "PlateNos",
        "PlateColor",
        "VehicleClass",
        "VehicleBrand",
        "VehicleModel",
        "VehicleColor",
        "VehicleStyles",
    }


def test_fields_type_model_validate_accepts_partial_filters():
    model = FieldsType.model_validate({"ArchiveIDList": ["A-001"]})

    assert model.ArchiveIDList == ["A-001"]
    assert model.ArchiveLibraryID is None
    assert model.PlaceCode is None


def test_archive_model_schema_matches_official_b3_fields():
    schema = Archive.model_json_schema()
    props = schema.get("properties", {})

    assert set(props) - {"id"} == {
        "ArchiveID",
        "ArchiveLibraryID",
        "CreateTime",
        "UpdateTime",
        "SourceIDList",
        "CenterFeatureList",
        "Similaritydegree",
        "Confidence",
        "SubImageList",
    }


def test_vehicle_archive_model_schema_matches_official_b4_fields():
    schema = VehicleArchive.model_json_schema()
    props = schema.get("properties", {})

    assert set(props) - {"id"} == {
        "ArchiveID",
        "ArchiveLibraryID",
        "PlateNo",
        "PlateColor",
        "VehicleClass",
        "VehicleBrand",
        "VehicleModel",
        "VehicleColor",
        "VehicleStyles",
        "CreateTime",
        "UpdateTime",
        "SourceIDList",
        "SubImageList",
    }


def test_archive_subject_model_schema_matches_official_b5_fields():
    schema = ArchiveSubject.model_json_schema()
    props = schema.get("properties", {})

    assert set(props) - {"id"} == {
        "ArchiveID",
        "PersonIDList",
        "FaceIDList",
        "GaitIDList",
        "MotorVehicleIDList",
        "NonMotorVehicleIDList",
        "PersonObjectList",
        "FaceObjectList",
        "GaitObjectList",
        "MotorVehicleObjectList",
        "NonMotorVehicleObjectList",
    }


def test_gait_model_schema_matches_official_b16_fields():
    schema = Gait.model_json_schema()
    props = schema.get("properties", {})

    assert set(props) == {
        "GaitID",
        "SourceID",
        "Angle",
        "GaitAppearTime",
        "GaitDisappearTime",
        "Similaritydegree",
        "InfoKind",
        "GenderCode",
        "AgeUpLimit",
        "AgeLowerLimit",
        "AccompanyNumber",
        "HeightUpLimit",
        "HeightLowerLimit",
        "SubImageList",
    }
