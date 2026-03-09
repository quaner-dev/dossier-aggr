from main import app


def test_1400_missing_routes_registered_on_openapi():
    paths = app.openapi()["paths"]

    assert "/VIID/Subscribes/{subscribe_id}" in paths
    assert "put" in paths["/VIID/Subscribes/{subscribe_id}"]

    assert "/VIID/SubscribeNotifications" in paths
    assert "post" in paths["/VIID/SubscribeNotifications"]
    assert "get" in paths["/VIID/SubscribeNotifications"]
    assert "delete" in paths["/VIID/SubscribeNotifications"]

    assert "/VIID/System/Time" in paths
    assert "get" in paths["/VIID/System/Time"]

    assert "/VIID/Persons/{person_id}" in paths
    assert "get" in paths["/VIID/Persons/{person_id}"]
    assert "put" in paths["/VIID/Persons/{person_id}"]
    assert "delete" in paths["/VIID/Persons/{person_id}"]

    assert "/VIID/Faces/{face_id}" in paths
    assert "get" in paths["/VIID/Faces/{face_id}"]
    assert "put" in paths["/VIID/Faces/{face_id}"]
    assert "delete" in paths["/VIID/Faces/{face_id}"]
