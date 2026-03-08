from main import app


def test_1400_missing_routes_registered_on_openapi():
    paths = app.openapi()["paths"]

    assert "/VIID/Subscribes/{subscribe_id}" in paths
    assert "put" in paths["/VIID/Subscribes/{subscribe_id}"]

    assert "/VIID/SubscribeNotifications/{notification_id}" in paths
    assert "get" in paths["/VIID/SubscribeNotifications/{notification_id}"]

    assert "/VIID/System/Time" in paths
    assert "get" in paths["/VIID/System/Time"]
