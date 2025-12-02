from fastapi.testclient import TestClient
from contants import *
from typing import Dict, Any
from main import app

client = TestClient(app)


def test_subscribe():
    payload: Dict[str, Any] = {
        "SubscribeListObject": {
            "SubscribeObject": [
                {
                    "SubscribeID": "510116000000032024022816194212625",
                    "Title": "人脸抓拍数据",
                    "SubscribeDetail": "12",
                    "ResourceURI": "51011657225035559375",
                    "ApplicantName": "sysadmin",
                    "ApplicantOrg": "1a4b9f60",
                    "BeginTime": "20240228161912",
                    "EndTime": "20990228161912",
                    "ReceiveAddr": "http://10.184.48.208:14606/VIID/SubscribeNotifications",
                    "ReportInterval": 3,
                    "Reason": "人脸数据",
                    "OperateType": 0,
                    "SubscribeStatus": 0,
                    "ResourceClass": 4,
                    "ResultImageDeclare": "14",
                    "ResultFeatureDeclare": -1,
                    "TabID": "51011638925031798819992024022816194236203",
                }
            ]
        }
    }
    response = client.post(url=subscribe_url, json=payload)
    assert response.status_code == 200


def test_digest_auth_first_request_returns_401():
    """测试第一次请求没有Authorization头返回401"""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
    assert "Digest" in response.headers["WWW-Authenticate"]


def test_digest_auth_second_request_returns_200():
    """测试第二次请求带Authorization头返回200"""
    # 带任意Digest Authorization头即可通过
    response = client.get(
        "/users/me",
        headers={"Authorization": "Digest username=\"test\", realm=\"VIID API\", nonce=\"abc123\""}
    )
    assert response.status_code == 200
    assert "scheme" in response.json()
    assert response.json()["scheme"] == "Digest"
