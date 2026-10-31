"""
Standardize and Package All Submission Files for HCL Career Shaper COE
Module: scripts/organize_submission_files.py
"""
import os
import shutil

SUB_DIR = "submission_files"
os.makedirs(SUB_DIR, exist_ok=True)

# Standardized mappings
copies = [
    # 1. Synopsis
    ("submission_files/01_Petrochemical_Trade_Analytics_Project_Synopsis.docx", "submission_files/01_Project_Synopsis_Petrochemical_Trade_Analytics.docx"),
    ("submission_files/01_Petrochemical_Trade_Analytics_Project_Synopsis.pdf", "submission_files/01_Project_Synopsis_Petrochemical_Trade_Analytics.pdf"),
    
    # 2. Code File
    ("submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.docx", "submission_files/02_Complete_Project_Code_File.docx"),
    ("submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.pdf", "submission_files/02_Complete_Project_Code_File.pdf"),

    # 3. Project Screenshots
    ("submission_files/03_Petrochemical_Trade_Analytics_Project_Screenshots.docx", "submission_files/03_Project_Screenshots_and_Working.docx"),
    ("submission_files/03_Petrochemical_Trade_Analytics_Project_Screenshots.pdf", "submission_files/03_Project_Screenshots_and_Working.pdf"),

    # 4. Project Report
    ("submission_files/01_Petrochemical_Trade_Analytics_Project_Report.docx", "submission_files/04_Comprehensive_Project_Report.docx"),
    ("submission_files/01_Petrochemical_Trade_Analytics_Project_Report.pdf", "submission_files/04_Comprehensive_Project_Report.pdf"),

    # 5. Cleaned Dataset
    ("submission_files/02_Cleaned_Petrochemical_Trade_Data.csv", "submission_files/05_Cleaned_Petrochemical_Trade_Data.csv"),

    # 6. ML Model Predictions
    ("submission_files/03_ML_Model_Predictions_and_Evaluation.csv", "submission_files/06_ML_Model_Predictions_and_Evaluation.csv"),

    # 7. Statistical Results
    ("submission_files/04_Statistical_Hypothesis_Testing_Results.csv", "submission_files/07_Statistical_Hypothesis_Testing_Results.csv"),

    # 8. Excel Model
    ("submission_files/05_Petrochemical_Trade_Executive_Model.xlsx", "submission_files/08_Petrochemical_Trade_Executive_Model.xlsx"),

    # 9. Power BI Guide
    ("submission_files/06_PowerBI_DAX_and_Modeling_Guide.pdf", "submission_files/09_PowerBI_DAX_and_Modeling_Guide.pdf"),
]

for src, dst in copies:
    if os.path.exists(src) and src != dst:
        shutil.copy2(src, dst)
        print(f"Copied: {src} -> {dst}")

# Remove old numbered files to avoid duplicates in the UI
old_files_to_remove = [
    "submission_files/01_Petrochemical_Trade_Analytics_Project_Report.docx",
    "submission_files/01_Petrochemical_Trade_Analytics_Project_Report.pdf",
    "submission_files/01_Petrochemical_Trade_Analytics_Project_Synopsis.docx",
    "submission_files/01_Petrochemical_Trade_Analytics_Project_Synopsis.pdf",
    "submission_files/02_Cleaned_Petrochemical_Trade_Data.csv",
    "submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.docx",
    "submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.pdf",
    "submission_files/03_ML_Model_Predictions_and_Evaluation.csv",
    "submission_files/03_Petrochemical_Trade_Analytics_Project_Screenshots.docx",
    "submission_files/03_Petrochemical_Trade_Analytics_Project_Screenshots.pdf",
    "submission_files/04_Statistical_Hypothesis_Testing_Results.csv",
    "submission_files/05_Petrochemical_Trade_Executive_Model.xlsx",
    "submission_files/06_PowerBI_DAX_and_Modeling_Guide.pdf",
]

for f in old_files_to_remove:
    if os.path.exists(f):
        # We also keep a fallback copy of 04_Statistical_Hypothesis_Testing_Results.csv if needed
        if "04_Statistical" in f:
            continue
        os.remove(f)
        print(f"Removed legacy name: {f}")

print("\nFINAL SUBMISSION FILES INVENTORY:")
total_bytes = 0
for f in sorted(os.listdir(SUB_DIR)):
    fp = os.path.join(SUB_DIR, f)
    size = os.path.getsize(fp)
    total_bytes += size
    print(f"  - {f} ({size/1024:.1f} KB)")
print(f"\nTotal package size: {total_bytes/(1024*1024):.2f} MB (Well within 16 MB limit)")
