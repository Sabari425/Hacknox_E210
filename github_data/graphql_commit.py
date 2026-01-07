import requests, json

TOKEN = ""
API_URL = "https://api.github.com/graphql"

headers = {"Authorization": f"Bearer {TOKEN}"}

query = """
{
  repository(owner: "fastapi", name: "fastapi") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 40) {
            nodes {
              committedDate
              author {
                user {
                  login
                }
              }
              additions
              deletions
              changedFiles
              messageHeadline
            }
          }
        }
      }
    }
  }
}
"""

r = requests.post(API_URL, json={"query": query}, headers=headers)

with open("graphql_commit_intelligence.json", "w") as f:
    json.dump(r.json(), f, indent=2)

print("DONE ✅ graphql_commit_intelligence.json created")
