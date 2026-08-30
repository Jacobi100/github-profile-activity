def event_format(event):
    event_type = event.get('type','UnknownEvent')
    repository = event.get('repo',{}).get('name','unknown repository')

    if event_type == 'PushEvent' :
        commits = event.get("payload",{}).get('commits',[])
        return f"Pushed {len(commits)} commits to {repository}"

    return f"Activity occured in {repository}: {event_type}"

    if event_type == "IssuesEvent":
        action = event.get("payload", {}).get("action", "updated")
    return f"{action.capitalize()} an issue in {repository}"

    if event_type == "WatchEvent":
        return f"Starred {repository}"

    if event_type == "ForkEvent":
        return f"Forked {repository}"

    if event_type == "CreateEvent":
        ref_type = event.get("payload", {}).get("ref_type", "resource")
    return f"Created a {ref_type} in {repository}"    