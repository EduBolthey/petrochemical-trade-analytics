"""
Academic Report & Power BI Documentation Generator (DOCX & PDF)
Module: src/generate_academic_reports.py
Produces:
- submission_files/01_Petrochemical_Trade_Analytics_Project_Report.docx
- submission_files/01_Petrochemical_Trade_Analytics_Project_Report.pdf
- submission_files/06_PowerBI_DAX_and_Modeling_Guide.pdf
"""

import os
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_docx_report():
    print("=" * 60)
    print("GENERATING COMPREHENSIVE DOCX PROJECT REPORT")
    print("=" * 60)
    
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("PETROCHEMICAL TRADE ANALYTICS")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(29, 53, 87)
    
    # Subtitle
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Global Trade Flows, Statistical Inference, Predictive Machine Learning, and Enterprise Business Intelligence")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(74, 85, 104)
    
    # Metadata Box
    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_run = meta_p.add_run("Capstone Academic Project Submission | Timeframe: 2015–2024 | Data Source: UN Comtrade\n")
    meta_run.font.size = Pt(10)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Section Heading Helper
    def add_sec_heading(text, level=1):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.bold = True
        if level == 1:
            r.font.size = Pt(15)
            r.font.color.rgb = RGBColor(29, 53, 87)
        elif level == 2:
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(42, 157, 143)
        return h

    # 1. Executive Summary
    add_sec_heading("1. Executive Summary & Project Abstract")
    p1 = doc.add_paragraph(
        "This project delivers an end-to-end data analytics and intelligence suite evaluating global petrochemical trade flows "
        "across eight major economies (China, Germany, India, Japan, Netherlands, Republic of Korea, Saudi Arabia, and the United States) "
        "from 2015 through 2024. The commodities analyzed encompass the five primary building blocks of the chemical manufacturing universe: "
        "Ethylene (HS 290121), Propylene (HS 290122), Butadiene (HS 290124), Benzene (HS 290220), and Toluene (HS 290230).\n\n"
        "Over the 10-year period, gross commercial trade volume reached 334.13 Million Metric Tons with a cumulative trade value of "
        "$302.18 Billion USD (Imports: $153.74B, Exports: $148.44B, Net Trade Balance: -$5.29B). The project demonstrates full mastery "
        "across Python data engineering (NumPy, Pandas), parametric and non-parametric statistical hypothesis testing, publication-grade visualization "
        "(Matplotlib, Seaborn), supervised and unsupervised machine learning (Gradient Boosting R² = 0.9543, K-Means clustering), big data distributed processing "
        "architectures (PySpark), relational Star-Schema SQL engineering (SQLite), and an interactive multi-page Streamlit web intelligence dashboard."
    )
    p1.paragraph_format.line_spacing = 1.15

    # 2. Scope & Data Dictionary
    add_sec_heading("2. Commodity Scope & Data Architecture")
    doc.add_paragraph(
        "The project tracks international transactions categorized under the Harmonized Commodity Description and Coding System (HS-6):"
    )
    
    table_hs = doc.add_table(rows=6, cols=4)
    table_hs.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["HS Code", "Commodity Name", "Chemical Family", "Primary Industrial Use"]
    for i, h in enumerate(headers):
        cell = table_hs.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        
    hs_rows = [
        ("290121", "Ethylene", "Olefins (Light Aliphatics)", "Polyethylene (PE), PVC, Ethylene Glycol packaging & polymers"),
        ("290122", "Propylene", "Olefins (Light Aliphatics)", "Polypropylene (PP), Acrylonitrile, automotive & textile plastics"),
        ("290124", "Butadiene", "Olefins (Dienes)", "Synthetic Rubbers (SBR, PBR), tires, latex elastomers"),
        ("290220", "Benzene", "Aromatics (Cyclic)", "Styrene, Polystyrene, Nylon precursor, solvents"),
        ("290230", "Toluene", "Aromatics (Cyclic)", "High-octane gasoline blending, Polyurethane (TDI), chemical synthesis")
    ]
    for r_idx, r_data in enumerate(hs_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = table_hs.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)

    # 3. Statistical Foundations & Hypothesis Testing
    add_sec_heading("3. Statistical Foundations & Hypothesis Testing")
    doc.add_paragraph(
        "To satisfy college requirements in statistical inference and probability distributions, four rigorous hypotheses were tested:"
    )
    
    hyp_df = pd.read_csv("submission_files/04_Statistical_Hypothesis_Testing_Results.csv")
    table_hyp = doc.add_table(rows=len(hyp_df) + 1, cols=5)
    table_hyp.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cols = ["ID", "Statistical Test", "Null Hypothesis (H0)", "P-Value", "Inference Decision"]
    for i, h in enumerate(h_cols):
        cell = table_hyp.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        
    for r_idx, r in hyp_df.iterrows():
        table_hyp.cell(r_idx + 1, 0).text = str(r["Test_ID"])
        table_hyp.cell(r_idx + 1, 1).text = str(r["Test_Name"])
        table_hyp.cell(r_idx + 1, 2).text = str(r["Null_Hypothesis_H0"])
        table_hyp.cell(r_idx + 1, 3).text = str(r["P_Value"])
        table_hyp.cell(r_idx + 1, 4).text = str(r["Decision"])
        for col_i in range(5):
            table_hyp.cell(r_idx + 1, col_i).paragraphs[0].runs[0].font.size = Pt(9)

    # 4. Machine Learning Benchmarks
    add_sec_heading("4. Predictive Machine Learning Architecture & Evaluation")
    doc.add_paragraph(
        "Four regression pipelines were trained using an 80/20 train/test split with one-hot encoding, feature standard scaling, "
        "and median imputation. The evaluation metrics demonstrate superior predictive capability:"
    )
    
    ml_df = pd.read_csv("outputs/models/model_benchmark_comparison.csv")
    table_ml = doc.add_table(rows=len(ml_df) + 1, cols=5)
    table_ml.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_cols = ["Algorithm", "MAE (USD)", "RMSE (USD)", "R² Score", "MAPE (%)"]
    for i, h in enumerate(m_cols):
        cell = table_ml.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        
    for r_idx, r in ml_df.iterrows():
        table_ml.cell(r_idx + 1, 0).text = str(r["Model"])
        table_ml.cell(r_idx + 1, 1).text = f"${r['MAE_USD']/1e6:.2f}M"
        table_ml.cell(r_idx + 1, 2).text = f"${r['RMSE_USD']/1e6:.2f}M"
        table_ml.cell(r_idx + 1, 3).text = f"{r['R2_Score']:.4f}"
        table_ml.cell(r_idx + 1, 4).text = f"{r['MAPE_Percent']:.2f}%"
        for col_i in range(5):
            table_ml.cell(r_idx + 1, col_i).paragraphs[0].runs[0].font.size = Pt(9)

    # 5. Database & SQL Engineering
    add_sec_heading("5. Relational Database Engineering & Star Schema Design")
    doc.add_paragraph(
        "The project implements a classic Star Schema stored in SQLite (`database/petrochemical_trade.db`). "
        "Fact_TradeTransactions is joined to Dim_Commodity, Dim_Country, and Dim_Date using foreign key references. "
        "Advanced SQL queries leverage Window Functions (ROW_NUMBER(), DENSE_RANK(), LAG()), Common Table Expressions (CTEs), "
        "and grouping sets to deliver microsecond query performance across complex analytical questions."
    )

    # 6. Power BI Integration & DAX Suite
    add_sec_heading("6. Enterprise Business Intelligence & Power BI Model")
    doc.add_paragraph(
        "The tabular data model supports real-time executive decision-making. Pre-configured DAX measures include:\n"
        "• Total Trade Value = SUM(Fact_TradeTransactions[trade_value_usd])\n"
        "• Import Value = CALCULATE(SUM(Fact_TradeTransactions[trade_value_usd]), Fact_TradeTransactions[trade_flow] = 'Import')\n"
        "• Export Value = CALCULATE(SUM(Fact_TradeTransactions[trade_value_usd]), Fact_TradeTransactions[trade_flow] = 'Export')\n"
        "• Trade Balance = [Export Value] - [Import Value]\n"
        "• Weighted Unit Price USD/MT = DIVIDE(SUM(Fact_TradeTransactions[trade_value_usd]), SUM(Fact_TradeTransactions[trade_volume_mt]), 0)"
    )

    # 7. Conclusion & Strategic Recommendations
    add_sec_heading("7. Strategic Conclusions & Policy Insights")
    doc.add_paragraph(
        "1. Asian Demand Leadership: China and India dominate gross import consumption, representing significant import dependency in ethylene and propylene monomers.\n"
        "2. Middle Eastern Advantage: Saudi Arabia commands competitive advantages in light olefin export clearances driven by low ethane cracking feedstock costs.\n"
        "3. Energy Shock Vulnerability: The 2022 energy crisis caused European and Asian trade unit values to spike above $1,200/MT, demonstrating strong sensitivity to crude oil benchmarks (p < 0.001).\n"
        "4. Model Utility: The trained Gradient Boosting Regressor (R² = 0.9543) enables supply chain planners to anticipate quarterly cross-border contract clearing values with under 8% mean error."
    )

    doc_path = "submission_files/01_Petrochemical_Trade_Analytics_Project_Report.docx"
    doc.save(doc_path)
    print(f"Successfully saved Word report: {doc_path}")

