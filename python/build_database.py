import csv
import sqlite3
from pathlib import Path

# Lokalizacja projektu
project = Path(__file__).resolve().parent.parent

csv_path = project / "data" / "tickets.csv"
db_path = project / "data" / "operations.db"
sql_path = project / "sql" / "create_tables.sql"

# Wczytanie danych CSV
with open(csv_path, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    tickets = list(reader)

# Puste daty zamieniamy na NULL
for ticket in tickets:
    if ticket["resolved_at"] == "":
        ticket["resolved_at"] = None

# Połączenie z bazą danych
with sqlite3.connect(db_path) as connection:

    # Tworzenie tabeli
    sql = sql_path.read_text(encoding="utf-8")
    connection.executescript(sql)

    # Import zgłoszeń
    connection.executemany(
        """
        INSERT INTO tickets (
            ticket_id,
            customer_id,
            agent_id,
            category,
            priority,
            created_at,
            resolved_at,
            sla_deadline,
            status,
            reopened
        )
        VALUES (
            :ticket_id,
            :customer_id,
            :agent_id,
            :category,
            :priority,
            :created_at,
            :resolved_at,
            :sla_deadline,
            :status,
            :reopened
        )
        """,
        tickets
    )

    # Kontrola liczby rekordów
    total = connection.execute(
        "SELECT COUNT(*) FROM tickets"
    ).fetchone()[0]

print("=== DATABASE CREATED ===")
print(f"Total tickets imported: {total}")
print(f"Database: {db_path}")