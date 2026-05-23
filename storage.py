import sqlite3
import json
import os
from datetime import datetime, timezone
from config import DATA_DIR

DB_PATH = os.path.join(DATA_DIR, "jobs.db")


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT DEFAULT '',
            link TEXT NOT NULL UNIQUE,
            posted TEXT,
            description TEXT DEFAULT '',
            source TEXT DEFAULT '',
            score REAL DEFAULT 0.0,
            matched_skills TEXT DEFAULT '',
            seen_count INTEGER DEFAULT 1,
            first_seen TEXT,
            last_seen TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_link ON jobs(link)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_score ON jobs(score DESC)
    """)
    conn.commit()
    conn.close()


def save_jobs(jobs):
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now(timezone.utc).isoformat()
    count_new = 0
    count_updated = 0
    for j in jobs:
        try:
            conn.execute("""
                INSERT INTO jobs (title, company, link, posted, description, source, score, matched_skills, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(link) DO UPDATE SET
                    seen_count = seen_count + 1,
                    last_seen = excluded.last_seen,
                    score = excluded.score,
                    matched_skills = excluded.matched_skills
            """, (
                j.get("title", ""),
                j.get("company", ""),
                j.get("link", ""),
                j.get("posted", now),
                j.get("description", ""),
                j.get("source", ""),
                j.get("score", 0.0),
                j.get("matched_skills", ""),
                now,
                now,
            ))
            if conn.total_changes > 0:
                count_new += 1
        except Exception:
            count_updated += 1
    conn.commit()
    conn.close()
    return count_new


def get_saved_jobs(min_score=0, limit=200):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT title, company, link, posted, description, source, score, matched_skills
        FROM jobs
        WHERE score >= ?
        ORDER BY score DESC, last_seen DESC
        LIMIT ?
    """, (min_score, limit)).fetchall()
    conn.close()
    jobs = []
    for r in rows:
        jobs.append({
            "company": r[1],
            "title": r[0],
            "link": r[2],
            "posted": r[3] or datetime.now(timezone.utc).isoformat(),
            "description": r[4],
            "source": r[5],
            "score": r[6],
            "matched_skills": r[7],
        })
    return jobs


def get_stats():
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    scored = conn.execute("SELECT COUNT(*) FROM jobs WHERE score > 0").fetchone()[0]
    avg_score = conn.execute("SELECT AVG(score) FROM jobs WHERE score > 0").fetchone()[0]
    last_7 = conn.execute(
        "SELECT COUNT(*) FROM jobs WHERE last_seen >= datetime('now', '-7 days')"
    ).fetchone()[0]
    conn.close()
    return {"total": total, "scored": scored, "avg_score": round(avg_score or 0, 1), "last_7_days": last_7}
