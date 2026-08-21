import contextlib
import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from github_activity import cli


class TestCli(unittest.TestCase):
    def test_formats_common_events(self):
        events = [
            {
                "type": "PushEvent",
                "repo": {"name": "owner/repo"},
                "payload": {"commits": [{}, {}, {}]},
            },
            {
                "type": "IssuesEvent",
                "repo": {"name": "owner/repo"},
                "payload": {"action": "opened"},
            },
            {"type": "WatchEvent", "repo": {"name": "owner/repo"}, "payload": {}},
        ]
        with patch("github_activity.cli.fetch_events", return_value=events):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = cli.main(["alice"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            output.getvalue().strip().splitlines(),
            [
                "- Pushed 3 commits to owner/repo",
                "- Opened a new issue in owner/repo",
                "- Starred owner/repo",
            ],
        )

    def test_handles_no_events(self):
        with patch("github_activity.cli.fetch_events", return_value=[]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = cli.main(["alice"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "No recent activity found.")

    def test_handles_http_403(self):
        err = HTTPError(url="", code=403, msg="Forbidden", hdrs=None, fp=None)
        with patch("github_activity.cli.fetch_events", side_effect=err):
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                exit_code = cli.main(["alice"])

        self.assertEqual(exit_code, 1)
        self.assertIn("HTTP 403", output.getvalue())


if __name__ == "__main__":
    unittest.main()
