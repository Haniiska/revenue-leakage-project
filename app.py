import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Revenue Leakage Detection", layout="wide")

st.title("🏥 AI Revenue Leakage Detection System")
st.markdown("Upload hospital data files to detect missing claims and revenue leakage.")

# Sidebar Upload
st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File", type=["xlsx","csv"])
billing_file = st.sidebar.file_uploader("Upload Billing File", type=["xlsx","csv"])
claims_file = st.sidebar.file_uploader("Upload Claims File", type=["xlsx","csv"])


# Function to load file
def load_file(file):
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return pd.read_csv(file)


if patients_file and billing_file and claims_file:

    # Load data
    patients = load_file(patients_file)
    billing = load_file(billing_file)
    claims = load_file(claims_file)

    # Fix column names
    patients.columns = patients.columns.str.strip().str.lower()
    billing.columns = billing.columns.str.strip().str.lower()
    claims.columns = claims.columns.str.strip().str.lower()

    st.success("Files uploaded successfully ✅")

    # Merge datasets
    df = pd.merge(patients, billing, on="patient_id", how="left")
    df = pd.merge(df, claims, on="patient_id", how="left")

    # Handle missing values
    df["paid_amount"] = df["paid_amount"].fillna(0)
    df["charge"] = df["charge"].fillna(0)

    # Calculate loss
    df["loss"] = df["charge"] - df["paid_amount"]

    # Identify issues
    missing_claims = df[df["claim_submitted"] == "No"]
    underpaid = df[df["paid_amount"] < df["charge"]]

    total_loss = df["loss"].sum()

    st.divider()

    # Dashboard Metrics
    st.header("📊 Revenue Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Patients", len(df))
    col2.metric("Missing Claims", len(missing_claims))
    col3.metric("Underpaid Claims", len(underpaid))
    col4.metric("Total Revenue Leakage", f"₹ {int(total_loss)}")

    st.divider()

    # Data table
    st.subheader("Hospital Data")
    st.dataframe(df, use_container_width=True)

    # Missing claims
    st.subheader("⚠ Missing Claims")
    st.dataframe(missing_claims, use_container_width=True)

    # Underpaid claims
    st.subheader("💰 Underpaid Claims")
    st.dataframe(underpaid, use_container_width=True)

    # Chart
    st.subheader("Revenue Comparison Chart")
    st.bar_chart(df[["charge","paid_amount"]])

else:

    st.info("Please upload all three files to begin analysis.")
