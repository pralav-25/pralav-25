import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from scripts.cards import fetch_contributions, main


def response(days):
    return {"data": {"user": {"contributionsCollection": {"contributionCalendar": {
        "totalContributions": sum(count for _, count in days),
        "weeks": [{"contributionDays": [
            {"date": date, "contributionCount": count} for date, count in days
        ]}],
    }}}}}


class ContributionTests(unittest.TestCase):
    def test_no_token_does_not_make_a_request(self):
        with patch("scripts.cards.graphql") as api:
            self.assertIsNone(fetch_contributions("example", None))
        api.assert_not_called()

    def test_calendar_boundaries(self):
        cases = [
            ([], (0, 0, 0)),
            ([("2026-09-11", 0), ("2026-09-12", 0)], (0, 0, 0)),
            ([("2026-09-10", 2), ("2026-09-11", 3), ("2026-09-12", 0)], (5, 2, 2)),
            ([("2026-09-09", 2), ("2026-09-10", 1), ("2026-09-11", 0), ("2026-09-12", 4)], (7, 1, 2)),
            ([("2026-12-31", 1), ("2027-01-01", 2)], (3, 2, 2)),
            ([("2026-09-12", 1), ("2026-09-11", 2)], (3, 2, 2)),
        ]
        for days, expected in cases:
            with self.subTest(days=days), patch("scripts.cards.graphql", return_value=response(days)):
                self.assertEqual(fetch_contributions("example", "test-token"), expected)

    def test_graphql_errors_leave_contribution_tiles_unavailable(self):
        with patch("scripts.cards.graphql", return_value={"errors": [{"message": "Unavailable"}]}):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertIsNone(fetch_contributions("example", "test-token"))

    def test_network_and_decode_errors_do_not_abort_card_generation(self):
        for error in [
            urllib.error.HTTPError("https://api.github.com/graphql", 503, "Unavailable", {}, None),
            urllib.error.URLError("Connection unavailable"),
            TimeoutError("Request timed out"),
            json.JSONDecodeError("Invalid response", "<html>", 0),
        ]:
            with self.subTest(error=type(error).__name__), patch("scripts.cards.graphql", side_effect=error):
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertIsNone(fetch_contributions("example", "test-token"))

    def test_missing_calendar_data_does_not_abort_card_generation(self):
        malformed_date = response([("not-a-date", 1)])
        malformed_count = response([("2026-09-12", -1)])
        for payload in [None, [], {}, {"data": None}, {"data": {"user": None}}, malformed_date, malformed_count]:
            with self.subTest(payload=payload), patch("scripts.cards.graphql", return_value=payload):
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertIsNone(fetch_contributions("example", "test-token"))

    def test_refresh_still_writes_stats_and_project_cards_when_graphql_is_down(self):
        repos = [{"name": "demo", "description": "A tested project", "language": "Python",
                  "fork": False, "stargazers_count": 3, "forks_count": 1}]
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            projects = output / "projects.json"
            projects.write_text(json.dumps({"projects": [{"repo": "demo"}]}))
            with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}), \
                 patch("scripts.cards.rest", side_effect=[{"public_repos": 1, "followers": 2}, repos]), \
                 patch("scripts.cards.graphql", side_effect=urllib.error.URLError("Offline")), \
                 contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                main(["--user", "example", "--out", folder, "--projects", str(projects)])
            for theme in ["dark", "light"]:
                stats = (output / f"card-stats-{theme}.svg").read_text()
                self.assertIn("Public repos", stats)
                self.assertNotIn("Contributions (1y)", stats)
                self.assertIn("A tested project", (output / f"card-demo-{theme}.svg").read_text())
