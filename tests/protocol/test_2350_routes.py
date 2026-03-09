from main import app


def test_2350_routes_registered_on_openapi():
    openapi = app.openapi()
    paths = openapi["paths"]

    expected_paths = {
        "/VIID/ArchiveLibraries",
        "/VIID/Subscribes",
        "/VIID/Subscribes/{subscribe_id}",
        "/VIID/SubscribeNotifications",
        "/VIID/VehicleArchives",
        "/VIID/VehicleArchivesQuerySync",
        "/VIID/VehicleArchiveSubjects",
        "/VIID/VehicleArchiveSubjectQuerySync",
        "/VIID/ArchiveConfidence",
        "/VIID/VehicleArchiveConfidence",
    }

    for path in expected_paths:
        assert path in paths

    assert "/VIID/ArchiveLibraryQuerySync" not in paths
    assert "/VIAS/Tasks" not in paths
    assert "get" in paths["/VIID/ArchiveLibraries"]
    assert "post" in paths["/VIID/ArchiveLibraries"]
    assert "put" in paths["/VIID/ArchiveLibraries"]
    assert "delete" in paths["/VIID/ArchiveLibraries"]

    assert "get" in paths["/VIID/Subscribes"]
    assert "post" in paths["/VIID/Subscribes"]
    assert "put" in paths["/VIID/Subscribes"]
    assert "delete" in paths["/VIID/Subscribes"]
    assert "put" in paths["/VIID/Subscribes/{subscribe_id}"]
    assert "post" in paths["/VIID/SubscribeNotifications"]
    assert "get" in paths["/VIID/SubscribeNotifications"]
    assert "delete" in paths["/VIID/SubscribeNotifications"]
    assert "post" in paths["/VIID/VehicleArchivesQuerySync"]
    assert "post" in paths["/VIID/VehicleArchives"]
    assert "put" in paths["/VIID/VehicleArchives"]
    assert "delete" in paths["/VIID/VehicleArchives"]
    assert "get" not in paths["/VIID/VehicleArchives"]
