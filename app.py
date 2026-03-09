import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="AI Revenue Leakage Detection",
    layout="wide"
)

# Title
st.title("🏥 AI Revenue Leakage Detection System")
st.caption("Smart analytics platform for hospital revenue cycle management")

# Sidebar Upload
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

    # Revenue loss calculation
    df["Revenue_Loss"] = df["Billed_Amount_USD"] - df["Actual_Payment_USD"]
    df["Revenue_Loss"] = df["Revenue_Loss"].fillna(0)

    # Detect issues
    missing_claims = df[df["Claim_Submitted"] == "No"]
    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    total_loss = df["Revenue_Loss"].sum()

    st.divider()

    # Metrics Dashboard
    st.header("📊 Revenue Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Patients", df["Patient_ID"].nunique())
    col2.metric("Missing Claims", len(missing_claims))
    col3.metric("Underpaid Claims", len(underpaid_claims))
    col4.metric("Revenue Leakage", f"$ {total_loss}")

    st.divider()

    # Alert section
    if total_loss > 0:
        st.error(f"⚠ Revenue Leakage Detected: ${total_loss}")
    else:
        st.success("No revenue leakage detected")

    st.divider()

    # Charts
    st.subheader("Revenue Comparison")

    fig = px.bar(
        df,
        x="Procedure_Name",
        y=["Billed_Amount_USD", "Actual_Payment_USD"],
        title="Billed vs Actual Payment",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Department analysis
    st.subheader("Revenue Leakage by Department")

    dept_loss = df.groupby("Department")["Revenue_Loss"].sum().reset_index()

    fig2 = px.bar(
        dept_loss,
        x="Department",
        y="Revenue_Loss",
        color="Revenue_Loss",
        title="Department-wise Revenue Leakage"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Tabs for tables
    tab1, tab2, tab3 = st.tabs(
        ["📄 Full Dataset", "⚠ Missing Claims", "💰 Underpaid Claims"]
    )

    with tab1:
        st.subheader("Hospital Combined Dataset")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Claims Not Submitted to Insurance")
        st.dataframe(missing_claims, use_container_width=True)

    with tab3:
        st.subheader("Insurance Underpaid Claims")
        st.dataframe(underpaid_claims, use_container_width=True)

    st.divider()

    # Download report
    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Revenue Audit Report",
        data=csv,
        file_name="revenue_leakage_report.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload all three files to begin analysis.")
