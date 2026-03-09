import streamlit as st
import pandas as pd
import plotly.express as px

from data_pipeline import load_data
from ml_model import detect_anomalies

# -------------------------
# PAGE SETTINGS
# -------------------------

st.set_page_config(
    page_title="AI Revenue Leakage Detection",
    layout="wide"
)

# -------------------------
# DARK UI STYLE
# -------------------------

st.markdown("""
<style>

.stApp{
background-color:#0f172a;
color:white;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:#020617;
color:white;
}

section[data-testid="stSidebar"] *{
color:white;
}

/* Titles */

h1,h2,h3{
color:#e2e8f0;
}

/* Metric cards */

[data-testid="metric-container"]{
background:#1e293b;
border-radius:10px;
padding:15px;
border-left:5px solid #38bdf8;
}

/* Tables */

[data-testid="stDataFrame"]{
background:#1e293b;
}

/* Buttons */

.stDownloadButton>button{
background:#38bdf8;
color:black;
font-weight:600;
border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------

col1,col2 = st.columns([1,8])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966484.png",width=70)

with col2:
    st.title("AI Revenue Leakage Detection System")
    st.caption("Healthcare Revenue Cycle Analytics Dashboard")

st.info("Upload hospital datasets to detect missing claims, underpayments and AI anomalies.")

# -------------------------
# SIDEBAR UPLOAD
# -------------------------

st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File",type=["xlsx"])
billing_file = st.sidebar.file_uploader("Upload Billing File",type=["xlsx"])
insurance_file = st.sidebar.file_uploader("Upload Insurance File",type=["xlsx"])

# -------------------------
# PROCESS DATA
# -------------------------

if patients_file and billing_file and insurance_file:

    df = load_data(patients_file,billing_file,insurance_file)

    df = detect_anomalies(df)

    st.success("Files uploaded successfully")

    # -------------------------
    # CLAIM ANALYSIS
    # -------------------------

    missing_claims = df[df["Claim_Submitted"]=="No"]

    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    ai_anomalies = df[df["AI_Anomaly"]=="Suspicious"]

    total_loss = df["Revenue_Loss"].sum()

    # -------------------------
    # METRICS
    # -------------------------

    st.header("Revenue Dashboard")

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("Total Patients",df["Patient_ID"].nunique())
    c2.metric("Missing Claims",len(missing_claims))
    c3.metric("Underpaid Claims",len(underpaid_claims))
    c4.metric("AI Suspicious Claims",len(ai_anomalies))
    c5.metric("Revenue Leakage",f"${total_loss}")

    st.divider()

    if total_loss > 0:
        st.error(f"Revenue Leakage Detected: ${total_loss}")
    else:
        st.success("No Revenue Leakage Detected")

    # -------------------------
    # REVENUE CHART
    # -------------------------

    st.subheader("Revenue Comparison")

    fig = px.bar(
        df,
        x="Procedure_Name",
        y=["Billed_Amount_USD","Actual_Payment_USD"],
        barmode="group",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

    # -------------------------
    # DEPARTMENT LOSS
    # -------------------------

    st.subheader("Department Revenue Leakage")

    dept = df.groupby("Department")["Revenue_Loss"].sum().reset_index()

    fig2 = px.bar(
        dept,
        x="Department",
        y="Revenue_Loss",
        template="plotly_dark"
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.divider()

    # -------------------------
    # AI ANOMALY DETECTION
    # -------------------------

    st.header("AI Anomaly Detection")

    st.info("Machine Learning Model Used: Isolation Forest")

    st.metric("AI Suspicious Claims Detected",len(ai_anomalies))

    fig_ml = px.scatter(
        df,
        x="Billed_Amount_USD",
        y="Actual_Payment_USD",
        color="AI_Anomaly",
        template="plotly_dark",
        title="AI Anomaly Detection Visualization"
    )

    st.plotly_chart(fig_ml,use_container_width=True)

    st.subheader("Suspicious Claims Detected by AI")

    st.dataframe(ai_anomalies)

    st.divider()

    # -------------------------
    # DATA TABS
    # -------------------------

    tab1,tab2,tab3 = st.tabs([
        "Full Dataset",
        "Missing Claims",
        "Underpaid Claims"
    ])

    with tab1:
        st.dataframe(df)

    with tab2:
        st.dataframe(missing_claims)

    with tab3:
        st.dataframe(underpaid_claims)

    st.divider()

    # -------------------------
    # DOWNLOAD REPORT
    # -------------------------

    st.download_button(
        "Download Revenue Audit Report",
        df.to_csv(index=False),
        "revenue_audit_report.csv"
    )

else:

    st.warning("Upload Patients, Billing and Insurance files to start analysis.")
