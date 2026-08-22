import sys 

if len(sys.argv) != 2 :
    print("Usage: python3 github_activity.py <username>")
    sys.exit(1)

username = sys.argv[1]
print(f"Fetcching github ativity for {username}")