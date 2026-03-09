import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Page config
st.set_page_config(
    page_title="AI Revenue Leakage Detection",
    layout="wide"
)

# -----------------------------
# Hospital Theme
# -----------------------------

st.markdown("""
<style>

.stApp {
background: linear-gradient(rgba(10,40,80,0.75), rgba(10,40,80,0.75)),
url("https://images.unsplash.com/photo-1576091160399-112ba8d25d1f");
background-size: cover;
background-position: center;
background-attachment: fixed;
}

.block-container {
background: white;
padding: 2rem;
border-radius: 12px;
box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
}

section[data-testid="stSidebar"] {
background-color:#0b2b4c;
color:white;
}

section[data-testid="stSidebar"] * {
color:white;
}

[data-testid="metric-container"] {
background:#f8fbff;
border-left:6px solid #1a73e8;
padding:15px;
border-radius:10px;
box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------

st.title("🏥 AI Revenue Leakage Detection System")
st.caption("Hospital Revenue Cycle Analytics Dashboard")

st.info("Upload hospital datasets to detect missing claims, underpayments and AI anomalies.")

# -----------------------------
# Sidebar Upload
# -----------------------------

st.sidebar.header("Upload Hospital Data")

patients_file = st.sidebar.file_uploader("Upload Patients File", type=["xlsx"])
billing_file = st.sidebar.file_uploader("Upload Billing File", type=["xlsx"])
insurance_file = st.sidebar.file_uploader("Upload Insurance File", type=["xlsx"])

# -----------------------------
# Main Logic
# -----------------------------

if patients_file and billing_file and insurance_file:

    patients = pd.read_excel(patients_file)
    billing = pd.read_excel(billing_file)
    insurance = pd.read_excel(insurance_file)

    st.success("Files uploaded successfully ✅")

    # Merge datasets
    df = pd.merge(patients, billing, on="Patient_ID", how="left")
    df = pd.merge(df, insurance, on="Patient_ID", how="left")

    # Revenue loss
    df["Revenue_Loss"] = df["Billed_Amount_USD"] - df["Actual_Payment_USD"]
    df["Revenue_Loss"] = df["Revenue_Loss"].fillna(0)

    # Missing claims
    missing_claims = df[df["Claim_Submitted"] == "No"]

    # Underpaid claims
    underpaid_claims = df[df["Actual_Payment_USD"] < df["Billed_Amount_USD"]]

    # -----------------------------
    # AI ANOMALY DETECTION
    # -----------------------------

    model = IsolationForest(contamination=0.1, random_state=42)

    features = df[["Billed_Amount_USD","Actual_Payment_USD"]]

    df["AI_Anomaly"] = model.fit_predict(features)

    df["AI_Anomaly"] = df["AI_Anomaly"].map({1:"Normal",-1:"Suspicious"})

    ai_anomalies = df[df["AI_Anomaly"] == "Suspicious"]

    total_loss = df["Revenue_Loss"].sum()

    # -----------------------------
    # Dashboard Metrics
    # -----------------------------

    st.header("📊 Revenue Dashboard")

    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric("Total Patients", df["Patient_ID"].nunique())
    col2.metric("Missing Claims", len(missing_claims))
    col3.metric("Underpaid Claims", len(underpaid_claims))
    col4.metric("AI Suspicious Claims", len(ai_anomalies))
    col5.metric("Revenue Leakage", f"${total_loss}")

    st.divider()

    # Alert
    if total_loss > 0:
        st.error(f"⚠ Revenue Leakage Detected: ${total_loss}")
    else:
        st.success("No Revenue Leakage Detected")

    # -----------------------------
    # Revenue Chart
    # -----------------------------

    st.subheader("Revenue Comparison")

    fig = px.bar(
        df,
        x="Procedure_Name",
        y=["Billed_Amount_USD","Actual_Payment_USD"],
        barmode="group",
        color_discrete_sequence=["#1a73e8","#6ec6ff"]
    )

    st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # Department Leakage
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
    # Tabs
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
        st.dataframe(ai_anomalies,use_container_width=True)

    st.divider()

    # -----------------------------
    # Download Report
    # -----------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Revenue Audit Report",
        data=csv,
        file_name="hospital_revenue_report.csv",
        mime="text/csv"
    )

else:
    st.warning("Upload Patients, Billing and Insurance files to start analysis.")
