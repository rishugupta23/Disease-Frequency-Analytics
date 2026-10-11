
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.express as px

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Indian Healthcare Analytics",
    page_icon="🏥",
    layout="wide"
)

sns.set_theme(style="whitegrid")

# --------------------------------------------------
# 2. LOAD CLEANED DATASET
# --------------------------------------------------
DATA_FILE = Path(__file__).parent / "new_cleaned_healthcare_data.csv"

st.title("🏥 Indian Healthcare Analytics Dashboard")
st.write(
    "Disease frequency and healthcare record analysis using Python."
)

if not DATA_FILE.exists():
    st.error(
        "Cleaned dataset not found. Place "
        "'cleaned_healthcare_data.csv' in the same folder as app.py."
    )
    st.stop()

df = pd.read_csv(DATA_FILE)

required_columns = [
    "Patient_ID", "Age", "Gender", "Region",
    "Visit_Date", "Primary_Diagnosis",
    "Blood_Glucose_mg_dL", "HbA1c_%",
    "Total_Cholesterol_mg_dL", "Treatment_Outcome", "BMI"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(f"Missing columns in CSV: {missing_columns}")
    st.stop()

# --------------------------------------------------
# 3. PREPARE DATA TYPES AND DERIVED COLUMNS
# --------------------------------------------------
df["Visit_Date"] = pd.to_datetime(
    df["Visit_Date"], errors="coerce"
)

numeric_columns = [
    "Age", "BMI", "Blood_Glucose_mg_dL",
    "HbA1c_%", "Total_Cholesterol_mg_dL"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

category_columns = [
    "Gender", "Region", "Primary_Diagnosis",
    "Treatment_Outcome"
]

for col in category_columns:
    df[col] = df[col].fillna("Unknown / Not recorded").astype(str)
    df[col] = df[col].replace(
        {"": "Unknown / Not recorded", "nan": "Unknown / Not recorded"}
    )

if "Age_Group" not in df.columns:
    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[0, 18, 35, 50, 65, float("inf")],
        labels=["0-18", "19-35", "36-50", "51-65", "66+"],
        include_lowest=True
    )

if "BMI_Group" not in df.columns:
    df["BMI_Group"] = pd.cut(
        df["BMI"],
        bins=[0, 18.5, 25, 30, float("inf")],
        labels=["Underweight", "Normal", "Overweight", "Obese"],
        right=False
    )

df["Visit_Month"] = df["Visit_Date"].dt.to_period("M").astype(str)
df["Visit_Month"] = df["Visit_Month"].replace("NaT", "Unknown")

st.success("Healthcare dataset loaded successfully!")

# --------------------------------------------------
# 4. SIDEBAR FILTERS
# --------------------------------------------------
# ==================================================
# PATIENT AND DISEASE SEARCH
# ==================================================
st.subheader("🔍 Search Healthcare Records")

search_query = st.text_input(
    "Search by Patient ID, Disease or Region",
    placeholder="e.g. P001, Type 2 Diabetes, Delhi"
)

search_df = df.copy()

if search_query.strip():
    query = search_query.strip()

    search_mask = (
        search_df["Patient_ID"].astype(str).str.contains(
            query, case=False, na=False, regex=False
        )
        | search_df["Primary_Diagnosis"].astype(str).str.contains(
            query, case=False, na=False, regex=False
        )
        | search_df["Region"].astype(str).str.contains(
            query, case=False, na=False, regex=False
        )
    )

    search_df = search_df[search_mask]

st.caption(f"Search matches: {len(search_df)} records")
st.sidebar.header("🔎 Dashboard Filters")

regions = sorted(df["Region"].unique().tolist())
genders = sorted(df["Gender"].unique().tolist())
diseases = sorted(df["Primary_Diagnosis"].unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)

selected_genders = st.sidebar.multiselect(
    "Select Gender",
    options=genders,
    default=genders
)

selected_diseases = st.sidebar.multiselect(
    "Select Disease",
    options=diseases,
    default=diseases
)

# Apply all selected filters
filtered_df = search_df[
    search_df["Region"].isin(selected_regions)
    & search_df["Gender"].isin(selected_genders)
    & search_df["Primary_Diagnosis"].isin(selected_diseases)
].copy()

# --------------------------------------------------
# 5. FILTERED ANALYSIS AND KPI CARDS
# --------------------------------------------------
st.subheader("Filtered Analysis")
st.write(f"Records matching filters: **{len(filtered_df)}**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Filtered Records", len(filtered_df))

with col2:
    st.metric(
        "Disease Types",
        filtered_df["Primary_Diagnosis"].nunique()
    )

with col3:
    st.metric("Regions", filtered_df["Region"].nunique())

with col4:
    st.metric("Gender Categories", filtered_df["Gender"].nunique())

# --------------------------------------------------
# 6. FILTERED HEALTHCARE RECORDS AND CSV DOWNLOAD
# --------------------------------------------------
st.subheader("Healthcare Records")

st.caption(f"Showing {len(filtered_df)} matching records.")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Records (CSV)",
    data=csv_data,
    file_name="filtered_healthcare_records.csv",
    mime="text/csv"
)

