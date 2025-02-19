import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set seaborn style
sns.set()

# Set Streamlit page layout to wide
st.set_page_config(layout="wide")

# Load the dataset
data = pd.read_csv("tips (1).csv")

# Ensure 'billdate' is in datetime format
data["billdate"] = pd.to_datetime(data["billdate"])

# Title of the Streamlit app
st.title("📊 Tips Dataset Visualization")

# 🔹 Line Chart
st.subheader("📈 LINE CHART")
st.line_chart(data, x="billdate", y="total_bill", use_container_width=True)

st.divider()

# 🔹 Scatter Chart
st.subheader("📌 SCATTER CHART")
st.scatter_chart(data, x="tip", y="total_bill", use_container_width=True)

st.divider()

# 🔹 Histogram Chart
st.subheader("📊 HISTOGRAM CHART")

# User selects column for histogram
selected_column = st.selectbox("Select a column for the histogram:", data.columns)

# Format the column name (replace underscores and title-case it)
formatted_column = selected_column.replace("_", " ").title()

# Plot Histogram
fig, ax = plt.subplots(figsize=(15, 5))  # Full-width figure
sns.histplot(data[selected_column], bins=20, kde=True, ax=ax, color="green")

# Apply formatted column name to title and labels
ax.set_title(f"Distribution of {formatted_column}", fontsize=20, color="black", fontweight="bold")
ax.set_xlabel(formatted_column, fontsize=14, color="black", fontweight="bold")

# Display plot in Streamlit
st.pyplot(fig)

st.divider()

# 🔹 Salary & Tax Calculation
st.subheader("💰 Salary & Tax Calculator")

# Two columns for input fields
col1, col2 = st.columns(2)

with col1:
    salary = st.number_input("💵 Enter your salary (₱):", min_value=0.0, format="%.2f")

with col2:
    tax_rate = st.number_input("📉 Enter tax percentage (%):", min_value=0.0, max_value=100.0, format="%.2f")

# Compute net salary
if salary > 0 and tax_rate >= 0:
    tax_amount = (tax_rate / 100) * salary
    net_salary = salary - tax_amount

    st.subheader("📊 Salary Breakdown")

    # Display in a clean metrics format
    col1, col2, col3 = st.columns(3)

    col1.metric(label="💰 **Gross Salary**", value=f"₱{salary:,.2f}")
    col2.metric(label="📉 **Tax Deduction**", value=f"₱{tax_amount:,.2f}", delta=f"-{tax_rate:.2f}%")
    col3.metric(label="✅ **Net Salary**", value=f"₱{net_salary:,.2f}")

st.divider()
st.write("🚀 **Use the sidebar to explore different visualizations!**")
