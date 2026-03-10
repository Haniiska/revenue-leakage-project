from fastapi import FastAPI, UploadFile, File
import shutil
import os
import pandas as pd

app = FastAPI()

# Root route
@app.get("/")
def home():
    return {"message": "AI Revenue Leakage API is running"}

@app.post("/upload")
async def upload_files(
    ehr: UploadFile = File(...),
    billing: UploadFile = File(...),
    claims: UploadFile = File(...)
):

    # Render la files save panna correct location
    os.makedirs("/tmp/data", exist_ok=True)

    ehr_path = f"/tmp/data/{ehr.filename}"
    billing_path = f"/tmp/data/{billing.filename}"
    claims_path = f"/tmp/data/{claims.filename}"

    # Save files
    with open(ehr_path, "wb") as f:
        shutil.copyfileobj(ehr.file, f)

    with open(billing_path, "wb") as f:
        shutil.copyfileobj(billing.file, f)

    with open(claims_path, "wb") as f:
        shutil.copyfileobj(claims.file, f)

    # Read CSV files
    ehr_df = pd.read_csv(ehr_path)
    billing_df = pd.read_csv(billing_path)
    claims_df = pd.read_csv(claims_path)

    # Simple demo logic
    ehr_rows = len(ehr_df)
    billing_rows = len(billing_df)
    claims_rows = len(claims_df)

    leakage_detected = billing_rows != claims_rows

    return {
        "ehr_records": ehr_rows,
        "billing_records": billing_rows,
        "claims_records": claims_rows,
        "leakage_detected": leakage_detected
    }