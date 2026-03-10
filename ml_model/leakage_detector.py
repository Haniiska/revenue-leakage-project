import pandas as pd
from ml_model.llm_explainer import explain_issue
from ml_model.predictor import detect_anomalies

def detect_leakage(ehr_file, billing_file, claims_file):

    claims = pd.read_csv(claims_file)

    claims.columns = claims.columns.str.strip()

    df = claims.copy()

    def detect_issue(row):

        billed = row["Billed Amount"]
        paid = row["Paid Amount"]

        if paid == 0:
            return "Unpaid Claim"

        elif paid < billed:
            return "Underpayment"

        else:
            return "Normal"

    df["issue"] = df.apply(detect_issue, axis=1)

    # LLM explanation only for first few rows (speed)
    df["llm_explanation"] = ""

    for i in range(min(5, len(df))):

        row = df.iloc[i]

        df.at[i, "llm_explanation"] = explain_issue(
            row["Claim ID"],
            row["issue"],
            row["Billed Amount"],
            row["Paid Amount"]
        )

    # AI anomaly detection
    df = detect_anomalies(df)

    return df