import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from errors import (
    GitHubAPIError,
    InvalidResponseError,
    NetworkError,
    RateLimitError,
    UserNotFoundError,
)

API_URL = "https://api.github.com/users/{username}/events"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "github-user-activity-cli",
}


def fetch_events(username):
    request = Request(API_URL.format(username=username), headers=HEADERS)

    try:
        with urlopen(request, timeout=10) as response:
            data = response.read()
    except HTTPError as exc:
        if exc.code == 404:
            raise UserNotFoundError(f"GitHub user '{username}' was not found.") from exc
        if exc.code == 403:
            raise RateLimitError("GitHub API rate limit exceeded or access was forbidden.") from exc
        if 500 <= exc.code < 600:
            raise GitHubAPIError(f"GitHub service error (HTTP {exc.code}).") from exc
        raise GitHubAPIError(f"GitHub API request failed (HTTP {exc.code}).") from exc
    except URLError as exc:
        raise NetworkError("Could not connect to GitHub.") from exc

    try:
        events = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidResponseError("GitHub returned invalid JSON.") from exc

    if not isinstance(events, list):
        raise InvalidResponseError("GitHub returned an unexpected response format.")

    return events
