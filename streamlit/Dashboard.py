import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set seaborn style
sns.set()

# Set Streamlit page layout
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("CAPSTONEDATA.csv")

df = load_data()
df["PROJDATE"] = pd.to_datetime(df["PROJDATE"])

# --- SIDEBAR ---
st.sidebar.image("https://marketplace.canva.com/EAFvxbQlQwU/1/0/1600w/canva-blue-modern-artificial-intelligence-technology-logo-fSD54RypYpE.jpg", width=200)
st.sidebar.title("📊 Dashboard Navigation")
menu = st.sidebar.radio("Choose a Section", ["📋 Overview", "📈 Sales & Income", "📊 Tax Analysis", "💰 Salary Calculator"])

st.sidebar.divider()
st.sidebar.write("🚀 **Use the sidebar to navigate!**")

# --- COMMON FILTERS ---
st.sidebar.subheader("🔍 Filters")
start_date, end_date = st.sidebar.date_input("Select Date Range", [df["PROJDATE"].min(), df["PROJDATE"].max()])
filtered_df = df[(df["PROJDATE"] >= pd.Timestamp(start_date)) & (df["PROJDATE"] <= pd.Timestamp(end_date))]

country_filter = st.sidebar.multiselect("Filter by Country", options=df["COUNTRY"].unique(), default=df["COUNTRY"].unique())
filtered_df = filtered_df[filtered_df["COUNTRY"].isin(country_filter)]

# --- OVERVIEW SECTION ---
if menu == "📋 Overview":
    st.title("📊 Financial Overview")

    # --- Filters ---
    st.subheader("🔍 Apply Filters")
    date_range_overview = st.date_input(
        "Select Date Range",
        [df["PROJDATE"].min(), df["PROJDATE"].max()],
        key="overview_date_range"
    )

    country_filter_overview = st.multiselect(
        "Filter by Country",
        options=df["COUNTRY"].unique(),
        default=df["COUNTRY"].unique(),
        key="overview_country_filter"
    )

    # Filter dataset based on selections
    filtered_overview_df = df[
        (df["PROJDATE"] >= pd.Timestamp(date_range_overview[0])) &
        (df["PROJDATE"] <= pd.Timestamp(date_range_overview[1])) &
        (df["COUNTRY"].isin(country_filter_overview))
        ]

    # Display filtered dataset
    with st.expander("📋 View Filtered Dataset"):
        st.dataframe(filtered_overview_df, use_container_width=True)

    # --- Dynamic Key Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"₱{filtered_overview_df['GROSSSALES'].sum():,.2f}")
    col2.metric("Total Income", f"₱{filtered_overview_df['GROSSINCOME'].sum():,.2f}")
    col3.metric("Total Tax", f"₱{filtered_overview_df['TAXDUE'].sum():,.2f}")

    # --- Two-Column Layout for Charts ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Gross Sales Trend")
        st.line_chart(filtered_overview_df, x="PROJDATE", y="GROSSSALES", use_container_width=True)

    with col2:
        st.subheader("📊 Income Distribution by Category")
        income_by_category = filtered_overview_df.groupby("CATEGORY")["GROSSINCOME"].sum().reset_index()
        st.bar_chart(income_by_category, x="CATEGORY", y="GROSSINCOME", use_container_width=True)

# --- SALES & INCOME SECTION ---
elif menu == "📈 Sales & Income":
    st.title("📈 Sales & Income Analysis")

    # --- Year Filter ---
    st.subheader("🔍 Filter by Year")
    available_years = sorted(filtered_df["PROJDATE"].dt.year.unique(), reverse=True)
    selected_year = st.selectbox("📅 Select Year", options=available_years, index=0, key="sales_year")

    # Filter Data Based on Selected Year
    final_filtered_df = filtered_df[filtered_df["PROJDATE"].dt.year == selected_year]

    # --- Key Metrics ---
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gross Sales", f"₱{final_filtered_df['GROSSSALES'].sum():,.2f}")
    col2.metric("Total Net Sales", f"₱{final_filtered_df['NETSALES'].sum():,.2f}")
    col3.metric("Total Gross Income", f"₱{final_filtered_df['GROSSINCOME'].sum():,.2f}")

    # --- Charts Layout ---
    col1, col2 = st.columns(2)

    # --- Line Chart - Net Sales Over Time ---
    with col1:
        st.subheader("📈 Net Sales Trend")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=final_filtered_df, x="PROJDATE", y="NETSALES", marker="o", color="blue", ax=ax)
        ax.set_title(f"Net Sales Trend in {selected_year}", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Net Sales")
        ax.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig)

    # --- Histogram - Net Sales Distribution ---
    with col2:
        st.subheader("📊 Net Sales Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(final_filtered_df["NETSALES"], bins=25, kde=True, color="purple", alpha=0.7, ax=ax)
        ax.set_title(f"Net Sales Distribution in {selected_year}", fontsize=14, fontweight="bold")
        ax.set_xlabel("Net Sales")
        ax.set_ylabel("Frequency")
        ax.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig)

