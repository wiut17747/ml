import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="NY Housing Forecast, 00017747", layout="wide")
st.title("New York Housing Price Prediction Dashboard")


@st.cache_data
def load_and_process():
    df = pd.read_csv("housing_data.csv")
    df_ny = df[df["StateName"] == "NY"].copy()

    id_vars = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
    date_cols = [c for c in df_ny.columns if c not in id_vars]

    df_long = df_ny.melt(
        id_vars=id_vars, value_vars=date_cols, var_name="Date", value_name="Price"
    )
    df_long["Date"] = pd.to_datetime(df_long["Date"])
    df_clean = (
        df_long.dropna(subset=["Price"]).sort_values(["RegionName", "Date"]).copy()
    )

    df_clean["Year"] = df_clean["Date"].dt.year
    df_clean["Month"] = df_clean["Date"].dt.month

    df_model = (
        df_clean.groupby("RegionName")
        .apply(
            lambda g: g.assign(
                Price_Next_Month=g["Price"].shift(-1),
                Price_Lag_1M=g["Price"].shift(1),
                Price_Lag_6M=g["Price"].shift(6),
                Price_Lag_12M=g["Price"].shift(12),
                Price_Roll_3M=g["Price"].rolling(3, min_periods=1).mean().shift(1),
            )
        )
        .reset_index(drop=True)
    )

    df_model = df_model.dropna(subset=["Price_Next_Month", "Price_Lag_12M"])

    return df_clean, df_model


df_clean, df_model = load_and_process()


page = st.sidebar.radio(
    "Go to", ["Overview", "Price Trends", "Top Regions", "Model Results"]
)


if page == "Overview":

    st.write(
        """
    ### Project Summary
    - **Dataset**: Zillow ZHVI — All Homes in New York State
 - **Task**: Predict next-month home value
 - **Best Model**: Linear Regression → R² = 0.99984
    """
    )

elif page == "Price Trends":
    st.header("Interactive Price Trends")
    region = st.selectbox("Select a region", sorted(df_clean["RegionName"].unique()))
    data = df_clean[df_clean["RegionName"] == region]
    fig = px.line(data, x="Date", y="Price", title=f"Historical ZHVI — {region}")
    fig.update_layout(height=600, xaxis_title="Date", yaxis_title="Price ($)")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Top Regions":
    st.header("Most Expensive Regions (Latest Month)")
    latest = df_clean[df_clean["Date"] == df_clean["Date"].max()].nlargest(10, "Price")
    fig = px.bar(
        latest,
        x="Price",
        y="RegionName",
        orientation="h",
        color="Price",
        color_continuous_scale="Viridis",
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.header("Final Model Comparison")
    results = pd.DataFrame(
        {
            "Model": ["Linear Regression", "Random Forest", "XGBoost"],
            "R² Score": [0.99984, 0.9906, 0.9857],
            "MAE (USD)": [11221, 4370, 6130],
        }
    )
    st.table(
        results.style.format(
            {"R² Score": "{:.5f}", "MAE (USD)": "${:,.0f}"}
        ).highlight_max("R² Score", color="#d4edda")
    )

st.caption("Student ID: 00017747")
