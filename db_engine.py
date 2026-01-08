import duckdb

DB_FILE = "hacknox.db"

def get_db():
    return duckdb.connect(DB_FILE)


def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS meeting_intelligence (
        version INTEGER,
        name TEXT,
        involvement_score INTEGER,
        time_spoken_seconds INTEGER,
        lines_spoken INTEGER,
        behavior_type TEXT,
        important_topics TEXT,
        summary TEXT,
        overall_meeting_summary TEXT,
        meeting_topics TEXT,
        generated_at TIMESTAMP
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS git_intelligence (
        version INTEGER,
        name TEXT,
        work_importance DOUBLE,
        pr_involvement DOUBLE,
        comment_quality DOUBLE,
        activity DOUBLE,
        collaboration_health DOUBLE,
        git_score DOUBLE,
        git_behavior TEXT,
        generated_at TIMESTAMP
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS final_team_intelligence (
        version INTEGER,
        name TEXT,
        merged_score DOUBLE,
        final_behavior TEXT,
        git_score DOUBLE,
        meeting_score DOUBLE,
        generated_at TIMESTAMP
    )
    """)

    db.close()


def get_next_version(table_name):
    db = get_db()
    v = db.execute(f"SELECT COALESCE(MAX(version), 0) + 1 FROM {table_name}").fetchone()[0]
    db.close()
    return v
