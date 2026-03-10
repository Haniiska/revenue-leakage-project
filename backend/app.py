from fastapi import FastAPI, UploadFile, File
import shutil
import os
from ml_model.leakage_detector import detect_leakage

app = FastAPI()


@app.post("/upload")
async def upload_files(
    ehr: UploadFile = File(...),
    billing: UploadFile = File(...),
    claims: UploadFile = File(...)
):

    os.makedirs("data", exist_ok=True)

    ehr_path = f"data/{ehr.filename}"
    billing_path = f"data/{billing.filename}"
    claims_path = f"data/{claims.filename}"

    with open(ehr_path, "wb") as f:
        shutil.copyfileobj(ehr.file, f)

    with open(billing_path, "wb") as f:
        shutil.copyfileobj(billing.file, f)

    with open(claims_path, "wb") as f:
        shutil.copyfileobj(claims.file, f)

    result = detect_leakage(ehr_path, billing_path, claims_path)

    return result.head(10).to_dict(orient="records")