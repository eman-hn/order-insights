# ============================================================
# ORDER INSIGHTS DASHBOARD
# ============================================================

# Import Libraries

import pandas as pd
import streamlit as st
import plotly.express as px

# Page Configuration

st.set_page_config(
    page_title="Order Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load the cleaned dataset

df = pd.read_csv(
    "output/cleaned.csv",
    parse_dates=["order_date"]
)

# Dashboard Title

st.title("📊 Online Store - Order Insights")

st.write(
    "An interactive dashboard to explore order data and sales performance."
)


# Filters

st.sidebar.header("Filters")

# Get unique regions and categories
regions = sorted(df["region"].dropna().unique())
categories = sorted(df["category"].dropna().unique())

# Region filter
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    regions,
    default=regions
)

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

# Filter the Dataset

filtered = df[
    df["region"].isin(selected_regions) &
    df["category"].isin(selected_categories)
]

# Key Performance Indicators (KPI)

c1, c2, c3 = st.columns(3)

# Calculate total orders, total sales and average order value
total_orders = len(filtered)
total_sales = filtered["order_value"].sum()
average_order_value = filtered["order_value"].mean()

# Display KPI cards
c1.metric("Total Orders", total_orders)

c2.metric("Total Sales", round(total_sales, 2))

c3.metric(
    "Average Order Value",
    round(average_order_value, 2) if total_orders > 0 else 0
)


# Sales Chart

st.subheader("Total Sales by Region")

# Calculate sales for each region
sales = filtered.groupby(
    "region",
    as_index=False
)["order_value"].sum()

# Create an interactive bar chart
fig = px.bar(
    sales,
    x="region",
    y="order_value",
    title="Total Sales by Region",
    labels={
        "region": "Region",
        "order_value": "Total Sales"
    }
)

# Display the chart
st.plotly_chart(fig, width="stretch")


# Filtered Order Data

st.subheader("Order Details")

# Display the filtered dataset
st.dataframe(
    filtered,
    width="stretch"
)

# Download filtered data

st.download_button(
    label="Download Filtered Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_orders.csv",
    mime="text/csv"
)
