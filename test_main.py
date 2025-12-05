from fastapi.testclient import TestClient
from typing import Dict, Any
from datetime import datetime

from contants import *
from main import app

# 创建测试客户端
client = TestClient(app)


def test_register_with_auth():
    """测试注册接口（需要认证）"""
    # 第一次请求应该返回401，要求认证
    response = client.post(REGISTER_URL)
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
    assert "Digest" in response.headers["WWW-Authenticate"]

    # 第二次请求带认证头应该成功
    response = client.post(
        REGISTER_URL,
        headers={
            "Authorization": 'Digest username="test", realm="VIID API", nonce="abc123"'
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["RequestURL"] == REGISTER_URL
    assert data["StatusCode"] == "0"
    assert data["StatusString"] == "注册成功"
    assert "LocalTime" in data


def test_register_without_auth():
    """测试注册接口（无认证头）"""
    response = client.post(REGISTER_URL)
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_unregister():
    """测试注销接口"""
    response = client.post(UNREGISTER_URL)
    assert response.status_code == 200
    data = response.json()
    assert data["RequestURL"] == UNREGISTER_URL
    assert data["StatusCode"] == "0"
    assert data["StatusString"] == "注销成功"
    assert "LocalTime" in data


def test_keepalive():
    """测试保活接口"""
    response = client.post(KEEPALIVE_URL)
    assert response.status_code == 200
    data = response.json()
    assert data["RequestURL"] == KEEPALIVE_URL
    assert data["StatusCode"] == "0"
    assert data["StatusString"] == "保活成功"
    assert "LocalTime" in data


def test_subscribe_success():
    """测试订阅接口成功情况"""
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
    response = client.post(url=SUBSCRIBES_URL, json=payload)
    assert response.status_code == 200


def test_subscribe_invalid_payload():
    """测试订阅接口无效负载"""
    # 测试缺少必填字段
    payload: Dict[str, Any] = {
        "SubscribeListObject": {
            "SubscribeObject": [
                {
                    "SubscribeID": "test123",
                    "Title": "测试订阅",
                    # 缺少其他必填字段
                }
            ]
        }
    }
    response = client.post(url=SUBSCRIBES_URL, json=payload)
    # FastAPI会自动验证并返回422错误
    assert response.status_code == 422


def test_subscribe_empty_list():
    """测试订阅接口空列表"""
    payload: Dict[str, Any] = {"SubscribeListObject": {"SubscribeObject": []}}
    response = client.post(url=SUBSCRIBES_URL, json=payload)
    assert response.status_code == 200


def test_subscribe_multiple_items():
    """测试订阅接口多个订阅项"""
    payload: Dict[str, Any] = {
        "SubscribeListObject": {
            "SubscribeObject": [
                {
                    "SubscribeID": "test001",
                    "Title": "订阅1",
                    "SubscribeDetail": "detail1",
                    "ResourceURI": "uri1",
                    "ApplicantName": "user1",
                    "ApplicantOrg": "org1",
                    "BeginTime": "20240101000000",
                    "EndTime": "20241231235959",
                    "ReceiveAddr": "http://example.com/notify1",
                    "ReportInterval": 5,
                    "Reason": "reason1",
                    "OperateType": 0,
                    "SubscribeStatus": 0,
                    "ResourceClass": 4,
                    "ResultImageDeclare": "14",
                    "ResultFeatureDeclare": -1,
                    "TabID": "tab001",
                },
                {
                    "SubscribeID": "test002",
                    "Title": "订阅2",
                    "SubscribeDetail": "detail2",
                    "ResourceURI": "uri2",
                    "ApplicantName": "user2",
                    "ApplicantOrg": "org2",
                    "BeginTime": "20240101000000",
                    "EndTime": "20241231235959",
                    "ReceiveAddr": "http://example.com/notify2",
                    "ReportInterval": 10,
                    "Reason": "reason2",
                    "OperateType": 1,
                    "SubscribeStatus": 1,
                    "ResourceClass": 4,
                    "ResultImageDeclare": "14",
                    "ResultFeatureDeclare": -1,
                    "TabID": "tab002",
                },
            ]
        }
    }
    response = client.post(url=SUBSCRIBES_URL, json=payload)
    assert response.status_code == 200


def test_apes_empty():
    """测试获取APE列表（空数据库）"""
    response = client.get(APES_URL)
    assert response.status_code == 200
    data = response.json()
    assert "APEListObject" in data
    assert "APEObject" in data["APEListObject"]
    # 注意：由于使用真实数据库，可能返回空数组


def test_subscribe_notifications():
    """测试订阅通知接口"""
    response = client.post(SUBSCRIBE_NOTIFICATIONS_URL)
    # 目前这个接口返回200，但实际功能未实现
    assert response.status_code == 200
    data = response.json()
    assert data["RequestURL"] == SUBSCRIBE_NOTIFICATIONS_URL
    assert data["StatusCode"] == "0"
    assert data["StatusString"] == "OK"


def test_invalid_endpoint():
    """测试无效端点"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


def test_health_check():
    """测试健康检查端点"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_subscribe_duplicate_id():
    """测试重复订阅ID"""
    payload: Dict[str, Any] = {
        "SubscribeListObject": {
            "SubscribeObject": [
                {
                    "SubscribeID": "DUPLICATE001",
                    "Title": "重复订阅测试",
                    "SubscribeDetail": "detail",
                    "ResourceURI": "uri",
                    "ApplicantName": "user",
                    "ApplicantOrg": "org",
                    "BeginTime": "20240101000000",
                    "EndTime": "20241231235959",
                    "ReceiveAddr": "http://example.com/notify",
                    "ReportInterval": 5,
                    "Reason": "test",
                    "OperateType": 0,
                    "SubscribeStatus": 0,
                    "ResourceClass": 4,
                    "ResultImageDeclare": "14",
                    "ResultFeatureDeclare": -1,
                    "TabID": "tab001",
                }
            ]
        }
    }

    # 第一次订阅
    response1 = client.post(url=SUBSCRIBES_URL, json=payload)
    assert response1.status_code == 200

    # 第二次相同ID的订阅
    response2 = client.post(url=SUBSCRIBES_URL, json=payload)
    assert response2.status_code == 200  # 目前代码允许重复ID


def test_subscribe_edge_cases():
    """测试订阅边界情况"""
    # 测试最小有效负载
    payload: Dict[str, Any] = {
        "SubscribeListObject": {
            "SubscribeObject": [
                {
                    "SubscribeID": "MINIMAL001",
                    "Title": "最小测试",
                    "SubscribeDetail": "d",
                    "ResourceURI": "u",
                    "ApplicantName": "u",
                    "ApplicantOrg": "o",
                    "BeginTime": "20240101000000",
                    "EndTime": "20240101000001",
                    "ReceiveAddr": "http://e.com",
                    "ReportInterval": 1,
                    "Reason": "r",
                    "OperateType": 0,
                    "SubscribeStatus": 0,
                    "ResourceClass": 4,
                    "ResultImageDeclare": "14",
                    "ResultFeatureDeclare": -1,
                    "TabID": "t",
                }
            ]
        }
    }
    response = client.post(url=SUBSCRIBES_URL, json=payload)
    assert response.status_code == 200


def test_response_time_format():
    """测试响应时间格式"""
    response = client.post(KEEPALIVE_URL)
    assert response.status_code == 200
    data = response.json()

    # 验证时间格式为YYYYMMDDHHMMSS
    local_time = data["LocalTime"]
    assert len(local_time) == 14
    # 尝试解析时间
    try:
        datetime.strptime(local_time, "%Y%m%d%H%M%S")
        assert True
    except ValueError:
        assert False, f"Invalid time format: {local_time}"


def test_all_endpoints_response_structure():
    """测试所有端点的响应结构一致性"""
    endpoints = [
        (REGISTER_URL, "POST", True),  # 需要认证
        (UNREGISTER_URL, "POST", False),
        (KEEPALIVE_URL, "POST", False),
        (SUBSCRIBE_NOTIFICATIONS_URL, "POST", False),
    ]

    for endpoint, method, needs_auth in endpoints:
        if method == "POST":
            if needs_auth:
                response = client.post(
                    endpoint,
                    headers={
                        "Authorization": 'Digest username="test", realm="VIID API", nonce="abc123"'
                    },
                )
            else:
                response = client.post(endpoint)

            assert response.status_code == 200
            data = response.json()

            # 验证通用响应结构
            assert "RequestURL" in data
            assert "StatusCode" in data
            assert "StatusString" in data
            assert "LocalTime" in data

            # 验证URL匹配
            assert data["RequestURL"] == endpoint


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
        headers={
            "Authorization": 'Digest username="test", realm="VIID API", nonce="abc123"'
        },
    )
    assert response.status_code == 200
    assert "scheme" in response.json()
    assert response.json()["scheme"] == "Digest"
