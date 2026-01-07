import requests, json

TOKEN = ""
API_URL = "https://api.github.com/graphql"

headers = {"Authorization": f"Bearer {TOKEN}"}

query = """
{
  repository(owner: "fastapi", name: "fastapi") {
    issues(first: 40, states: CLOSED, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        title
        createdAt
        closedAt
        author {
          login
        }
        assignees(first: 5) {
          nodes {
            login
          }
        }
        comments {
          totalCount
        }
      }
    }
  }
}
"""

r = requests.post(API_URL, json={"query": query}, headers=headers)

with open("graphql_issue_intelligence.json", "w") as f:
    json.dump(r.json(), f, indent=2)

print("DONE ✅ graphql_issue_intelligence.json created")
