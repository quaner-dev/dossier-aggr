from models import Gait, VehicleArchive


def test_vehicle_archive_model_validate_roundtrip():
    payload = {
        "ArchiveID": "VA-001",
        "ArchiveLibraryID": "LIB-001",
        "PlateNo": "ABC123",
        "VehicleClass": "K11",
        "CreateTime": "20260101120000",
        "UpdateTime": "20260101120000",
        "ImageID": "IMG-VA-001",
    }

    model = VehicleArchive.model_validate(payload)
    dumped = model.model_dump(mode="json")

    assert dumped["ArchiveID"] == "VA-001"
    assert dumped["ArchiveLibraryID"] == "LIB-001"
    assert dumped["PlateNo"] == "ABC123"


def test_gait_model_schema_contains_expected_fields():
    schema = Gait.model_json_schema()
    props = schema.get("properties", {})

    assert "Vendor" in props
    assert "AlgorithmVersion" in props
    assert "GaitData" in props
