import streamlit as st
import pandas as pd

st.title("AI Revenue Leakage Detection System")

data = pd.read_csv("dataset.csv")

st.subheader("Hospital Data")
st.dataframe(data)

data["loss"] = data["charge"] - data["paid_amount"]

total_loss = data["loss"].sum()

missing_claims = data[data["claim_submitted"] == "No"]
underpaid = data[data["paid_amount"] < data["charge"]]

st.metric("Total Revenue Leakage", total_loss)

st.subheader("Missing Claims")
st.dataframe(missing_claims)

st.subheader("Underpaid Claims")
st.dataframe(underpaid)

st.bar_chart(data[["charge", "paid_amount"]])
