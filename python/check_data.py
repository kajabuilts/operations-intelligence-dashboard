import pandas as pd
from pathlib import Path

# 1. Wczytanie danych
project = Path(__file__).resolve().parent.parent
file_path = project / "data" / "tickets.csv"

df = pd.read_csv(file_path)

print("=== DATA QUALITY REPORT ===")

# 2. Liczba zgłoszeń
print("\nTotal tickets:", len(df))

# 3. Sprawdzenie duplikatów
duplicates = df["ticket_id"].duplicated().sum()
print("Duplicate ticket IDs:", duplicates)

# 4. Sprawdzenie brakujących wartości
print("\nMissing values:")
print(df.isnull().sum())

# 5. Rozkład priorytetów
print("\nTickets by priority:")
print(df["priority"].value_counts())

# 6. Rozkład statusów
print("\nTickets by status:")
print(df["status"].value_counts())

# 7. Sprawdzenie poprawności dat
df["created_at"] = pd.to_datetime(df["created_at"])
df["resolved_at"] = pd.to_datetime(df["resolved_at"])
df["sla_deadline"] = pd.to_datetime(df["sla_deadline"])

invalid_dates = (
    df["resolved_at"] < df["created_at"]
).sum()

print("\nInvalid resolution dates:", invalid_dates)

# 8. Sprawdzenie zgodności statusów z datami
invalid_status = (
    ((df["status"] == "Resolved") & df["resolved_at"].isna())
    |
    ((df["status"] == "Open") & df["resolved_at"].notna())
).sum()

print("Invalid status/date combinations:", invalid_status)

print("\n=== END OF REPORT ===")