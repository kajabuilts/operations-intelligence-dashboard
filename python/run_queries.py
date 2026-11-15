import sqlite3
from pathlib import Path

# Project paths
project = Path(__file__).resolve().parent.parent

database = project / "data" / "operations.db"
sql_file = project / "sql" / "basic_analysis.sql"

# Read SQL queries
sql_text = sql_file.read_text(encoding="utf-8")

queries = sql_text.split(";")

print("=== SQL ANALYSIS REPORT ===")

with sqlite3.connect(database) as connection:

    for index, query in enumerate(queries, start=1):

        query = query.strip()

        if not query:
            continue

        cursor = connection.execute(query)

        print(f"\n--- QUERY {index} ---")

        # Column names
        columns = [column[0] for column in cursor.description]
        print(" | ".join(columns))

        # Results
        for row in cursor.fetchall():
            print(" | ".join(str(value) for value in row))

print("\n=== END OF REPORT ===")