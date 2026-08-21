import argparse
import json
import sys
from urllib import error, request


def fetch_events(username: str) -> list[dict]:
    url = f"https://api.github.com/users/{username}/events"
    req = request.Request(url, headers={"User-Agent": "github-user-activity-cli"})
    with request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def format_event(event: dict) -> str | None:
    event_type = event.get("type")
    repo_name = event.get("repo", {}).get("name", "unknown repository")

    if event_type == "PushEvent":
        commits = len(event.get("payload", {}).get("commits", []))
        return f"- Pushed {commits} commit{'s' if commits != 1 else ''} to {repo_name}"
    if event_type == "IssuesEvent":
        action = event.get("payload", {}).get("action", "updated")
        if action == "opened":
            return f"- Opened a new issue in {repo_name}"
        return f"- {action.capitalize()} an issue in {repo_name}"
    if event_type == "WatchEvent":
        return f"- Starred {repo_name}"
    if event_type == "PullRequestEvent":
        action = event.get("payload", {}).get("action", "updated")
        if action == "opened":
            return f"- Opened a pull request in {repo_name}"
        return f"- {action.capitalize()} a pull request in {repo_name}"
    return f"- {event_type} in {repo_name}" if event_type else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="github-activity")
    parser.add_argument("username", help="GitHub username")
    args = parser.parse_args(argv)

    try:
        events = fetch_events(args.username)
    except error.HTTPError as exc:
        if exc.code == 404:
            print(f"User '{args.username}' not found.", file=sys.stderr)
        elif exc.code == 403:
            print(
                "GitHub API request was forbidden or rate-limited (HTTP 403).",
                file=sys.stderr,
            )
        else:
            print(f"GitHub API request failed with status {exc.code}.", file=sys.stderr)
        return 1
    except error.URLError:
        print("Network error while fetching activity.", file=sys.stderr)
        return 1

    if not events:
        print("No recent activity found.")
        return 0

    for event in events:
        line = format_event(event)
        if line:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
