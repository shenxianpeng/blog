"""Tests for the last-commit badge data.

The point of the script is that the badges look exactly like shields' own
github/last-commit badge, so these pin its wording and colour at the edges:
dayjs calendar() day boundaries in UTC and the age() colour steps.
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gen_last_commit_badges import age_color, badge, format_date, packages

# A Sunday afternoon.
NOW = datetime(2026, 10, 18, 15, 0, tzinfo=timezone.utc)


def at(*args):
    return datetime(*args, tzinfo=timezone.utc)


class TestFormatDate:
    def test_today_starts_at_utc_midnight(self):
        assert format_date(at(2026, 10, 18, 0, 0), NOW) == "today"
        assert format_date(at(2026, 10, 17, 23, 59), NOW) == "yesterday"

    def test_yesterday_covers_the_whole_previous_day(self):
        assert format_date(at(2026, 10, 17, 0, 0), NOW) == "yesterday"
        assert format_date(at(2026, 10, 16, 23, 59), NOW) == "last friday"

    def test_last_weekday_reaches_back_six_days(self):
        assert format_date(at(2026, 10, 12, 0, 0), NOW) == "last monday"
        assert format_date(at(2026, 10, 11, 23, 59), NOW) == "october"

    def test_month_drops_only_the_current_year(self):
        assert format_date(at(2026, 1, 2), NOW) == "january"
        assert format_date(at(2025, 9, 3), NOW) == "september 2025"

    def test_commit_after_now_reads_today(self):
        assert format_date(NOW + timedelta(hours=1), NOW) == "today"


class TestAgeColor:
    def test_steps(self):
        cases = {6: "brightgreen", 7: "green", 29: "green", 30: "yellowgreen",
                 179: "yellowgreen", 180: "yellow", 364: "yellow", 365: "orange",
                 729: "orange", 730: "red"}
        for days, color in cases.items():
            assert age_color(NOW - timedelta(days=days), NOW) == color, days

    def test_partial_days_round_down(self):
        assert age_color(NOW - timedelta(days=6, hours=23), NOW) == "brightgreen"


def test_badge_is_a_shields_endpoint_document():
    assert badge(at(2026, 10, 18, 9), NOW) == {
        "schemaVersion": 1, "label": "last commit", "message": "today", "color": "brightgreen",
    }


def test_packages_reads_the_github_links_only():
    page = (
        "[commit-check]: https://pypi.org/project/commit-check/\n"
        "[gh-commit-check]: https://github.com/commit-check/commit-check\n"
        "[gh-mkdocs-ng]: https://github.com/mkdocs-ng/mkdocs\n"
        "[badge-name-gh-x]: https://img.shields.io/badge/x-blue\n"
    )
    assert packages(page) == {"commit-check": "commit-check/commit-check", "mkdocs-ng": "mkdocs-ng/mkdocs"}
