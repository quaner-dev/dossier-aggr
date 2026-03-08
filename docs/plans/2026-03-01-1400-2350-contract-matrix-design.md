# 1400 + 2350 Protocol-First Design (Current-State Matrix)

## Goal

Build this project strictly from protocol contracts first, with implementation and tests traced to each protocol clause.

- 1400 baseline source: `.protocol/1400/*`
- 2350 baseline source: `.protocol/2350/附件4-《公安视频图像分析技术要求 第5部分：目标聚档服务》（报批稿）0606 - 修订.docx`
- Contract precedence: `.protocol` > `.docs` > current code behavior

## Current Architecture Baseline

- Entry: `main.py`
- Layers: `api/` -> `services/` -> `tasks/` -> `models/` -> DB
- Async write pattern: many 1400 writes use `task.kiq(...)`
- DB runtime target: PostgreSQL (deployment)
- DB test target: SQLite (local/CI)

## Interface Matrix (1400)

| Clause | Path | Method | Current State | Notes |
| --- | --- | --- | --- | --- |
| 7.2.1 Register | `/VIID/System/Register` | POST | Implemented | Digest auth applied |
| 7.2.2 UnRegister | `/VIID/System/UnRegister` | POST | Implemented | Uses APS update |
| 7.2.3 Keepalive | `/VIID/System/Keepalive` | POST | Implemented | Uses APS update |
| 7.2.5 APE Query | `/VIID/APEs` | GET | Implemented | list path exists |
| 7.2.5 APE Update | `/VIID/APEs` | PUT | Implemented | async write via taskiq |
| 7.2.6 APS Query | `/VIID/APSs` | GET | Implemented | list path exists |
| 7.2.11.1 Person Query | `/VIID/Persons` | GET | Implemented (partial) | TODO: protocol query conditions not complete |
| 7.2.11.1 Person Create | `/VIID/Persons` | POST | Implemented | async write via taskiq |
| 7.2.11.1 Person Update | `/VIID/Persons` | PUT | Implemented | async write via taskiq |
| 7.2.11.1 Person Delete | `/VIID/Persons` | DELETE | Implemented (risk) | task-side delete implementation needs correction |
| 7.2.11.2 Person Query by ID | `/VIID/Persons/{person_id}` | GET | Implemented | single object response |
| 7.2.12.1 Face Query | `/VIID/Faces` | GET | Implemented (partial) | TODO: full key-value query missing |
| 7.2.12.1 Face Create | `/VIID/Faces` | POST | Implemented | async write via taskiq |
| 7.2.12.1 Face Update | `/VIID/Faces` | PUT | Implemented | async write via taskiq |
| 7.2.12.1 Face Delete | `/VIID/Faces` | DELETE | Implemented (risk) | service signature/task payload mismatch risk |
| 7.2.20.1 Subscribe Create | `/VIID/Subscribes` | POST | Implemented | async write via taskiq |
| 7.2.20.2 Subscribe Query | `/VIID/Subscribes` | GET | Implemented | list path exists |
| 7.2.20.2 Subscribe Update | `/VIID/Subscribes` | PUT | Implemented | async write via taskiq |
| 7.2.20.2 Subscribe Delete | `/VIID/Subscribes` | DELETE | Implemented | async write via taskiq |
| 7.2.21.1 Notification | `/VIID/SubscribeNotifications` | POST | Implemented | async write via taskiq |

## Interface Matrix (2350)

### URLs confirmed from original attachment

- `/VIID/ArchiveLibraries`
- `/VIAS/Tasks`
- `/VIID/Subscribes`
- `/VIID/SubscribeNotifications`
- `/VIID/Archives`
- `/VIID/ArchivesQuerySync`
- `/VIID/ArchiveSubjects`
- `/VIID/ArchiveSubjectQuerySync`
- `/VIID/VehicleArchives`
- `/VIID/VehicleArchivesQuerySync`
- `/VIID/VehicleArchiveSubjects`
- `/VIID/VehicleArchiveSubjectQuerySync`
- `/VIID/ArchiveConfidence`
- `/VIID/VehicleArchiveConfidence`

### Clause-level status

