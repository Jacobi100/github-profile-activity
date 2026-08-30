class GitHubActivityError(Exception):
    """Base class for expected GitHub activity errors."""


class UserNotFoundError(GitHubActivityError):
    pass


class RateLimitError(GitHubActivityError):
    pass


class GitHubAPIError(GitHubActivityError):
    pass


class NetworkError(GitHubActivityError):
    pass


class InvalidResponseError(GitHubActivityError):
    pass
