"""Tests for tznow CLI."""

import pytest
import zoneinfo
from datetime import datetime
from tznow import __version__
from tznow.cli import (
    DEFAULT_ZONES,
    ALIASES,
    format_time,
    resolve_timezone,
    get_times,
    main,
)


class TestVersion:
    def test_version_exists(self):
        assert __version__ == "0.1.0"


class TestFormatTime:
    def test_format_time_basic(self):
        dt = datetime(2026, 10, 5, 14, 30, 45, tzinfo=zoneinfo.ZoneInfo("UTC"))
        result = format_time(dt, "UTC")
        assert "14:30:45" in result
        assert "2026-10-05" in result
        assert "UTC" in result

    def test_format_time_with_width(self):
        dt = datetime(2026, 10, 5, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo("America/New_York"))
        result = format_time(dt, "NY", width=40)
        assert "09:15:30" in result
        assert "2026-10-05" in result


class TestResolveTimezone:
    def test_resolve_utc(self):
        tz = resolve_timezone("UTC")
        assert tz.key == "UTC"

    def test_resolve_alias_ny(self):
        tz = resolve_timezone("ny")
        assert tz.key == "America/New_York"

    def test_resolve_alias_nyc(self):
        tz = resolve_timezone("nyc")
        assert tz.key == "America/New_York"

    def test_resolve_alias_tokyo(self):
        tz = resolve_timezone("tokyo")
        assert tz.key == "Asia/Tokyo"

    def test_resolve_full_name(self):
        tz = resolve_timezone("Europe/London")
        assert tz.key == "Europe/London"

    def test_resolve_case_insensitive(self):
        tz = resolve_timezone("UTC")
        assert tz.key == "UTC"
        tz2 = resolve_timezone("utc")
        assert tz2.key == "UTC"

    def test_resolve_with_whitespace(self):
        tz = resolve_timezone("  utc  ")
        assert tz.key == "UTC"


class TestGetTimes:
    def test_get_times_defaults(self):
        now = datetime.now(zoneinfo.ZoneInfo("UTC"))
        results = get_times(now=now)
        assert len(results) == len(DEFAULT_ZONES)
        for result in results:
            assert "ERROR" not in result

    def test_get_times_custom_zones(self):
        now = datetime(2026, 10, 5, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
        results = get_times(["UTC", "America/New_York"], now=now)
        assert len(results) == 2
        assert "12:00:00" in results[0]  # UTC
        assert "08:00:00" in results[1]  # NY is UTC-4 in October

    def test_get_times_with_aliases(self):
        now = datetime(2026, 10, 5, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
        results = get_times(["ny", "tokyo"], now=now)
        assert len(results) == 2
        assert "08:00:00" in results[0]  # NY
        assert "21:00:00" in results[1]  # Tokyo is UTC+9

    def test_get_times_invalid_timezone(self):
        results = get_times(["Invalid/Timezone"])
        assert len(results) == 1
        assert "ERROR" in results[0]

    def test_get_times_mixed_valid_invalid(self):
        now = datetime(2026, 10, 5, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
        results = get_times(["UTC", "Invalid/TZ", "America/New_York"], now=now)
        assert len(results) == 3
        assert "12:00:00" in results[0]
        assert "ERROR" in results[1]
        assert "08:00:00" in results[2]


class TestMain:
    def test_main_no_args(self, capsys):
        exit_code = main([])
        assert exit_code == 0
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == len(DEFAULT_ZONES)

    def test_main_with_args(self, capsys):
        exit_code = main(["UTC", "ny"])
        assert exit_code == 0
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2

    def test_main_default_argv(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.argv", ["tznow"])
        exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == len(DEFAULT_ZONES)

    def test_main_with_sys_argv(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.argv", ["tznow", "UTC", "tokyo"])
        exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2


class TestAliases:
    def test_aliases_exist(self):
        assert "utc" in ALIASES
        assert "ny" in ALIASES
        assert "tokyo" in ALIASES

    def test_aliases_map_correctly(self):
        assert ALIASES["ny"] == "America/New_York"
        assert ALIASES["tokyo"] == "Asia/Tokyo"


class TestDefaultZones:
    def test_default_zones_not_empty(self):
        assert len(DEFAULT_ZONES) > 0

    def test_default_zones_valid(self):
        for tz_name in DEFAULT_ZONES:
            tz = zoneinfo.ZoneInfo(tz_name)
            assert tz is not None