# --------------------------------------------------
# 7. DISEASE FREQUENCY
# --------------------------------------------------
st.subheader("Disease Frequency")

if not filtered_df.empty:
    disease_counts = (
        filtered_df["Primary_Diagnosis"]
        .value_counts()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    disease_counts.plot(kind="barh", ax=ax)

    ax.set_title("Disease Frequency in Filtered Records")
    ax.set_xlabel("Number of Records")
    ax.set_ylabel("Disease")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No records match the selected filters.")

# --------------------------------------------------
# 8. DISEASE FREQUENCY BY GENDER
# --------------------------------------------------
st.subheader("Disease Frequency by Gender")

if not filtered_df.empty:
    gender_data = (
        filtered_df.groupby(
            ["Primary_Diagnosis", "Gender"]
        ).size().reset_index(name="Patient_Count")
    )

    gender_pivot = gender_data.pivot(
        index="Primary_Diagnosis",
        columns="Gender",
        values="Patient_Count"
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(11, 6))
    gender_pivot.plot(kind="bar", ax=ax)

    ax.set_title("Disease Counts by Gender")
    ax.set_xlabel("Disease")
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=40)
    ax.legend(title="Gender")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# --------------------------------------------------
# 9. AGE GROUP VS DISEASE
# --------------------------------------------------
st.subheader("Disease Frequency by Age Group")

age_data = filtered_df.dropna(
    subset=["Age_Group", "Primary_Diagnosis"]
)

if not age_data.empty:
    age_summary = (
        age_data.groupby(
            ["Age_Group", "Primary_Diagnosis"],
            observed=False
        ).size().reset_index(name="Patient_Count")
    )

    age_pivot = age_summary.pivot(
        index="Age_Group",
        columns="Primary_Diagnosis",
        values="Patient_Count"
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(11, 6))
    age_pivot.plot(kind="bar", ax=ax)

    ax.set_title("Disease Counts Across Age Groups")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="Disease", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Age-group data is not available for these filters.")

# --------------------------------------------------
# 10. TREATMENT OUTCOME ANALYSIS
# --------------------------------------------------
st.subheader("Disease vs Treatment Outcome")

