# Baseline Test Cases

## 健康检查

```bash
curl -s http://127.0.0.1:8000/startup
curl -s http://127.0.0.1:8000/live
curl -s http://127.0.0.1:8000/ready
```

## Register Digest

```bash
curl --digest -u tester:admin \
  -H 'Content-Type: application/json' \
  -X POST http://127.0.0.1:8000/VIID/System/Register \
  -d '{"RegisterObject":{"DeviceID":"APS-001"}}'
```

## APE 批量更新 + 查询回读

```bash
curl -H 'Content-Type: application/json' \
  -X PUT http://127.0.0.1:8000/VIID/APEs \
  -d '{"APEListObject":{"APEObject":[{"ApeID":"APE-001","Name":"Cam-1","Model":"M1","IPAddr":"192.168.1.10","IPV6Addr":null,"Port":8001,"Longitude":116.39,"Latitude":39.90,"PlaceCode":"110000","Place":"BJ","OrgCode":"110101","CapDirection":0,"MonitorDirection":1,"MonitorAreaDesc":"Gate","IsOnline":1,"OwnerApsID":"APS-001","UserId":"admin","Password":"pass","FunctionType":"Capture","PositionType":"Fixed"}]}}'

curl -s http://127.0.0.1:8000/VIID/APEs
```

## Subscribe 重复创建负向用例

- 首次创建应成功。
- 使用同一 `SubscribeID` 再次创建，应返回已存在语义。

## 异步最终一致性

- 对 `.kiq` 写路径，断言接口返回与任务执行结果一致。
- 对 InMemoryBroker 场景，保留轮询加超时验证最终可见性的 e2e 用例。
- 当前基线至少覆盖 `ArchiveSubject`。
