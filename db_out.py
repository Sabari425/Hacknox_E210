import duckdb

db = duckdb.connect("hacknox.db")

print(db.execute("""
SELECT version, name, git_score, git_behavior
FROM git_intelligence
ORDER BY version DESC, git_score DESC
""").fetchall())
