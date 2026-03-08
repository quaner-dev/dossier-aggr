from pathlib import Path


def test_protocol_2350_doc_covers_all_interface_clauses():
    content = Path(".docs/PROTOCOL_2350.md").read_text(encoding="utf-8")

    for clause in (
        "A.5",
        "A.6",
        "A.7",
        "A.8",
        "A.9",
        "A.10",
        "A.11",
        "A.12",
        "A.13",
        "A.14",
        "A.15",
        "A.16",
        "A.17",
        "A.18",
    ):
        assert clause in content


def test_protocol_2350_doc_covers_all_attachment_urls():
    content = Path(".docs/PROTOCOL_2350.md").read_text(encoding="utf-8")

    for url in (
        "/VIID/ArchiveLibraries",
        "/VIAS/Tasks",
        "/VIID/Subscribes",
        "/VIID/SubscribeNotifications",
        "/VIID/Archives",
        "/VIID/ArchivesQuerySync",
        "/VIID/ArchiveSubjects",
        "/VIID/ArchiveSubjectQuerySync",
        "/VIID/VehicleArchives",
        "/VIID/VehicleArchivesQuerySync",
        "/VIID/VehicleArchiveSubjects",
        "/VIID/VehicleArchiveSubjectQuerySync",
        "/VIID/ArchiveConfidence",
        "/VIID/VehicleArchiveConfidence",
    ):
        assert url in content
