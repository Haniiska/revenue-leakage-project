from fastapi import FastAPI
import pandas as pd
from ml_model import detect_anomalies

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Revenue Leakage Detection API running"}

@app.post("/detect")

def detect(data: list):

    df = pd.DataFrame(data)

    df = detect_anomalies(df)

    return df.to_dict(orient="records")
