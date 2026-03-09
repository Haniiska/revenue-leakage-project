import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Revenue Leakage Detection", layout="wide")

st.title("🏥 AI Revenue Leakage Detection System")
st.write("Upload hospital datasets to detect revenue leakage.")

# Sidebar uploads
st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File", type=["xlsx"])
billing_file = st.sidebar.file_uploader("Upload Billing File", type=["xlsx"])
insurance_file = st.sidebar.file_uploader("Upload Insurance File", type=["xlsx"])


if patients_file and billing_file and insurance_file:

    # Load files
    patients = pd.read_excel(patients_file)
    billing = pd.read_excel(billing_file)
    insurance = pd.read_excel(insurance_file)

    st.success("Files uploaded successfully ✅")

    # Merge datasets
    df = pd.merge(patients, billing, on="Patient_ID", how="left")
    df = pd.merge(df, insurance, on="Patient_ID", how="left")

    # Revenue leakage calculation
    df["Revenue_Loss"] = df["Billed_Amount_USD"] - df["Actual_Payment_USD"]

    df["Revenue_Loss"] = df["Revenue_Loss"].fillna(0)

    # Identify issues
    missing_claims = df[df["Claim_Submitted"] == "No"]
    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    total_loss = df["Revenue_Loss"].sum()

    st.divider()

    # Dashboard
    st.header("📊 Revenue Leakage Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Patients", df["Patient_ID"].nunique())
    col2.metric("Missing Claims", len(missing_claims))
    col3.metric("Underpaid Claims", len(underpaid_claims))
    col4.metric("Total Revenue Leakage", f"$ {total_loss}")

    st.divider()

    # Full Data
    st.subheader("Hospital Combined Dataset")
    st.dataframe(df)

    # Missing claims
    st.subheader("⚠ Missing Claims")
    st.dataframe(missing_claims)

    # Underpaid claims
    st.subheader("💰 Underpaid Claims")
    st.dataframe(underpaid_claims)

    # Chart
    st.subheader("Revenue Comparison")
    st.bar_chart(df[["Billed_Amount_USD", "Actual_Payment_USD"]])

else:

    st.info("Please upload all three files to begin analysis.")
