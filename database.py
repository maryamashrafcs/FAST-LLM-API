import sqlite3

DB_FILE = "tasks.db"

def get_db_connection():
    """Establishes and returns a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by field name
    return conn

def init_db():
    """Creates tasks table and seeds initial tasks if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    # Seed 3 default tasks if table is empty
    if count == 0:
        default_tasks = [
            ("Learn SQLite", 0),
            ("Connect FastAPI to database", 0),
            ("Pass Pytest suite", 0)
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            default_tasks
        )
    
    conn.commit()
    conn.close()