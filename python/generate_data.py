import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Ustawienia projektu
random.seed(42)

PROJECT = Path(__file__).resolve().parent.parent
DATA = PROJECT / "data"
DATA.mkdir(exist_ok=True)

# Dane klientów i pracowników
customers = [f"C{i:03d}" for i in range(1, 51)]
agents = [f"A{i:03d}" for i in range(1, 9)]

categories = [
    "Delivery Delay",
    "Missing Documents",
    "Incorrect Invoice",
    "Damaged Shipment",
    "Tracking Issue",
    "General Inquiry"
]

priorities = ["Low", "Medium", "High", "Urgent"]

sla_hours = {
    "Low": 168,
    "Medium": 120,
    "High": 72,
    "Urgent": 24
}

# Wplyw kategorii na czas rozwiazania

category_duration_factors = {
    "Delivery Delay": 1.20,
    "Missing Documents": 1.00,
    "Incorrect Invoice": 1.10,
    "Damaged Shipment": 1.25,
    "Tracking Issue": 0.90,
    "General Inquiry": 0.85
}

# Tworzenie zgłoszeń
tickets = []

start_date = datetime(2026, 1, 1)

for i in range(1, 10001):

    created = start_date + timedelta(
        minutes=random.randint(0, 181 * 24 * 60 - 1)
    )

    priority = random.choices(
        priorities,
        weights=[20, 45, 25, 10]
    )[0]

    category = random.choices(
    categories,
    weights=[25, 16, 14, 12, 20, 13],
    k=1
)[0]

    deadline = created + timedelta(
        hours=sla_hours[priority]
    )

    is_resolved = random.random() < 0.92

    if is_resolved:
        duration = (
    random.uniform(0.35, 1.25)
    * sla_hours[priority]
    * category_duration_factors[category]
)
        resolved = created + timedelta(hours=duration)
        status = "Resolved"
    else:
        resolved = None
        status = "Open"

    tickets.append({
        "ticket_id": i,
        "customer_id": random.choices(
    customers,
    weights=[5] * 8 + [1] * 42,
    k=1
)[0],
        "agent_id": random.choice(agents),
        "category": category,
        "priority": priority,
        "created_at": created.isoformat(),
        "resolved_at": resolved.isoformat() if resolved else "",
        "sla_deadline": deadline.isoformat(),
        "status": status,
        "reopened": int(is_resolved and random.random() < 0.08)
    })

# Zapis danych do CSV
output = DATA / "tickets.csv"

with open(output, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=tickets[0].keys()
    )

    writer.writeheader()
    writer.writerows(tickets)

print("Data generated successfully!")
print(f"Total tickets: {len(tickets)}")
print(f"File saved: {output}")