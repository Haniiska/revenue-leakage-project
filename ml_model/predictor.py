import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    features = df[["Billed Amount", "Paid Amount"]]

    model = IsolationForest(contamination=0.1, random_state=42)

    df["anomaly"] = model.fit_predict(features)

    df["anomaly"] = df["anomaly"].map({1: "Normal", -1: "Suspicious"})

    return df