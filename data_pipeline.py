import pandas as pd

def load_data(patients_file, billing_file, insurance_file):

    patients = pd.read_excel(patients_file)
    billing = pd.read_excel(billing_file)
    insurance = pd.read_excel(insurance_file)

    df = pd.merge(patients, billing, on="Patient_ID", how="left")
    df = pd.merge(df, insurance, on="Patient_ID", how="left")

    df["Revenue_Loss"] = df["Billed_Amount_USD"] - df["Actual_Payment_USD"]

    return df
