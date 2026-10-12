"""UTC clock used by rules and tests.

`utcnow` always calls `_system_utc`, so tests can replace `_system_utc`
without patching every import site.
"""

from datetime import datetime, timezone


def _system_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None)


def utcnow() -> datetime:
    return _system_utc()
