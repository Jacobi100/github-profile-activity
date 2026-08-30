# GitHub User Activity CLI

A small Python command-line app that accepts a GitHub username, calls the GitHub Events API, and prints readable recent activity.

## Project goal

This project shows how to:

- accept a username from the command line
- request data from the GitHub REST API
- parse JSON responses
- format event data into readable messages
- handle expected API and network errors cleanly

No third-party libraries are used. It relies only on Python’s standard library.

## Project files

- `main.py` – CLI entry point
- `api.py` – GitHub API request and response handling
- `errors.py` – custom exceptions for expected failures
- `README.md` – usage and project documentation

## Requirements

- Python 3
- Internet access to reach GitHub’s public API

## Setup

From the project folder:

```bash
cd github-user-activity
```

## Run the app

```bash
python3 main.py {username}
```

Or with any public GitHub username:

```bash
python3 main.py kamranahmedse
```

## Usage

```bash
python3 main.py <username>
```

If the username is missing, the app prints:

```text
Usage: python3 github_activity.py <username>
```

## Example output

```text
- Pushed 3 commits to kamranahmedse/developer-roadmap
- Opened an issue in kamranahmedse/developer-roadmap
- Starred kamranahmedse/developer-roadmap
- Created a repository in kamranahmedse
```

For unknown event types, the app falls back to a safe message:

```text
- Activity occurred in owner/repository: ReleaseEvent
```

## Supported events

The formatter handles common GitHub event types, including:

- `PushEvent`
- `IssuesEvent`
- `IssueCommentEvent`
- `WatchEvent`
- `ForkEvent`
- `CreateEvent`
- `PullRequestEvent`
- `DeleteEvent`

Unknown event types are displayed without crashing the program.

## Error handling

The app catches and prints friendly messages for expected problems:

```text
Error: GitHub user 'does-not-exist' was not found.
Error: Could not connect to GitHub.
Error: GitHub API rate limit exceeded or access was forbidden.
Error: GitHub service error (HTTP 500).
No recent public activity found for octocat.
```

## API details

The app requests:

```text
https://api.github.com/users/<username>/events
```

with recommended headers such as:

```python
{
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "github-user-activity-cli",
}
```

## Verification project

Project URL for verification:

https://roadmap.sh/projects/github-user-activity

## Testing

To run the project tests later, use:

```bash
python3 -m unittest discover -s tests -v
```

## Notes

This project is intentionally built with only Python’s standard library, which keeps it easy to understand and useful for learning API basics, JSON parsing, formatting, and error handling.
