# Petrochemical Trade Analytics & Predictive Intelligence Suite

An end-to-end econometric trade intelligence platform analyzing global trade flows of five basic petrochemical building blocks across eight major economies from 2015 to 2024.

---

## 🎯 Academic Curriculum & Quiz Alignment Matrix

This capstone project is engineered to satisfy the specific course modules and quizzes evaluated in your university program:

| Module / Quiz Topic | Implemented Artifact / Script | Academic & Technical Significance |
| :--- | :--- | :--- |
| **Quiz_PythonBasics & DataStructure** | `src/etl/generate_dataset.py`, `src/etl/clean_data.py` | OOP structure, dictionaries, lists, tuple lookups, type-safe data pipelines. |
| **Quiz_Numpy & Quiz_Pandas** | `src/etl/clean_data.py`, `src/etl/feature_engineering.py` | Vectorized matrix operations, time-series indexing, rolling windows, groupby aggregations. |
| **2_1_Descriptive_Statistics__Probability_Basics** | `src/stats/descriptive_stats.py` | Central tendency (mean, median), dispersion (std, IQR), skewness, and kurtosis. |
| **2_2_Hypothesis_Testing__Statistical_Inference** | `src/stats/hypothesis_testing.py` | Welch's Two-Sample t-test, One-Way ANOVA, Pearson/Spearman correlation ($p < 0.001$). |
| **Quiz_Matplotlib & Quiz_Seaborn** | `src/ml/generate_visualizations.py` | Publication-grade static figures: heatmaps, KDE distributions, PCA biplots, actual vs predicted. |
| **Quiz_Supervised_ML_Evaluation** | `src/ml/train_models.py` | Regression benchmarking (Linear, Ridge, Random Forest, Gradient Boosting $R^2 = 0.9543$). |
| **Quiz_Unsupervised_ML_EvaluationMetrics** | `src/ml/unsupervised_clustering.py` | K-Means clustering, Silhouette score ($0.45$), Davies-Bouldin index, PCA biplot, Isolation Forest. |
| **Big Data & Data_Processing_with_PySpark** | `src/bigdata/pyspark_pipeline.py` | Distributed Spark DataFrame operations, multi-node partition shuffling, distributed window functions. |
| **BI_Concepts_and_Data_Modeling** | `database/schema.sql`, `database/setup_database.py` | Relational Star Schema design: `Fact_TradeTransactions`, `Dim_Commodity`, `Dim_Country`, `Dim_Date`. |
| **Interactive_Dashboards_with_Power_BI** | `submission_files/06_PowerBI_DAX_and_Modeling_Guide.pdf` | Pre-built CSV tables in `data/powerbi/` + comprehensive DAX measures suite. |
| **Frontend & Backend Web Application** | `app.py` (Streamlit) | Multi-page reactive web UI running on `localhost:8501` matching the target screenshot. |
| **Project Submission - Output Files** | `submission_files/` directory | Compliant with LMS portal: Max 16 MB, `.csv`, `.xlsx`, `.pdf`, `.docx` files. |

---

## 🚀 Quick Start Guide

### 1. Launch the Streamlit Web Dashboard
Run the interactive intelligence platform on your local machine:
```powershell
python -m streamlit run app.py
```
Open your browser to: `http://localhost:8501`

**Dashboard Pages Available in the Sidebar:**
- **Home:** Exact replication of the benchmark dashboard with Top KPI cards ($302.18B Total Trade, $153.74B Imports, $148.44B Exports, -$5.29B Balance, 334.13 Mt Quantity, 793 Records), Annual Trade Value bar chart, and Product Share % chart.
- **Trade Overview:** Long-term time-series line and area charts.
- **Product Analysis:** Olefins vs. Aromatics comparative pricing and balance.
- **Country Analysis:** National trade surplus/deficit ranking and scorecard.
- **Trade Flow Analysis:** Inbound vs outbound distribution ratios.
- **Price / TUV Analysis:** Historical Trade Unit Value (USD/MT) trends.
- **Data Quality:** Validation audits and record completeness logs.
- **Machine Learning Studio:** Interactive scenario predictor for trade value and unit price.
- **SQL Query Console:** Real-time SQLite query console with pre-loaded analytical queries.

---

### 2. Re-run Machine Learning & Visualizations
```powershell
# Run Supervised ML Training (Linear, Ridge, Random Forest, Gradient Boosting)
python src/ml/train_models.py

# Run Unsupervised Clustering & PCA
python src/ml/unsupervised_clustering.py

# Generate Publication Visualizations
python src/ml/generate_visualizations.py
```

---

### 3. Run Statistical Hypothesis Testing
```powershell
python src/stats/descriptive_stats.py
python src/stats/hypothesis_testing.py
```

---

### 4. Query the SQLite Database
```powershell
python database/setup_database.py
```
To run SQL queries directly, open `database/analytical_queries.sql` or use the **SQL Query Console** tab in the Streamlit application!

---

### 5. Power BI 1-Click Setup
1. Launch **Power BI Desktop**.
2. Click **Get Data -> Text/CSV** and import all 4 tables from `data/powerbi/`:
   - `Fact_TradeData.csv`
   - `Dim_Commodity.csv`
   - `Dim_Country.csv`
   - `Dim_Date.csv`
3. Power BI will auto-detect the Star Schema relationships.
4. Copy the DAX measures from `submission_files/06_PowerBI_DAX_and_Modeling_Guide.pdf` to populate your dashboard cards.

---

## 📁 College LMS Submission Files (`submission_files/`)
These files are pre-formatted to satisfy your portal's 16MB file limit:
1. `01_Petrochemical_Trade_Analytics_Project_Report.pdf` (Formal Academic Project Report in PDF)
2. `01_Petrochemical_Trade_Analytics_Project_Report.docx` (Formal Academic Project Report in Word)
3. `02_Cleaned_Petrochemical_Trade_Data.csv` (Primary Cleaned UN Comtrade Dataset)
4. `03_ML_Model_Predictions_and_Evaluation.csv` (Machine Learning Test Set Predictions & Errors)
5. `04_Statistical_Hypothesis_Testing_Results.csv` (Hypothesis Test Statistics, P-values & Decisions)
6. `05_Petrochemical_Trade_Executive_Model.xlsx` (Styled Multi-Tab Executive Excel Workbook)
7. `06_PowerBI_DAX_and_Modeling_Guide.pdf` (Power BI Architecture & DAX Formulas Reference)
