import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Revenue Leakage Intelligence",
    layout="wide"
)

st.title("🏥 AI Revenue Leakage Intelligence System")

st.markdown(
    "Detect healthcare billing leakage, underpayments and suspicious claims using **AI + Machine Learning**."
)

st.divider()

# File upload section
col1, col2, col3 = st.columns(3)

with col1:
    ehr = st.file_uploader("Upload EHR Dataset")

with col2:
    billing = st.file_uploader("Upload Billing Dataset")

with col3:
    claims = st.file_uploader("Upload Claims Dataset")

st.divider()

if st.button("🚀 Analyze Leakage"):

    if ehr and billing and claims:

        files = {
            "ehr": ehr,
            "billing": billing,
            "claims": claims
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        data = response.json()

        df = pd.DataFrame(data)

        # Leakage calculation
        df["Leakage"] = df["Billed Amount"] - df["Paid Amount"]

        st.subheader("📊 Leakage Detection Results")

        st.dataframe(df, use_container_width=True)

        # Metrics
        total_claims = len(df)
        underpayment = len(df[df["issue"] == "Underpayment"])
        unpaid = len(df[df["issue"] == "Unpaid Claim"])
        suspicious = len(df[df["anomaly"] == "Suspicious"])
        revenue_loss = df["Leakage"].sum()

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Total Claims", total_claims)
        c2.metric("Underpayment Cases", underpayment)
        c3.metric("Unpaid Claims", unpaid)
        c4.metric("Suspicious Claims", suspicious)
        c5.metric("Estimated Revenue Loss", f"${revenue_loss}")

        st.divider()

        # Billed vs Paid chart
        st.subheader("💰 Billed vs Paid Amount")

        fig1 = px.bar(
            df,
            x="Claim ID",
            y=["Billed Amount", "Paid Amount"],
            barmode="group",
            title="Billing Comparison"
        )

        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        # Provider Leakage Chart
        st.subheader("🏥 Leakage by Provider")

        provider_df = df.groupby("Provider ID")["Leakage"].sum().reset_index()

        fig2 = px.bar(
            provider_df,
            x="Provider ID",
            y="Leakage",
            color="Leakage",
            title="Provider Revenue Leakage"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # Diagnosis Leakage Chart
        st.subheader("🧬 Leakage by Diagnosis")

        diagnosis_df = df.groupby("Diagnosis Code")["Leakage"].sum().reset_index()

        fig3 = px.bar(
            diagnosis_df,
            x="Diagnosis Code",
            y="Leakage",
            color="Leakage",
            title="Diagnosis Revenue Leakage"
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        # Suspicious claims
        st.subheader("⚠ Suspicious Claims (AI Fraud Detection)")

        fraud = df[df["anomaly"] == "Suspicious"]

        if len(fraud) > 0:
            st.dataframe(fraud, use_container_width=True)
        else:
            st.success("No suspicious claims detected.")

    else:

        st.warning("⚠ Please upload all datasets.")