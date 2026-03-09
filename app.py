import streamlit as st
import pandas as pd
import plotly.express as px

from data_pipeline import load_data
from ml_model import detect_anomalies

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Revenue Leakage Detection",
    layout="wide"
)

# -----------------------------
# HOSPITAL UI STYLE
# -----------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#f4f9ff,#e8f1ff);
}

/* Sidebar */

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#0a2540,#1f4e79);
color:white;
}

section[data-testid="stSidebar"] *{
color:white;
}

/* Titles */

h1{
color:#0a2540;
font-weight:700;
}

h2{
color:#163a5f;
}

h3{
color:#1f4e79;
}

/* Metric Cards */

[data-testid="metric-container"]{
background:white;
border-radius:12px;
padding:18px;
box-shadow:0 6px 18px rgba(0,0,0,0.1);
border-left:6px solid #2a7de1;
}

/* Data tables */

[data-testid="stDataFrame"]{
background:white;
border-radius:10px;
}

/* Buttons */

.stDownloadButton>button{
background:#2a7de1;
color:white;
border-radius:8px;
padding:10px 20px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

col1,col2 = st.columns([1,8])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966484.png",width=70)

with col2:
    st.title("AI Revenue Leakage Detection System")
    st.caption("Healthcare Revenue Cycle Analytics Dashboard")

st.info("Upload hospital datasets to detect missing claims, underpayments and AI anomalies.")

# -----------------------------
# SIDEBAR UPLOAD
# -----------------------------

st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File",type=["xlsx"])
billing_file = st.sidebar.file_uploader("Upload Billing File",type=["xlsx"])
insurance_file = st.sidebar.file_uploader("Upload Insurance File",type=["xlsx"])

# -----------------------------
# DATA PROCESSING
# -----------------------------

if patients_file and billing_file and insurance_file:

    df = load_data(patients_file,billing_file,insurance_file)

    df = detect_anomalies(df)

    st.success("Files uploaded successfully")

    # -----------------------------
    # REVENUE LOGIC
    # -----------------------------

    missing_claims = df[df["Claim_Submitted"]=="No"]

    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    ai_anomalies = df[df["AI_Anomaly"]=="Suspicious"]

    total_loss = df["Revenue_Loss"].sum()

    # -----------------------------
    # DASHBOARD METRICS
    # -----------------------------

    st.header("Revenue Dashboard")

    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric("Total Patients",df["Patient_ID"].nunique())
    col2.metric("Missing Claims",len(missing_claims))
    col3.metric("Underpaid Claims",len(underpaid_claims))
    col4.metric("AI Suspicious Claims",len(ai_anomalies))
    col5.metric("Revenue Leakage",f"${total_loss}")

    st.divider()

    # -----------------------------
    # ALERT
    # -----------------------------

    if total_loss > 0:
        st.error(f"Revenue Leakage Detected: ${total_loss}")
    else:
        st.success("No Revenue Leakage Detected")

    # -----------------------------
    # REVENUE CHART
    # -----------------------------

    st.subheader("Revenue Comparison")

    fig = px.bar(
        df,
        x="Procedure_Name",
        y=["Billed_Amount_USD","Actual_Payment_USD"],
        barmode="group",
        color_discrete_sequence=["#2a7de1","#6ec6ff"]
    )

    st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # DEPARTMENT LOSS
    # -----------------------------

    st.subheader("Department Revenue Leakage")

    dept = df.groupby("Department")["Revenue_Loss"].sum().reset_index()

    fig2 = px.bar(
        dept,
        x="Department",
        y="Revenue_Loss",
        color="Revenue_Loss",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.divider()

    # -----------------------------
    # DATA TABS
    # -----------------------------

    tab1,tab2,tab3,tab4 = st.tabs([
        "Full Dataset",
        "Missing Claims",
        "Underpaid Claims",
        "AI Suspicious Claims"
    ])

    with tab1:
        st.dataframe(df,use_container_width=True)

    with tab2:
        st.dataframe(missing_claims,use_container_width=True)

    with tab3:
        st.dataframe(underpaid_claims,use_container_width=True)

    with tab4:
        st.subheader("AI Detected Suspicious Claims")
        st.dataframe(ai_anomalies,use_container_width=True)

    st.divider()

    # -----------------------------
    # DOWNLOAD REPORT
    # -----------------------------

    st.download_button(
        "Download Revenue Audit Report",
        df.to_csv(index=False),
        "revenue_audit_report.csv"
    )

else:

    st.warning("Upload Patients, Billing and Insurance files to start analysis.")