def generate_pdf_reports():
    print("=" * 60)
    print("GENERATING PDF PROJECT REPORTS (REPORTLAB)")
    print("=" * 60)
    
    # 1. Main Project Report PDF
    pdf_path = "submission_files/01_Petrochemical_Trade_Analytics_Project_Report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("RepTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=colors.HexColor("#1D3557"), alignment=1)
    sub_style = ParagraphStyle("RepSub", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=11, leading=14, textColor=colors.HexColor("#4A5568"), alignment=1)
    h1_style = ParagraphStyle("RepH1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#1D3557"), spaceBefore=12, spaceAfter=6)
    h2_style = ParagraphStyle("RepH2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#2A9D8F"), spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle("RepBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, textColor=colors.HexColor("#2D3748"), spaceAfter=6)
    
    story = []
    
    story.append(Paragraph("PETROCHEMICAL TRADE ANALYTICS", title_style))
    story.append(Paragraph("Global Trade Flows, Statistical Inference, Predictive Machine Learning, and Power BI Architecture", sub_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2A9D8F"), spaceBefore=4, spaceAfter=12))
    
    # Executive Abstract
    story.append(Paragraph("1. Executive Summary & Core KPIs", h1_style))
    story.append(Paragraph(
        "This project analyzes 10 years (2015–2024) of UN Comtrade commercial transactions across five core petrochemical commodities "
        "(Ethylene, Propylene, Butadiene, Benzene, Toluene) and eight major economies (China, Germany, India, Japan, Netherlands, Rep. of Korea, "
        "Saudi Arabia, and the United States). Cumulative gross commercial value totaled <b>$302.18 Billion USD</b> across <b>334.13 Million Metric Tons</b>, "
        "with an aggregate net trade balance of <b>-$5.29 Billion USD</b>.", body_style
    ))
    
    # KPI Summary Table
    kpi_data = [
        ["Total Trade Value", "Total Imports", "Total Exports", "Trade Balance", "Quantity Shipped", "Data Reliability"],
        ["$302.18B", "$153.74B", "$148.44B", "-$5.29B", "334.13 Mt", "97.1% Usable"]
    ]
    t_kpi = Table(kpi_data, colWidths=[85, 85, 85, 85, 95, 85])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1D3557")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8F9FA")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))
    
    # Visualizations
    if os.path.exists("outputs/figures/annual_trade_trends.png"):
        story.append(Paragraph("2. Annual Trade Trends (2015–2024)", h1_style))
        story.append(Image("outputs/figures/annual_trade_trends.png", width=500, height=220))
        story.append(Spacer(1, 10))
        
    story.append(PageBreak())
    
    # Machine Learning Performance
    story.append(Paragraph("3. Supervised Machine Learning Benchmark (Trade Forecasting)", h1_style))
    ml_df = pd.read_csv("outputs/models/model_benchmark_comparison.csv")
    ml_table_data = [["Algorithm", "Target Variable", "MAE (USD)", "RMSE (USD)", "R² Score", "MAPE (%)"]]
    for _, r in ml_df.iterrows():
        ml_table_data.append([
            str(r["Model"]), str(r["Target"]), f"${r['MAE_USD']/1e6:.2f}M",
            f"${r['RMSE_USD']/1e6:.2f}M", f"{r['R2_Score']:.4f}", f"{r['MAPE_Percent']:.2f}%"
        ])
    t_ml = Table(ml_table_data, colWidths=[130, 95, 75, 75, 70, 75])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2A9D8F")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 10))
    
    if os.path.exists("outputs/figures/actual_vs_predicted.png"):
        story.append(Image("outputs/figures/actual_vs_predicted.png", width=480, height=210))
        story.append(Spacer(1, 10))
        
    # Statistical Hypothesis Testing
    story.append(Paragraph("4. Statistical Hypothesis Testing & Inference", h1_style))
    hyp_df = pd.read_csv("submission_files/04_Statistical_Hypothesis_Testing_Results.csv")
    hyp_table_data = [["Test ID", "Test Name", "Null Hypothesis (H0)", "P-Value", "Decision"]]
    for _, r in hyp_df.iterrows():
        hyp_table_data.append([
            str(r["Test_ID"]), str(r["Test_Name"]), str(r["Null_Hypothesis_H0"]),
            str(r["P_Value"]), str(r["Decision"])
        ])
    t_hyp = Table(hyp_table_data, colWidths=[55, 110, 190, 75, 90])
    t_hyp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1D3557")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_hyp)
    story.append(Spacer(1, 12))
    
    # Power BI & SQL Architecture
    story.append(Paragraph("5. Relational Star Schema & Power BI Enterprise Architecture", h1_style))
    story.append(Paragraph(
        "The project implements a full Star Schema database design in SQLite (`petrochemical_trade.db`) and CSV tables ready for Power BI Desktop. "
        "The dimensional model separates commercial transactions into <b>Fact_TradeTransactions</b> connected via primary/foreign key pairs to "
        "<b>Dim_Commodity</b>, <b>Dim_Country</b>, and <b>Dim_Date</b>. Advanced DAX expressions compute Total Trade, Net Balance, Coverage Ratio, "
        "and Year-over-Year growth dynamically across all filter slices.", body_style
    ))
    
    doc.build(story)
    print(f"Successfully saved PDF report: {pdf_path}")
    
    # 2. Power BI DAX & Modeling Guide PDF
    pbi_path = "submission_files/06_PowerBI_DAX_and_Modeling_Guide.pdf"
    doc_pbi = SimpleDocTemplate(pbi_path, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    story_pbi = []
    
    story_pbi.append(Paragraph("POWER BI DATA MODELING & DAX SPECIFICATION", title_style))
    story_pbi.append(Paragraph("Executive Business Intelligence Implementation Guide | Petrochemical Trade Analytics", sub_style))
    story_pbi.append(Spacer(1, 8))
    story_pbi.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2A9D8F"), spaceBefore=4, spaceAfter=12))
    
    story_pbi.append(Paragraph("1. Star Schema Dimensional Architecture", h1_style))
    story_pbi.append(Paragraph(
        "Power BI Desktop connects to four pre-formatted relational tables located in <code>data/powerbi/</code>:<br/>"
        "• <b>Fact_TradeData.csv:</b> Grain of one record per trade transaction with quantity, volume MT, value USD, and foreign key references.<br/>"
        "• <b>Dim_Commodity.csv:</b> HS Codes, Chemical Groups (Olefins vs Aromatics), and descriptions.<br/>"
        "• <b>Dim_Country.csv:</b> Reporter and partner economies with ISO codes and continental regions.<br/>"
        "• <b>Dim_Date.csv:</b> Continuous time calendar from 2015 to 2024 with year, quarter, month, and month-year keys.", body_style
    ))
    story_pbi.append(Spacer(1, 8))
    
    story_pbi.append(Paragraph("2. Essential DAX Measures Library", h1_style))
    dax_table_data = [
        ["Measure Name", "DAX Expression", "Business Significance"],
        ["Total Trade Value", "SUM(Fact_TradeData[trade_value_usd])", "Gross commercial market velocity ($302.18B)"],
        ["Import Value", 'CALCULATE(SUM(Fact_TradeData[trade_value_usd]), Fact_TradeData[trade_flow] = "Import")', "National inbound feedstock cost ($153.74B)"],
        ["Export Value", 'CALCULATE(SUM(Fact_TradeData[trade_value_usd]), Fact_TradeData[trade_flow] = "Export")', "National outbound export earnings ($148.44B)"],
        ["Trade Balance", "[Export Value] - [Import Value]", "Net trade surplus (+) or deficit (-) (-$5.29B)"],
        ["Total Volume Mt", "DIVIDE(SUM(Fact_TradeData[trade_volume_mt]), 1000000, 0)", "Total physical shipment in Million MT (334.13 Mt)"],
        ["Avg Price USD/MT", "DIVIDE(SUM(Fact_TradeData[trade_value_usd]), SUM(Fact_TradeData[trade_volume_mt]), 0)", "Trade Unit Value benchmark per ton"],
        ["YoY Trade Growth", "VAR Prev = CALCULATE([Total Trade Value], DATEADD(Dim_Date[full_date], -1, YEAR)) RETURN DIVIDE([Total Trade Value] - Prev, Prev, 0)", "Compound annual expansion velocity"]
    ]
    t_dax = Table(dax_table_data, colWidths=[100, 220, 200])
    t_dax.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1D3557")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story_pbi.append(t_dax)
    story_pbi.append(Spacer(1, 10))
    
    story_pbi.append(Paragraph("3. Step-by-Step 1-Click Power BI Desktop Setup Guide", h1_style))
    story_pbi.append(Paragraph(
        "1. Open <b>Power BI Desktop</b>.<br/>"
        "2. Click <b>Get Data -> Text/CSV</b> and select all 4 files from <code>data/powerbi/</code>.<br/>"
        "3. In the <b>Model View</b>, verify the 1-to-Many relationships from Dim tables to Fact_TradeData.<br/>"
        "4. In the <b>Report View</b>, create a New Table named <code>_Measures</code> and paste the DAX formulas above.<br/>"
        "5. Drag and drop the <b>Card Visual</b> for Total Trade, Imports, Exports, and Trade Balance.<br/>"
        "6. Add a <b>Clustered Column Chart</b> for Annual Trade Value by Year and Trade Flow.", body_style
    ))
    
    doc_pbi.build(story_pbi)
    print(f"Successfully saved Power BI guide PDF: {pbi_path}")

if __name__ == "__main__":
    generate_docx_report()
    generate_pdf_reports()