if not filtered_df.empty:
    outcome_pivot = pd.crosstab(
        filtered_df["Primary_Diagnosis"],
        filtered_df["Treatment_Outcome"]
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    outcome_pivot.plot(kind="bar", stacked=True, ax=ax)

    ax.set_title("Treatment Outcome Counts by Disease")
    ax.set_xlabel("Disease")
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=40)
    ax.legend(title="Treatment Outcome", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# --------------------------------------------------
# 11. BMI GROUP VS DISEASE
# --------------------------------------------------
st.subheader("BMI Category vs Disease")

bmi_data = filtered_df.dropna(
    subset=["BMI_Group", "Primary_Diagnosis"]
)

if not bmi_data.empty:
    bmi_pivot = pd.crosstab(
        bmi_data["BMI_Group"],
        bmi_data["Primary_Diagnosis"]
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    bmi_pivot.plot(kind="bar", ax=ax)

    ax.set_title("Disease Counts Across BMI Categories")
    ax.set_xlabel("BMI Category")
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="Disease", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("BMI category data is not available for these filters.")

# --------------------------------------------------
# 12. CLINICAL INDICATORS BY DISEASE
# --------------------------------------------------
st.subheader("Clinical Indicators by Disease")

clinical_columns = [
    "Blood_Glucose_mg_dL", "HbA1c_%"
]

if not filtered_df.empty:
    clinical_summary = (
        filtered_df.groupby("Primary_Diagnosis")[
            clinical_columns
        ].mean().round(2)
    )

    st.write("Average blood glucose and HbA1c by diagnosis")
    st.dataframe(clinical_summary, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    clinical_summary["Blood_Glucose_mg_dL"].sort_values().plot(
        kind="barh", ax=ax
    )
    ax.set_title("Average Blood Glucose by Disease")
    ax.set_xlabel("Mean Blood Glucose (mg/dL)")
    ax.set_ylabel("Disease")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    clinical_summary["HbA1c_%"].sort_values().plot(
        kind="barh", ax=ax
    )
    ax.set_title("Average HbA1c by Disease")
    ax.set_xlabel("Mean HbA1c (%)")
    ax.set_ylabel("Disease")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# --------------------------------------------------
# 13. CORRELATION HEATMAP
# --------------------------------------------------
st.subheader("Correlation Between Numerical Variables")

correlation_columns = [
    "Age", "BMI", "Blood_Glucose_mg_dL",
    "HbA1c_%", "Total_Cholesterol_mg_dL"
]

correlation_data = filtered_df[correlation_columns].dropna()

if len(correlation_data) >= 2:
    correlation_matrix = correlation_data.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-1,
        vmax=1,
        ax=ax
    )

    ax.set_title("Correlation Heatmap")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Not enough numerical data for correlation analysis.")

# --------------------------------------------------
# 14. MONTHLY RECORD FREQUENCY
# --------------------------------------------------
st.subheader("Monthly Healthcare Record Frequency")

monthly_data = filtered_df[
    filtered_df["Visit_Date"].notna()
].copy()

if not monthly_data.empty:
    monthly_summary = (
        monthly_data.groupby(
            monthly_data["Visit_Date"].dt.to_period("M")
        ).size()
    )

    monthly_summary.index = monthly_summary.index.astype(str)

    fig, ax = plt.subplots(figsize=(11, 5))
    monthly_summary.plot(kind="line", marker="o", ax=ax)

    ax.set_title("Monthly Healthcare Records")
    ax.set_xlabel("Visit Month")
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No valid visit dates available for the selected records.")

# ==================================================
# INTERACTIVE CHARTS USING PLOTLY
# ==================================================
st.divider()
st.header("📈 Interactive Data Visualization")

if filtered_df.empty:
    st.info("Selected search and filters ke liye records nahi hain.")

else:
    # 1. Interactive disease frequency
    st.subheader("1. Disease Frequency")

    disease_plot = (
        filtered_df.groupby("Primary_Diagnosis")
        .size()
        .reset_index(name="Patient_Count")
        .sort_values("Patient_Count", ascending=False)
    )

    fig1 = px.bar(
        disease_plot,
        x="Primary_Diagnosis",
        y="Patient_Count",
        color="Patient_Count",
        title="Disease Frequency",
        hover_data={"Patient_Count": True},
        labels={
            "Primary_Diagnosis": "Disease",
            "Patient_Count": "Number of Records"
        },
        color_continuous_scale="Blues"
    )

    fig1.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(
    fig1,
    use_container_width=True,
    key="interactive_disease_chart",
    config={
        "displayModeBar": True,
        "scrollZoom": True,
        "responsive": True
    }
)

    # 2. Disease counts by gender
    st.subheader("2. Disease by Gender")

    gender_plot = (
        filtered_df.groupby(
            ["Primary_Diagnosis", "Gender"]
        )
        .size()
        .reset_index(name="Patient_Count")
    )

    fig2 = px.bar(
        gender_plot,
        x="Primary_Diagnosis",
        y="Patient_Count",
        color="Gender",
        barmode="group",
        title="Disease Frequency by Gender",
        hover_data=["Patient_Count"],
        labels={
            "Primary_Diagnosis": "Disease",
            "Patient_Count": "Number of Records"
        }
    )

    fig2.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Age group vs disease
    st.subheader("3. Disease by Age Group")

    age_plot_data = filtered_df.dropna(
        subset=["Age_Group"]
    )

    age_plot = (
        age_plot_data.groupby(
            ["Age_Group", "Primary_Diagnosis"],
            observed=False
        )
        .size()
        .reset_index(name="Patient_Count")
    )

    fig3 = px.bar(
        age_plot,
        x="Age_Group",
        y="Patient_Count",
        color="Primary_Diagnosis",
        barmode="group",
        title="Disease Frequency Across Age Groups",
        hover_data=["Patient_Count"],
        labels={
            "Age_Group": "Age Group",
            "Patient_Count": "Number of Records",
            "Primary_Diagnosis": "Disease"
        }
    )

    st.plotly_chart(fig3, use_container_width=True)

    # 4. Treatment outcome
    st.subheader("4. Treatment Outcomes")

    outcome_plot = (
        filtered_df.groupby(
            ["Primary_Diagnosis", "Treatment_Outcome"]
        )
        .size()
        .reset_index(name="Patient_Count")
    )

    fig4 = px.bar(
        outcome_plot,
        x="Primary_Diagnosis",
        y="Patient_Count",
        color="Treatment_Outcome",
        barmode="stack",
        title="Treatment Outcome by Disease",
        hover_data=["Patient_Count"],
        labels={
            "Primary_Diagnosis": "Disease",
            "Patient_Count": "Number of Records",
            "Treatment_Outcome": "Treatment Outcome"
        }
    )

    fig4.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig4, use_container_width=True)

    # 5. Glucose vs HbA1c
    st.subheader("5. Blood Glucose vs HbA1c")

    scatter_data = filtered_df.dropna(
        subset=["Blood_Glucose_mg_dL", "HbA1c_%"]
    )

    fig5 = px.scatter(
        scatter_data,
        x="Blood_Glucose_mg_dL",
        y="HbA1c_%",
        color="Primary_Diagnosis",
        hover_data=["Patient_ID", "Age", "Region"],
        title="Blood Glucose and HbA1c Relationship",
        labels={
            "Blood_Glucose_mg_dL": "Blood Glucose (mg/dL)",
            "HbA1c_%": "HbA1c (%)",
            "Primary_Diagnosis": "Disease"
        }
    )

    st.plotly_chart(fig5, use_container_width=True)

# --------------------------------------------------
# 15. DATASET DETAILS
# --------------------------------------------------
with st.expander("View Dataset Details"):
    st.write("Dataset shape:", df.shape)

    st.write("Column names:")
    st.write(df.columns.tolist())

    st.write("Missing values per column:")
    st.dataframe(
        df.isna().sum().rename("Missing Values"),
        use_container_width=True
    )

    st.write("Descriptive statistics:")
    st.dataframe(
        df.describe(include="all").T,
        use_container_width=True
    )

# --------------------------------------------------
# 16. PROJECT NOTE
# --------------------------------------------------
st.divider()

st.caption(
    "This dashboard presents descriptive patterns in the selected "
    "healthcare dataset. Record counts are not population prevalence. "
    "Correlations do not establish causation, and group averages are "
    "not individual medical diagnoses."
)
