import requests, json

TOKEN = ""
API_URL = "https://api.github.com/graphql"

headers = {"Authorization": f"Bearer {TOKEN}"}

query = """
{
  repository(owner: "fastapi", name: "fastapi") {
    pullRequests(first: 30, states: MERGED, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        author {
          login
        }
        reviews(first: 20) {
          nodes {
            state
            author {
              login
            }
          }
        }
      }
    }
  }
}
"""

r = requests.post(API_URL, json={"query": query}, headers=headers)

with open("graphql_review_network.json", "w") as f:
    json.dump(r.json(), f, indent=2)

print("DONE ✅ graphql_review_network.json created")
