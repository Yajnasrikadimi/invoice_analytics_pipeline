import sqlite3
import pandas as pd

df = pd.read_csv("data/cleaned_invoices.csv")
conn = sqlite3.connect("invoices.db")
df.to_sql("invoices", conn, if_exists="replace", index=False)

def run(title, query):
    print(f"\n--- {title} ---")
    print(pd.read_sql(query, conn).to_string(index=False))

run("Overall KPIs", """
    SELECT COUNT(*) AS total_invoices,
           SUM(amount) AS total_amount,
           SUM(tax) AS total_tax,
           AVG(amount) AS average_invoice,
           MAX(amount) AS largest_invoice
    FROM invoices
""")

run("Invoices by status", """
    SELECT status, COUNT(*) AS invoices, SUM(amount) AS total_amount
    FROM invoices
    GROUP BY status
""")

run("Top customers", """
    SELECT customer, SUM(amount) AS total_amount
    FROM invoices
    GROUP BY customer
    ORDER BY total_amount DESC
""")

run("Monthly trend", """
    SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total_amount
    FROM invoices
    GROUP BY month
    ORDER BY month
""")

run("Money still owed", """
    SELECT status, SUM(amount) AS amount_owed
    FROM invoices
    WHERE status IN ('Unpaid', 'Pending')
    GROUP BY status
""")

conn.close()