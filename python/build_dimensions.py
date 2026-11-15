import sqlite3
from pathlib import Path

project = Path(__file__).resolve().parent.parent

db_path = project / "data" / "operations.db"
sql_path = project / "sql" / "create_dimensions.sql"

sql = sql_path.read_text(encoding="utf-8")

with sqlite3.connect(db_path) as connection:

    connection.executescript(sql)

    customers = connection.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    agents = connection.execute(
        "SELECT COUNT(*) FROM agents"
    ).fetchone()[0]

print("=== DIMENSIONS CREATED ===")
print(f"Customers: {customers}")
print(f"Agents: {agents}")