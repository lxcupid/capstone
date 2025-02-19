import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configure Streamlit page to use full width
st.set_page_config(layout="wide")

# Page Title
st.title("📊 Tips Data Analysis")

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("tips.csv")

df = load_data()

# Sidebar Menu for Navigation
st.sidebar.header("📌 Select a Chart")
menu = st.sidebar.radio(
    "Choose Visualization",
    ["📋 Show Data", "💰 Total Bill vs. Tip", "📈 Line Chart of Total Bill", "🎭 Distribution of Tips"]
)

# Display Raw Data
if menu == "📋 Show Data":
    st.subheader("📋 Raw Data Preview")

    # User input for row selection
    row_start = st.number_input("Enter start row:", min_value=0, max_value=len(df)-1, value=0, step=1)
    row_end = st.number_input("Enter end row:", min_value=row_start+1, max_value=len(df), value=20, step=1)

    # Filter data based on input
    filtered_df = df.iloc[row_start:row_end]

    # Display filtered data
    st.dataframe(filtered_df, use_container_width=True)

    # Summary statistics of the selected data
    st.subheader("📊 Summary Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)

    # Convert filtered data to CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    # Download button
    st.download_button(
        label="📥 Download Selected Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv",

    )

# Scatterplot: Total Bill vs. Tip
elif menu == "💰 Total Bill vs. Tip":
    st.subheader("💰 Total Bill vs. Tip")
    fig, ax = plt.subplots(figsize=(16, 6))  # Set wider figure size
    sns.scatterplot(data=df, x="total_bill", y="tip", hue="day", style="sex", ax=ax)
    st.pyplot(fig)

# Line Chart: Average Total Bill Per Day
elif menu == "📈 Line Chart of Total Bill":
    st.subheader("📈 Average Total Bill Per Day")
    avg_total_bill = df.groupby("day")["total_bill"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(16, 6))  # Set wide figure size
    sns.lineplot(data=avg_total_bill, x="day", y="total_bill", marker="o", ax=ax)
    ax.set_ylabel("Average Total Bill ($)")
    ax.set_title("Average Total Bill Per Day")
    st.pyplot(fig)

# Histogram: Tip Distribution
elif menu == "🎭 Distribution of Tips":
    st.subheader("🎭 Distribution of Tips")
    fig, ax = plt.subplots(figsize=(16, 6))  # Set wider figure size
    sns.histplot(df["tip"], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

st.divider()
st.write("🚀 **Use the sidebar to explore different visualizations!**")
