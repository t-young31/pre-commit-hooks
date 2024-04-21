from datetime import date, timedelta

from tyhooks.tf_deps import File

now = date.today()


def test_file_has_unchecked_versions() -> None:
    content = """
resource "null_resource" "test" {
  version = "1.0"
}
"""
    assert all(not r.version_checked_after(now) for r in File(content).resources)


def test_file_has_checked_version_old_is_not_ok() -> None:
    content = """
resource "null_resource" "test" {
  version = "1.0"  # checked 1970-01-01
}
"""
    assert all(not r.version_checked_after(now) for r in File(content).resources)


def test_file_has_no_versions_is_ok() -> None:
    content = """
resource "null_resource" "test1" {
  name = "test1"
}

resource "null_resource" "test2" {
  name = "test2"
}
"""
    resources = File(content).resources
    assert len(resources) == 2
    assert all(r.version_checked_after(now) for r in resources)


def test_file_has_checked_version_today_is_ok() -> None:
    content = (
        'resource "null_resource" "test" {'
        f'  version = "1.0"  # checked {now.year}-{now.month}-{now.day}'
        "}"
    )
    assert all(
        r.version_checked_after(now - timedelta(days=1))
        for r in File(content).resources
    )
