import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="AI Revenue Leakage Detection",
    layout="wide"
)

# Hospital Theme Background
st.markdown(
"""
<style>

.stApp {
background-image: url("https://images.unsplash.com/photo-1586773860418-d37222d8fce3");
background-size: cover;
background-attachment: fixed;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
background-color: rgba(240,248,255,0.95);
}

.block-container {
background-color: rgba(255,255,255,0.92);
padding: 2rem;
border-radius: 12px;
}

[data-testid="metric-container"] {
background-color: white;
border-radius: 10px;
padding: 15px;
border-left: 5px solid #0a4da3;
box-shadow: 0px 2px 8px rgba(0,0,0,0.15);
}

</style>
""",
unsafe_allow_html=True
)

# Header
st.markdown("""
# 🏥 AI Revenue Leakage Detection System
### Hospital Revenue Cycle Analytics Dashboard
""")

st.info("Upload hospital datasets to detect missing claims and revenue leakage automatically.")

# Sidebar Upload
st.sidebar.header("📂 Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File", type=["xlsx"])
billing_file = st.sidebar.file_uploader("Upload Billing File", type=["xlsx"])
insurance_file = st.sidebar.file_uploader("Upload Insurance File", type=["xlsx"])


if patients_file and billing_file and insurance_file:

    # Load data
    patients = pd.read_excel(patients_file)
    billing = pd.read_excel(billing_file)
    insurance = pd.read_excel(insurance_file)

    st.success("Files uploaded successfully ✅")

    # Merge datasets
    df = pd.merge(patients, billing, on="Patient_ID", how="left")
    df = pd.merge(df, insurance, on="Patient_ID", how="left")

    # Revenue Loss
    df["Revenue_Loss"] = df["Billed_Amount_USD"] - df["Actual_Payment_USD"]
    df["Revenue_Loss"] = df["Revenue_Loss"].fillna(0)

    # Issues detection
    missing_claims = df[df["Claim_Submitted"] == "No"]
    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    total_loss = df["Revenue_Loss"].sum()

    st.divider()

    # Dashboard Metrics
    st.header("📊 Revenue Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Patients", df["Patient_ID"].nunique())
    col2.metric("Missing Claims", len(missing_claims))
    col3.metric("Underpaid Claims", len(underpaid_claims))
    col4.metric("Total Revenue Leakage", f"$ {total_loss}")

    st.divider()

    # Alert
    if total_loss > 0:
        st.error(f"⚠ Revenue Leakage Detected: ${total_loss}")
    else:
        st.success("No revenue leakage detected")

    st.divider()

    # Revenue comparison chart
    st.subheader("💰 Revenue Comparison")

    fig = px.bar(
        df,
        x="Procedure_Name",
        y=["Billed_Amount_USD","Actual_Payment_USD"],
        color_discrete_sequence=["#0a4da3","#6ec6ff"],
        barmode="group",
        title="Billed vs Actual Payment"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Department Analysis
    st.subheader("🏥 Department Revenue Leakage")

    dept_loss = df.groupby("Department")["Revenue_Loss"].sum().reset_index()

    fig2 = px.bar(
        dept_loss,
        x="Department",
        y="Revenue_Loss",
        color="Revenue_Loss",
        color_continuous_scale="Blues",
        title="Department-wise Revenue Leakage"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Tabs
    tab1, tab2, tab3 = st.tabs(
        ["📄 Full Dataset", "⚠ Missing Claims", "💰 Underpaid Claims"]
    )

    with tab1:
        st.subheader("Hospital Combined Dataset")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Claims Not Submitted")
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
    st.warning("Please upload Patients, Billing and Insurance files to begin analysis.")
