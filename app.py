import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="AI Revenue Leakage Detection",
    layout="wide"
)

# ----------------------------
# UI STYLE
# ----------------------------

st.markdown("""
<style>

.stApp{
background-color:#f4f7fb;
}

/* Sidebar */
section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#0a2540,#123a66);
}

section[data-testid="stSidebar"] *{
color:white;
}

/* Header */
h1{
color:#0a2540;
font-weight:700;
}

h2,h3{
color:#1b2b4b;
}

/* Metric Cards */
[data-testid="metric-container"]{
background:white;
border-radius:12px;
padding:18px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
border-left:6px solid #1f77ff;
}

/* Info box */
[data-testid="stAlert"][kind="info"]{
background:#e6f2ff;
color:#003366;
}

/* Success box */
[data-testid="stAlert"][kind="success"]{
background:#e6ffed;
color:#14532d;
}

/* Warning box */
[data-testid="stAlert"][kind="warning"]{
background:#fff3cd;
color:#7a5a00;
}

/* Error box */
[data-testid="stAlert"][kind="error"]{
background:#ffe6e6;
color:#7a0000;
}

/* Buttons */
.stDownloadButton>button{
background:#1f77ff;
color:white;
border-radius:8px;
padding:10px 20px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------

col1,col2 = st.columns([1,8])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966484.png",width=70)

with col2:
    st.title("AI Revenue Leakage Detection System")
    st.caption("Hospital Revenue Cycle Analytics Dashboard")

st.info("Upload hospital datasets to detect missing claims, underpayments and AI anomalies.")

# ----------------------------
# SIDEBAR UPLOAD
# ----------------------------

st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File",type=["xlsx"])
billing_file = st.sidebar.file_uploader("Upload Billing File",type=["xlsx"])
insurance_file = st.sidebar.file_uploader("Upload Insurance File",type=["xlsx"])

# ----------------------------
# MAIN LOGIC
# ----------------------------

if patients_file and billing_file and insurance_file:

    patients = pd.read_excel(patients_file)
    billing = pd.read_excel(billing_file)
    insurance = pd.read_excel(insurance_file)

    st.success("Files uploaded successfully")

    # Merge datasets
    df = pd.merge(patients,billing,on="Patient_ID",how="left")
    df = pd.merge(df,insurance,on="Patient_ID",how="left")

    # Revenue Loss
    df["Revenue_Loss"] = df["Billed_Amount_USD"] - df["Actual_Payment_USD"]
    df["Revenue_Loss"] = df["Revenue_Loss"].fillna(0)

    # Missing Claims
    missing_claims = df[df["Claim_Submitted"]=="No"]

    # Underpaid Claims
    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    # ----------------------------
    # ML ANOMALY DETECTION
    # ----------------------------

    model = IsolationForest(contamination=0.1,random_state=42)

    features = df[["Billed_Amount_USD","Actual_Payment_USD"]]

    df["AI_Anomaly"] = model.fit_predict(features)

    df["AI_Anomaly"] = df["AI_Anomaly"].map({1:"Normal",-1:"Suspicious"})

    ai_anomalies = df[df["AI_Anomaly"]=="Suspicious"]

    total_loss = df["Revenue_Loss"].sum()

    # ----------------------------
    # DASHBOARD METRICS
    # ----------------------------

    st.header("Revenue Dashboard")

    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric("Total Patients",df["Patient_ID"].nunique())
    col2.metric("Missing Claims",len(missing_claims))
    col3.metric("Underpaid Claims",len(underpaid_claims))
    col4.metric("AI Suspicious Claims",len(ai_anomalies))
    col5.metric("Revenue Leakage",f"${total_loss}")

    st.divider()

    # Alert
    if total_loss > 0:
        st.error(f"Revenue Leakage Detected: ${total_loss}")
    else:
        st.success("No Revenue Leakage Detected")

    # ----------------------------
    # REVENUE CHART
    # ----------------------------

    st.subheader("Revenue Comparison")

    fig = px.bar(
        df,
        x="Procedure_Name",
        y=["Billed_Amount_USD","Actual_Payment_USD"],
        barmode="group",
        color_discrete_sequence=["#1f77ff","#6ec6ff"]
    )

    st.plotly_chart(fig,use_container_width=True)

    # ----------------------------
    # DEPARTMENT LEAKAGE
    # ----------------------------

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

    # ----------------------------
    # DATA TABS
    # ----------------------------

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

    # ----------------------------
    # DOWNLOAD REPORT
    # ----------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Revenue Audit Report",
        data=csv,
        file_name="revenue_leakage_report.csv",
        mime="text/csv"
    )

else:
    st.warning("Upload Patients, Billing and Insurance files to start analysis.")
