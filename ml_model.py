from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    model = IsolationForest(contamination=0.1, random_state=42)

    features = df[["Billed_Amount_USD","Actual_Payment_USD"]]

    df["AI_Anomaly"] = model.fit_predict(features)

    df["AI_Anomaly"] = df["AI_Anomaly"].map({
        1:"Normal",
        -1:"Suspicious"
    })

    return df
