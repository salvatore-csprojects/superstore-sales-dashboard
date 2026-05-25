import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv(
    "../data/raw/Sample - Superstore.csv",
    encoding="latin1"
)

# ---------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"])

df["Month"] = df["Order Date"].dt.month_name()
df["Year"] = df["Order Date"].dt.year

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📌 Dashboard Filters")

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
filtered_df = df[
    (df["Year"].isin(selected_year)) &
    (df["Category"].isin(selected_category))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("📊 Superstore Analytics Dashboard")

st.markdown("""
Interactive business intelligence dashboard built with Streamlit and Plotly.
""")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
profit_margin = (total_profit / total_sales) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("💵 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🧾 Total Orders", total_orders)
col4.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Sales Analysis",
    "👥 Customer Analysis",
    "📉 Profitability Analysis"
])

# ---------------------------------------------------
# TAB 1
# ---------------------------------------------------
with tab1:

    col_left, col_right = st.columns(2)

    with col_left:

        sales_by_category = (
            filtered_df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
            .sort_values(by="Sales", ascending=False)
        )

        fig1 = px.bar(
            sales_by_category,
            x="Sales",
            y="Category",
            orientation="h",
            title="Sales by Category",
            text_auto=".2s"
        )

        fig1.update_layout(height=500)

        st.plotly_chart(fig1, use_container_width=True)

    with col_right:

        monthly_sales = (
            filtered_df.groupby("Month")["Sales"]
            .sum()
            .reset_index()
        )

        monthly_sales["Month"] = pd.Categorical(
            monthly_sales["Month"],
            categories=month_order,
            ordered=True
        )

        monthly_sales = monthly_sales.sort_values("Month")

        fig2 = px.line(
            monthly_sales,
            x="Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        fig2.update_layout(height=500)

        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# TAB 2
# ---------------------------------------------------
with tab2:

    top_customers = (
        filtered_df.groupby("Customer Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
        .head(10)
    )

    fig3 = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Top 10 Customers",
        text_auto=".2s"
    )

    fig3.update_layout(height=600)

    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# TAB 3
# ---------------------------------------------------
with tab3:

    col_bottom_left, col_bottom_right = st.columns(2)

    with col_bottom_left:

        profit_by_category = (
            filtered_df.groupby("Category")["Profit"]
            .sum()
            .reset_index()
            .sort_values(by="Profit", ascending=False)
        )

        fig4 = px.bar(
            profit_by_category,
            x="Profit",
            y="Category",
            orientation="h",
            title="Profit by Category",
            text_auto=".2s"
        )

        fig4.update_layout(height=500)

        st.plotly_chart(fig4, use_container_width=True)

    with col_bottom_right:

        fig5 = px.scatter(
            filtered_df,
            x="Sales",
            y="Profit",
            color="Category",
            hover_data=["Customer Name"],
            title="Sales vs Profit"
        )

        fig5.update_layout(height=500)

        st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.caption("Built by Salvatore Lara using Streamlit + Plotly")