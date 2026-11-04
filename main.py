import pandas as pd

# 1. LOAD the data
df = pd.read_csv("data/invoices_large.csv")
print("Rows loaded:", len(df))
print(df.head())

# 2. CLEAN: fix common problems
df["status"] = df["status"].str.strip().str.title()      # " paid " -> "Paid"
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["tax"] = pd.to_numeric(df["tax"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.drop_duplicates(subset="invoice_id")
df = df.dropna(subset=["amount", "date"])
raw = pd.read_csv("data/invoices_large.csv")
rejected = raw[~raw.index.isin(df.index)]
rejected.to_csv("data/rejected_invoices.csv", index=False)
print("Rejected rows saved:", len(rejected))

# 3. ANALYZE: business questions answered as numbers
print("\n--- KPIs ---")
print("Total invoices:   ", len(df))
print("Total amount:     ", df["amount"].sum())
print("Total tax:        ", df["tax"].sum())
print("Average invoice:  ", df["amount"].mean())
print("Largest invoice:  ", df["amount"].max())
print("\nCount by status:\n", df["status"].value_counts())
print("\nAmount by status:\n", df.groupby("status")["amount"].sum())
print("\nTop customers:\n", df.groupby("customer")["amount"].sum().sort_values(ascending=False))

# 4. SAVE the cleaned data
df.to_csv("data/cleaned_invoices.csv", index=False)
print("\nSaved data/cleaned_invoices.csv")