# Disease Frequency Analysis Using Indian Healthcare Records with Python

## 📌 Project Overview

The **Disease Frequency Analysis Using Indian Healthcare Records with Python** project focuses on analyzing healthcare records to understand disease frequency, patient demographics, clinical indicators, and treatment outcomes.

The project uses Python-based data analysis and visualization techniques to explore healthcare data, identify patterns, and present meaningful insights through charts and an interactive Streamlit dashboard.

## 🎯 Objectives

- Analyze the frequency of different diseases in healthcare records.
- Study disease distribution across age groups, gender, and regions.
- Explore clinical indicators such as blood glucose, HbA1c, cholesterol, and BMI.
- Analyze treatment types and treatment outcomes.
- Visualize patterns and trends using graphs and charts.
- Build a Streamlit dashboard to explore the dataset interactively.

## 📊 Dataset Description

The dataset contains healthcare-related records with information such as:

- Patient ID
- Age and Gender
- Region and Socioeconomic Status
- Primary Diagnosis and Symptoms
- Blood Glucose, HbA1c, Cholesterol, and BMI
- Treatment Type and Treatment Outcome
- Hospital Type and Insurance Coverage
- Visit Date and Imaging Information

The dataset was cleaned and prepared before analysis. Duplicate records, missing values, and placeholder values were handled during data preprocessing.

## 🛠️ Technologies Used

- **Python** – Data analysis and programming
- **Pandas** – Data cleaning and manipulation
- **NumPy** – Numerical operations
- **Matplotlib** – Data visualization
- **Seaborn** – Statistical visualization
- **Plotly** – Interactive visualizations
- **Streamlit** – Dashboard development
- **Power BI** – Planned or additional business intelligence visualization

## 📁 Project Structure

```text
Disease-Frequency-Analytics/
│
├── Dataset/
│   ├── original_healthcare_data.csv
│   └── cleaned_healthcare_data.csv
│
├── Streamlit_Dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── Visualizations/
│   ├── Disease frequency charts
│   └── Choropleth map HTML (if included)
│
├── GeoJSON_Dataset/
│   └── Map boundary data (if required)
│
├── Code/
│   └── Python notebooks and scripts
│
├── PowerBI_Dashboard/
│
├── Synopsis.pdf
├── Project_Report.pdf (when available)
├── Project_Presentation.pptx (when available)
└── README.md
```

*Note: The structure above describes the intended organization. Some files may be added as the project progresses.*

## 📈 Key Analysis Areas

1. Disease frequency and distribution
2. Disease patterns by gender and age group
3. Regional disease distribution
4. Treatment types and outcomes
5. BMI group and disease analysis
6. Clinical indicator analysis
7. Monthly healthcare record trends

## 🚀 Running the Streamlit Dashboard

### 1. Clone the repository

```bash
git clone < https://github.com/rishugupta23/Disease-Frequency-Analytics >
cd Disease-Frequency-Analytics
```

### 2. Install dependencies

```bash
pip install -r Streamlit_Dashboard/requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run Streamlit_Dashboard/app.py
```

Ensure that the cleaned dataset is available at the file path expected by `app.py`.

## 📂 Visualizations

The `Visualizations` folder contains exported charts and other visualization outputs generated during the analysis. An HTML map, if included, can be downloaded and opened in a web browser; GitHub does not automatically run interactive HTML files.

## 🔮 Future Scope

- Expand the analysis with additional healthcare datasets.
- Improve interactive visualizations and dashboard functionality.
- Add further regional comparisons where reliable geographic data is available.
- Develop additional reports using Power BI.
- Improve data quality checks and analytical reporting.

## ⚠️ Disclaimer

This project is intended for educational and analytical purposes only. The findings depend on the available dataset and should not be interpreted as medical advice or as representative of the entire Indian population.

## 👨‍💻 Author

**Rishu Gupta**  
B.Tech – Computer Science Engineering (Artificial Intelligence & Machine Learning)

---

⭐ If you find this project useful, feel free to explore the repository and its visualizations.
