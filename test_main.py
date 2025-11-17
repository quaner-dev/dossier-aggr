from fastapi import FastAPI
from fastapi.testclient import TestClient
from contants import *
from typing import Dict, Any

app = FastAPI()
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