# --- TAX ANALYSIS SECTION ---
elif menu == "📊 Tax Analysis":
    st.title("📊 Tax Analysis")

    # --- Filters ---
    st.subheader("🔍 Apply Filters")
    date_range_tax = st.date_input(
        "Select Date Range",
        [df["PROJDATE"].min(), df["PROJDATE"].max()],
        key="tax_date_range"
    )

    country_filter_tax = st.multiselect(
        "Filter by Country",
        options=df["COUNTRY"].unique(),
        default=df["COUNTRY"].unique(),
        key="tax_country_filter"
    )

    # Filter dataset based on selections
    filtered_tax_df = df[
        (df["PROJDATE"] >= pd.Timestamp(date_range_tax[0])) &
        (df["PROJDATE"] <= pd.Timestamp(date_range_tax[1])) &
        (df["COUNTRY"].isin(country_filter_tax))
        ]

    # --- Dynamic Key Metrics ---
    col1, col2 = st.columns(2)
    col1.metric("Total Tax Due", f"₱{filtered_tax_df['TAXDUE'].sum():,.2f}")
    col2.metric("Total Taxable Income", f"₱{filtered_tax_df['TOTALTAXABLEINCOME'].sum():,.2f}")

    # --- Two-Column Layout for Charts ---
    col1, col2 = st.columns(2)

    # --- Tax Due Per Country (Bar Chart) ---
    with col1:
        st.subheader("🌍 Tax Due Per Country")
        country_tax = filtered_tax_df.groupby("COUNTRY")["TAXDUE"].sum().reset_index()

        # Use Seaborn for a better-designed bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=country_tax, x="TAXDUE", y="COUNTRY", palette="Blues_r", ax=ax)
        ax.set_title("Tax Due by Country", fontsize=14, fontweight="bold")
        ax.set_xlabel("Total Tax Due")
        ax.set_ylabel("Country")
        st.pyplot(fig)

    # --- Tax Breakdown (Pie Chart) ---
    with col2:
        st.subheader("🍰 Tax Breakdown")
        tax_data = filtered_tax_df[["TOTALTAXABLEINCOME", "OSD40", "NETTAXABLEINCOME"]].sum()

        fig, ax = plt.subplots(figsize=(6, 6))
        colors = ["#ff9999", "#66b3ff", "#99ff99"]
        explode = (0.05, 0.05, 0.05)  # Slight separation for better visibility

        wedges, texts, autotexts = ax.pie(
            tax_data, labels=tax_data.index, autopct="%1.1f%%",
            colors=colors, startangle=90, explode=explode,
            wedgeprops={"edgecolor": "black"}
        )

        # Improve text readability
        for text in texts + autotexts:
            text.set_fontsize(12)
            text.set_fontweight("bold")

        ax.set_title("Tax Breakdown", fontsize=16, fontweight="bold")
        st.pyplot(fig)

# --- SALARY CALCULATOR ---
elif menu == "💰 Salary Calculator":
    st.title("💰 Salary & Tax Calculator")

    salary = st.number_input("Enter your salary (₱):", min_value=0.0, format="%.2f")
    tax_rate = st.number_input("Enter tax percentage (%):", min_value=0.0, max_value=100.0, format="%.2f")

    if salary > 0 and tax_rate >= 0:
        tax_amount = (tax_rate / 100) * salary
        net_salary = salary - tax_amount

        st.success(f"📝 **Tax Deduction:** ₱{tax_amount:,.2f}")
        st.success(f"✅ **Net Salary after Tax:** ₱{net_salary:,.2f}")

# --- FOOTER ---
st.divider()
st.write("📊 **Financial Dashboard** | Powered by StreamLex 🚀")