| Clause | URL | Current State | Gap Type |
| --- | --- | --- | --- |
| A.5 ArchiveLibrary CRUD | `/VIID/ArchiveLibraries` (+ query sync resource) | Route skeleton exists | API/Service/Task logic missing |
| A.6 Task CRUD | `/VIAS/Tasks` | Missing | constants/api/models/services/tasks all missing |
| A.7 Archive+Track Subscribe | `/VIID/Subscribes` | Reused from 1400 | 2350 extra fields/enum constraints not aligned |
| A.8 Archive+Track Notification | `/VIID/SubscribeNotifications` | Reused from 1400 | 2350 extra object lists not aligned |
| A.9 Archive Query | `/VIID/ArchivesQuerySync` | Route skeleton exists | request/response logic missing |
| A.10 Archive CRUD | `/VIID/Archives` | Route skeleton exists | API/Service/Task logic missing |
| A.11 VehicleArchive Query | `/VIID/VehicleArchivesQuerySync` | Missing | vehicle query stack missing |
| A.12 VehicleArchive CRUD | `/VIID/VehicleArchives` | Missing | vehicle model + stack missing |
| A.13 ArchiveSubject Query | `/VIID/ArchiveSubjectQuerySync` | Route skeleton exists | query logic missing |
| A.14 ArchiveSubject CRUD | `/VIID/ArchiveSubjects` | Route skeleton exists | API/Service/Task logic missing |
| A.15 VehicleArchiveSubject Query | `/VIID/VehicleArchiveSubjectQuerySync` | Missing | vehicle subject stack missing |
| A.16 VehicleArchiveSubject CRUD | `/VIID/VehicleArchiveSubjects` | Missing | vehicle subject stack missing |
| A.17 Archive Confidence | `/VIID/ArchiveConfidence` | Missing | verify stack missing |
| A.18 VehicleArchive Confidence | `/VIID/VehicleArchiveConfidence` | Missing | verify stack missing |

## Object/Model Coverage Matrix (2350 Appendix B)

| Object | Current State | Gap |
| --- | --- | --- |
| B.2 ArchiveLibrary | Present | Service/Task usage missing |
| B.3 Archive | Present | Query/CRUD behavior missing |
| B.4 VehicleArchive | Missing | model + table + migration missing |
| B.5 ArchiveSubject | Present (protocol object) | persistence/logic missing |
| B.6 ArchiveQuery | Present | behavior mapping missing |
| B.7 PictureQueryCondition | Present | behavior mapping missing |
| B.8 ArchiveQueryResult | Present | behavior mapping missing |
| B.9 ArchiveSubjectQuery | Present | behavior mapping missing |
| B.10 ArchiveSubjectQueryResult | Present | behavior mapping missing |
| B.11 SubscribeNotification | Partially reused from 1400 | 2350 extra lists missing/alignment required |
| B.12 GeoRectangle | Present | behavior mapping missing |
| B.13 DeviceSelector | Present | behavior mapping missing |
| B.14 Fields | Present | behavior mapping missing |
| B.15 FeatureInfo | Present | behavior mapping missing |
| B.16 Gait | Missing | model missing |

## Design Recommendation

Use a phased protocol-first delivery with strict closure per clause:

1. Phase 1 (stabilize existing 1400 + 2350 skeleton)
- Fix existing 1400 high-risk behavior mismatches.
- Implement A.5/A.9/A.10/A.13/A.14 end-to-end first.
- Keep response wrappers/time format aligned with protocol.

2. Phase 2 (complete missing 2350 feature set)
- Add A.6/A.11/A.12/A.15/A.16/A.17/A.18.
- Add missing B.4/B.16 models and migrations.

3. Phase 3 (contract verification hardening)
- Add protocol conformance tests per clause.
- Validate both PostgreSQL runtime and SQLite test environment.

## Acceptance Gates

- Every clause in A.* is linked to concrete endpoint tests.
- Every B.* object used by endpoints has model validation tests.
- `pytest -q` passes.
- `alembic upgrade head` succeeds.
- `.docs/ARCHITECTURE.md`, `.docs/PROTOCOL_1400.md`, `.docs/PROTOCOL_2350.md`, `.docs/TESTING.md` synchronized when contract behavior changes.
