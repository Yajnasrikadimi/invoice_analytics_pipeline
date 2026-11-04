import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load the cleaned invoices
df = pd.read_csv("data/cleaned_invoices.csv")


def find_anomalies(data):
    data = data.copy()

    # How big is this invoice compared with the customer's and category's average?
    data["vs_customer"] = data["amount"] / data.groupby("customer")["amount"].transform("mean")
    data["vs_category"] = data["amount"] / data.groupby("category")["amount"].transform("mean")

    features = data[["amount", "vs_customer", "vs_category"]]

    # Flag the most unusual ~1% of invoices
    model = IsolationForest(contamination=0.01, random_state=42)
    data["flag"] = model.fit_predict(features) == -1   # True = unusual
    data["anomaly_score"] = -model.score_samples(features)  # higher = more unusual
    return data


# 2. Run on the real data
result = find_anomalies(df)
flagged = result[result["flag"]].sort_values("anomaly_score", ascending=False)
flagged.to_csv("data/flagged_invoices.csv", index=False)

print("Invoices checked:", len(result))
print("Invoices flagged:", len(flagged))
print()
print("Top 10 most unusual invoices:")
print(flagged[["invoice_id", "customer", "category", "amount", "vs_customer", "anomaly_score"]].head(10).to_string(index=False))

# 3. Sanity test: plant 10 fake invoices at 10x their normal amount
test = df.copy()
planted_ids = test.sample(10, random_state=1)["invoice_id"].tolist()
test.loc[test["invoice_id"].isin(planted_ids), "amount"] *= 10
test_result = find_anomalies(test)
caught = test_result[test_result["invoice_id"].isin(planted_ids) & test_result["flag"]]
print()
print(f"Planted-anomaly test: caught {len(caught)} of 10")