import sys 
if len(sys.argv) != 2 :
    print("Usage: python3 github_activity.py <username>")
    sys.exit(1)

username = sys.argv[1]
print(f"Fetching github ativity for {username}")

import urllib.request 

url = f"https://api.github.com/users/{username}/events"
request = urllib.request.Request(
    url , 
    headers = {
        "Accept" : "application/vnd.github+json",
        "X-Github-Api-Version" : "2022-11-28" , #GithubAPIVERSION
        "User-Agent" : "github-user-activity-cli",
    }
)

with urllib.request.urlopen(request) as response :
    data = response.read()

print(data) 
