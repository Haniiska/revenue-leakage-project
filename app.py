import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Revenue Leakage Detection", layout="wide")

st.title("🏥 AI Revenue Leakage Detection System")
st.markdown("Upload hospital data files to detect missing claims and revenue leakage.")

st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File", type=["xlsx","csv"])
billing_file = st.sidebar.file_uploader("Upload Billing File", type=["xlsx","csv"])
claims_file = st.sidebar.file_uploader("Upload Claims File", type=["xlsx","csv"])


def load_file(file):
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return pd.read_csv(file)


if patients_file and billing_file and claims_file:

    patients = load_file(patients_file)
    billing = load_file(billing_file)
    claims = load_file(claims_file)

    st.success("Files uploaded successfully ✅")

    # Merge datasets
    df = patients.merge(billing, on="patient_id", how="left")
    df = df.merge(claims, on="patient_id", how="left")

    # Calculate revenue loss
    df["loss"] = df["charge"] - df["paid_amount"]

    missing_claims = df[df["claim_submitted"] == "No"]
    underpaid = df[df["paid_amount"] < df["charge"]]

    total_loss = df["loss"].sum()

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", len(df))
    col2.metric("Missing Claims", len(missing_claims))
    col3.metric("Revenue Leakage", f"₹ {total_loss}")

    st.divider()

    st.subheader("Hospital Data")
    st.dataframe(df)

    st.subheader("⚠ Missing Claims")
    st.dataframe(missing_claims)

    st.subheader("💰 Underpaid Claims")
    st.dataframe(underpaid)

    st.subheader("Revenue Comparison Chart")
    st.bar_chart(df[["charge","paid_amount"]])

else:
    st.info("Please upload all three files to begin analysis.")
