import random
import pandas as pd

random.seed(42)

customers = ["ABC Corp", "XYZ Inc", "Alpha LLC", "InnovateCorp", "SmartSystems",
             "DataWorks", "BlueSky Ltd", "Nova Retail", "Pinnacle Co", "GreenLeaf Inc",
             "Orbit Labs", "Summit Group", "Vertex Corp", "Maple Foods", "Zenith LLC"]

categories = ["Software", "Hardware", "Consulting", "Marketing", "Travel", "Office Supplies"]

dates = pd.date_range("2025-01-01", "2026-09-30")
rows = []
for i in range(1, 5001):
    amount = round(random.uniform(100, 5000), 2)
    rows.append({
        "invoice_id": f"INV{i:05d}",
        "customer": random.choice(customers),
        "category": random.choices(categories, weights=[30, 20, 20, 15, 10, 5])[0],
        "amount": amount,
        "tax": round(amount * 0.08, 2),
        "date": random.choice(dates).strftime("%Y-%m-%d"),
        "status": random.choices(["Paid", "Unpaid", "Pending"], weights=[60, 25, 15])[0],
    })

df = pd.DataFrame(rows)

# Deliberately break about 3% of rows so cleaning has work to do
for idx in random.sample(range(1, len(df)), 150):
    problem = random.choice(["status", "amount", "date", "duplicate"])
    if problem == "status":
        df.loc[idx, "status"] = random.choice([" paid ", "PAID", "unpaid", "pending "])
    elif problem == "amount":
        df.loc[idx, "amount"] = None
    elif problem == "date":
        df.loc[idx, "date"] = "not a date"
    else:
        df.loc[idx, "invoice_id"] = df.loc[idx - 1, "invoice_id"]

df.to_csv("data/invoices_large.csv", index=False)
print("Created data/invoices_large.csv with", len(df), "rows")