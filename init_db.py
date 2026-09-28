import sqlite3

connection = sqlite3.connect("applications.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        job_title TEXT NOT NULL,
        location TEXT,
        status TEXT NOT NULL,
        application_date TEXT,
        follow_up_date TEXT,
        job_url TEXT,
        notes TEXT,
        priority TEXT DEFAULT 'Medium'
    )
""")

# Check whether the priority column already exists
columns = connection.execute(
    "PRAGMA table_info(applications)"
).fetchall()

column_names = [column[1] for column in columns]

if "priority" not in column_names:
    connection.execute(
        "ALTER TABLE applications ADD COLUMN priority TEXT DEFAULT 'Medium'"
    )

connection.commit()
connection.close()

print("Database initialized successfully!")