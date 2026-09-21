import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "character.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                memory TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()


def add_user(user_id, display_name):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO users (id, display_name)
            VALUES (?, ?)
            """,
            (user_id, display_name)
        )
        conn.commit()


def add_memory(user_id, memory):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO memories (user_id, memory)
            VALUES (?, ?)
            """,
            (user_id, memory)
        )
        conn.commit()

def add_memory_if_new(user_id, memory):
    with get_connection() as conn:
        existing = conn.execute(
            """
            SELECT 1
            FROM memories
            WHERE user_id = ? AND memory = ?
            """,
            (user_id, memory)
        ).fetchone()

        if existing:
            return False

        conn.execute(
            """
            INSERT INTO memories (user_id, memory)
            VALUES (?, ?)
            """,
            (user_id, memory)
        )

        conn.commit()
        return True


def get_memories(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT memory
            FROM memories
            WHERE user_id = ?
            ORDER BY created_at
            """,
            (user_id,)
        ).fetchall()

    return [row[0] for row in rows]


if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DB_PATH}")