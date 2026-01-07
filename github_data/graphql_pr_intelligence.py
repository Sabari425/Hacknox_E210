import requests
import json

TOKEN = ""
API_URL = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

query = """
{
  repository(owner: "fastapi", name: "fastapi") {
    pullRequests(first: 40, states: MERGED, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        title
        createdAt
        mergedAt
        author {
          login
        }
        reviews(first: 20) {
          nodes {
            state
            createdAt
            author {
              login
            }
          }
        }
        commits(last: 1) {
          nodes {
            commit {
              additions
              deletions
              changedFiles
            }
          }
        }
      }
    }
  }
}
"""

response = requests.post(API_URL, json={"query": query}, headers=headers)
data = response.json()

with open("graphql_pr_intelligence.json", "w") as f:
    json.dump(data, f, indent=2)

print("DONE ✅ graphql_pr_intelligence.json created")
