"""
Generate Styled Excel Executive Model
Module: src/generate_excel_model.py
Produces 'submission_files/05_Petrochemical_Trade_Executive_Model.xlsx'
"""

import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

def create_styled_excel():
    print("=" * 60)
    print("GENERATING STYLED EXCEL EXECUTIVE MODEL")
    print("=" * 60)
    
    clean_df = pd.read_csv("data/processed/cleaned_trade_data.csv")
    ml_comp = pd.read_csv("outputs/models/model_benchmark_comparison.csv")
    hyp_df = pd.read_csv("submission_files/04_Statistical_Hypothesis_Testing_Results.csv")
    
    output_path = "submission_files/05_Petrochemical_Trade_Executive_Model.xlsx"
    os.makedirs("submission_files", exist_ok=True)
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # Style definitions
    font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_normal = Font(name="Calibri", size=11)
    
    fill_navy = PatternFill(start_color="1D3557", end_color="1D3557", fill_type="solid")
    fill_teal = PatternFill(start_color="2A9D8F", end_color="2A9D8F", fill_type="solid")
    fill_light = PatternFill(start_color="F4F6F8", end_color="F4F6F8", fill_type="solid")
    
    thin_border = Border(
        left=Side(style="thin", color="D3D3D3"),
        right=Side(style="thin", color="D3D3D3"),
        top=Side(style="thin", color="D3D3D3"),
        bottom=Side(style="thin", color="D3D3D3")
    )
    
    # -------------------------------------------------------------
    # SHEET 1: Executive Summary & KPI Cards
    # -------------------------------------------------------------
    ws1 = wb.create_sheet("Executive_Summary")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("A1:G2")
    ws1["A1"] = "PETROCHEMICAL TRADE ANALYTICS - EXECUTIVE SUMMARY"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_navy
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1["A4"] = "Core Metric"
    ws1["B4"] = "Academic Value"
    ws1["C4"] = "Unit / Format"
    ws1["D4"] = "Strategic Significance"
    for col_letter in ["A", "B", "C", "D"]:
        cell = ws1[f"{col_letter}4"]
        cell.font = font_header
        cell.fill = fill_teal
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    kpi_rows = [
        ("TOTAL GROSS TRADE", "$302.18 Billion", "USD (Billions)", "Global commercial activity across 5 basic petrochemicals"),
        ("TOTAL IMPORTS", "$153.74 Billion", "USD (Billions)", "Aggregate inbound consumption across 8 major economies"),
        ("TOTAL EXPORTS", "$148.44 Billion", "USD (Billions)", "Aggregate outbound supply chain clearance"),
        ("NET TRADE BALANCE", "-$5.29 Billion", "USD (Billions)", "Structural import deficit driven by Asian demand"),
        ("TOTAL QUANTITY", "334.13 Million MT", "Metric Tons (Mt)", "Global physical volume shipped across 2015-2024"),
        ("REPORTED USABLE DATA", "97.10%", "Percentage (%)", "High reliability UN Comtrade reporting integrity"),
        ("MACHINE LEARNING ACCURACY", "R² = 0.9543", "Coefficient of Determination", "Gradient Boosting model trade forecasting precision")
    ]
    
    for row_idx, r in enumerate(kpi_rows, start=5):
        ws1[f"A{row_idx}"] = r[0]
        ws1[f"B{row_idx}"] = r[1]
        ws1[f"C{row_idx}"] = r[2]
        ws1[f"D{row_idx}"] = r[3]
        for col in ["A", "B", "C", "D"]:
            c = ws1[f"{col}{row_idx}"]
            c.font = font_bold if col == "B" else font_normal
            c.border = thin_border
            if row_idx % 2 == 0:
                c.fill = fill_light
                
    # -------------------------------------------------------------
    # SHEET 2: Annual KPI Breakdown (2015-2024)
    # -------------------------------------------------------------
    ws2 = wb.create_sheet("Annual_KPI_Metrics")
    ws2.views.sheetView[0].showGridLines = True
    
    annual_df = clean_df.groupby(["refYear", "trade_flow"])["trade_value_usd"].sum().unstack().fillna(0)
    annual_vol = clean_df.groupby("refYear")["trade_volume_mt"].sum()
    
    headers2 = ["Year", "Exports (USD B)", "Imports (USD B)", "Total Trade (USD B)", "Trade Balance (USD B)", "Volume (Mt)", "Avg TUV (USD/MT)", "YoY Growth %"]
    for c_idx, h in enumerate(headers2, start=1):
        cell = ws2.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    prev_total = None
    for r_idx, year in enumerate(sorted(clean_df["refYear"].unique()), start=2):
        exp = annual_df.loc[year, "Export"] / 1e9 if "Export" in annual_df.columns else 0
        imp = annual_df.loc[year, "Import"] / 1e9 if "Import" in annual_df.columns else 0
        tot = exp + imp
        bal = exp - imp
        vol = annual_vol.loc[year] / 1e6
        tuv = (tot * 1e9) / (vol * 1e6) if vol > 0 else 0
        yoy = ((tot - prev_total) / prev_total * 100) if prev_total else 0.0
        prev_total = tot
        
        row_vals = [year, round(exp, 2), round(imp, 2), round(tot, 2), round(bal, 2), round(vol, 2), round(tuv, 2), round(yoy, 2)]
        for c_idx, val in enumerate(row_vals, start=1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_normal
            cell.border = thin_border
            if r_idx % 2 == 1:
                cell.fill = fill_light
                
    # -------------------------------------------------------------
    # SHEET 3: Product Breakdown
    # -------------------------------------------------------------
    ws3 = wb.create_sheet("Product_Breakdown")
    ws3.views.sheetView[0].showGridLines = True
    
    prod_df = clean_df.groupby("commodity_name").agg(
        Total_Value_B=("trade_value_usd", lambda x: round(x.sum() / 1e9, 2)),
        Volume_Mt=("trade_volume_mt", lambda x: round(x.sum() / 1e6, 2)),
        Avg_TUV_USD_MT=("trade_unit_value_usd_mt", lambda x: round(x.mean(), 2)),
        Record_Count=("transaction_id", "count")
    ).reset_index()
    
    headers3 = ["Commodity Name", "Total Trade (USD B)", "Volume (Mt)", "Avg Unit Price (USD/MT)", "Record Count"]
    for c_idx, h in enumerate(headers3, start=1):
        cell = ws3.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_teal
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for r_idx, r in prod_df.iterrows():
        row_vals = [r["commodity_name"], r["Total_Value_B"], r["Volume_Mt"], r["Avg_TUV_USD_MT"], r["Record_Count"]]
        for c_idx, val in enumerate(row_vals, start=1):
            cell = ws3.cell(row=r_idx + 2, column=c_idx, value=val)
            cell.font = font_normal
            cell.border = thin_border
            
    # -------------------------------------------------------------
    # SHEET 4: Country Scorecard
    # -------------------------------------------------------------
    ws4 = wb.create_sheet("Country_Scorecard")
    ws4.views.sheetView[0].showGridLines = True
    
    cntry_df = clean_df.groupby("reporter_country").agg(
        Exports_B=("trade_value_usd", lambda x: round(x[clean_df.loc[x.index, "trade_flow"] == "Export"].sum() / 1e9, 2)),
        Imports_B=("trade_value_usd", lambda x: round(x[clean_df.loc[x.index, "trade_flow"] == "Import"].sum() / 1e9, 2)),
        Volume_Mt=("trade_volume_mt", lambda x: round(x.sum() / 1e6, 2)),
        Record_Count=("transaction_id", "count")
    ).reset_index()
    cntry_df["Net_Balance_B"] = cntry_df["Exports_B"] - cntry_df["Imports_B"]
    
    headers4 = ["Reporter Country", "Exports (USD B)", "Imports (USD B)", "Net Balance (USD B)", "Volume (Mt)", "Records"]
    for c_idx, h in enumerate(headers4, start=1):
        cell = ws4.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for r_idx, r in cntry_df.iterrows():
        row_vals = [r["reporter_country"], r["Exports_B"], r["Imports_B"], r["Net_Balance_B"], r["Volume_Mt"], r["Record_Count"]]
        for c_idx, val in enumerate(row_vals, start=1):
            cell = ws4.cell(row=r_idx + 2, column=c_idx, value=val)
            cell.font = font_normal
            cell.border = thin_border
            
    # -------------------------------------------------------------
    # SHEET 5: ML Benchmarks
    # -------------------------------------------------------------
    ws5 = wb.create_sheet("ML_Model_Benchmarking")
    ws5.views.sheetView[0].showGridLines = True
    
    headers5 = list(ml_comp.columns)
    for c_idx, h in enumerate(headers5, start=1):
        cell = ws5.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_teal
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for r_idx, r in ml_comp.iterrows():
        for c_idx, col in enumerate(headers5, start=1):
            cell = ws5.cell(row=r_idx + 2, column=c_idx, value=r[col])
            cell.font = font_normal
            cell.border = thin_border
            
    # -------------------------------------------------------------
    # SHEET 6: Statistical Hypothesis Tests
    # -------------------------------------------------------------
    ws6 = wb.create_sheet("Statistical_Tests")
    ws6.views.sheetView[0].showGridLines = True
    
    headers6 = list(hyp_df.columns)
    for c_idx, h in enumerate(headers6, start=1):
        cell = ws6.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for r_idx, r in hyp_df.iterrows():
        for c_idx, col in enumerate(headers6, start=1):
            cell = ws6.cell(row=r_idx + 2, column=c_idx, value=str(r[col]))
            cell.font = font_normal
            cell.border = thin_border
            
    # -------------------------------------------------------------
    # SHEET 7: Power BI DAX Formulas
    # -------------------------------------------------------------
    ws7 = wb.create_sheet("PowerBI_DAX_Formulas")
    ws7.views.sheetView[0].showGridLines = True
    
    dax_data = [
        ("Total Trade Value", "Total Trade Value = SUM(Fact_TradeTransactions[trade_value_usd])", "Gross commercial trade value (imports + exports)"),
        ("Import Value", 'Import Value = CALCULATE(SUM(Fact_TradeTransactions[trade_value_usd]), Fact_TradeTransactions[trade_flow] = "Import")', "Total value of inbound imports"),
        ("Export Value", 'Export Value = CALCULATE(SUM(Fact_TradeTransactions[trade_value_usd]), Fact_TradeTransactions[trade_flow] = "Export")', "Total value of outbound exports"),
        ("Trade Balance", "Trade Balance = [Export Value] - [Import Value]", "Net surplus (positive) or deficit (negative)"),
        ("Total Quantity Mt", "Total Quantity Mt = DIVIDE(SUM(Fact_TradeTransactions[trade_volume_mt]), 1000000, 0)", "Total physical shipment in Million Metric Tons"),
        ("Weighted Avg Price USD/MT", "Avg Price USD/MT = DIVIDE(SUM(Fact_TradeTransactions[trade_value_usd]), SUM(Fact_TradeTransactions[trade_volume_mt]), 0)", "Trade Unit Value benchmark per metric ton"),
        ("Coverage Ratio", "Coverage Ratio = DIVIDE([Export Value], [Import Value], 0)", "Export to Import solvency ratio"),
        ("YoY Trade Growth %", "YoY Trade Growth = VAR Prev = CALCULATE([Total Trade Value], DATEADD(Dim_Date[full_date], -1, YEAR)) RETURN DIVIDE([Total Trade Value] - Prev, Prev, 0)", "Compound annual percentage expansion rate")
    ]
    
    headers7 = ["Measure Name", "DAX Formula Statement", "Business & Analytical Purpose"]
    for c_idx, h in enumerate(headers7, start=1):
        cell = ws7.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_teal
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for r_idx, dax in enumerate(dax_data, start=2):
        ws7.cell(row=r_idx, column=1, value=dax[0]).font = font_bold
        ws7.cell(row=r_idx, column=2, value=dax[1]).font = font_normal
        ws7.cell(row=r_idx, column=3, value=dax[2]).font = font_normal
        for col_idx in [1, 2, 3]:
            ws7.cell(row=r_idx, column=col_idx).border = thin_border
            
    # Auto-adjust column widths for all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 65)
            
    wb.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    create_styled_excel()
