import pandas as pd
from pathlib import Path

# Wczytanie danych
project = Path(__file__).resolve().parent.parent
file_path = project / "data" / "tickets.csv"

df = pd.read_csv(file_path)

# Konwersja dat
df["created_at"] = pd.to_datetime(df["created_at"])
df["resolved_at"] = pd.to_datetime(df["resolved_at"])
df["sla_deadline"] = pd.to_datetime(df["sla_deadline"])

print("=== OPERATIONAL PERFORMANCE REPORT ===")

# 1. Liczba zgłoszeń według kategorii
print("\nTickets by category:")
print(df["category"].value_counts())

# 2. Wybieramy rozwiązane zgłoszenia
resolved = df[df["status"] == "Resolved"].copy()

# 3. Obliczamy czas rozwiązania w godzinach
resolved["resolution_hours"] = (
    resolved["resolved_at"] - resolved["created_at"]
).dt.total_seconds() / 3600

print("\nAverage resolution time (hours):")
print(round(resolved["resolution_hours"].mean(), 2))

# 4. Sprawdzamy dotrzymanie SLA
resolved["sla_met"] = (
    resolved["resolved_at"] <= resolved["sla_deadline"]
)

print("\nSLA Compliance (%):")
print(round(resolved["sla_met"].mean() * 100, 2))

# 5. Analiza według priorytetów
print("\nPerformance by priority:")

performance = resolved.groupby("priority").agg(
    total_tickets=("ticket_id", "count"),
    avg_resolution_hours=("resolution_hours", "mean"),
    sla_compliance=("sla_met", "mean")
)

performance["sla_compliance"] *= 100

print(performance.round(2))

# 6. Performance by category

print("\nPerformance by category:")

category_performance = resolved.groupby("category").agg(
    total_tickets=("ticket_id", "count"),
    avg_resolution_hours=("resolution_hours", "mean"),
    sla_compliance=("sla_met", "mean")
)

category_performance["sla_compliance"] *= 100

print(category_performance.round(2))

# 7. Export results

output_file = project / "data" / "category_performance.csv"

category_performance.round(2).to_csv(
    output_file,
    encoding="utf-8-sig"
)

print("\nCategory performance saved successfully!")

print("\n=== END OF REPORT ===")