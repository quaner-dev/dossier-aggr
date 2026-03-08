from main import app


def test_2350_routes_registered_on_openapi():
    openapi = app.openapi()
    paths = openapi["paths"]

    expected_paths = {
        "/VIAS/Tasks",
        "/VIID/Subscribes",
        "/VIID/Subscribes/{subscribe_id}",
        "/VIID/SubscribeNotifications",
        "/VIID/SubscribeNotifications/{notification_id}",
        "/VIID/VehicleArchives",
        "/VIID/VehicleArchivesQuerySync",
        "/VIID/VehicleArchiveSubjects",
        "/VIID/VehicleArchiveSubjectQuerySync",
        "/VIID/ArchiveConfidence",
        "/VIID/VehicleArchiveConfidence",
    }

    for path in expected_paths:
        assert path in paths

    assert "get" in paths["/VIID/Subscribes"]
    assert "post" in paths["/VIID/Subscribes"]
    assert "put" in paths["/VIID/Subscribes"]
    assert "delete" in paths["/VIID/Subscribes"]
    assert "put" in paths["/VIID/Subscribes/{subscribe_id}"]
    assert "post" in paths["/VIID/SubscribeNotifications"]
    assert "get" in paths["/VIID/SubscribeNotifications/{notification_id}"]
