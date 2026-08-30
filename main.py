import sys

from api import fetch_events
from errors import GitHubActivityError


def event_format(event):
    event_type = event.get('type', 'UnknownEvent')
    repository = event.get('repo', {}).get('name', 'unknown repository')

    if event_type == 'PushEvent':
        commits = event.get('payload', {}).get('commits', [])
        return f"Pushed {len(commits)} commits to {repository}"

    if event_type == 'IssuesEvent':
        action = event.get('payload', {}).get('action', 'updated')
        return f"{action.capitalize()} an issue in {repository}"

    if event_type == 'WatchEvent':
        return f"Starred {repository}"

    if event_type == 'ForkEvent':
        return f"Forked {repository}"

    if event_type == 'CreateEvent':
        ref_type = event.get('payload', {}).get('ref_type', 'resource')
        return f"Created a {ref_type} in {repository}"

    return f"Activity occurred in {repository}: {event_type}"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 github_activity.py <username>")
        return 1

    username = sys.argv[1]

    try:
        events = fetch_events(username)
    except GitHubActivityError as exc:
        print(f"Error: {exc}")
        return 1

    if not events:
        print(f"No recent public activity found for {username}.")
        return 0

    for event in events:
        print(f"- {event_format(event)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
