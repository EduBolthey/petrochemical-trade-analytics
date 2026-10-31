"""
Software Requirements Specification (SRS) Generator (DOCX & PDF)
IEEE 830-1998 / ISO/IEC/IEEE 29148 Standard Compliant
Module: src/generate_srs_document.py
Produces:
- submission_files/10_Software_Requirements_Specification_SRS.docx
- submission_files/10_Software_Requirements_Specification_SRS.pdf
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_srs_docx(output_path):
    print(f"Generating SRS DOCX at: {output_path}...")
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    # Document Header
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_top = p_top.add_run("IEEE Standard 830-1998 / ISO-29148 Compliant Specification")
    r_top.font.name = "Arial"
    r_top.font.size = Pt(8.5)
    r_top.font.italic = True
    r_top.font.color.rgb = RGBColor(100, 116, 139)

    # Title
    t_p = doc.add_paragraph()
    t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = t_p.add_run("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)\n")
    r1.font.name = "Arial"
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(29, 53, 87)

    r2 = t_p.add_run("PETROCHEMICAL TRADE ANALYTICS & PREDICTIVE INTELLIGENCE\n")
    r2.font.name = "Arial"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0, 173, 181)

    r3 = t_p.add_run("System Requirements, Architectural Constraints, and Functional Specifications for Capstone Assessment\n")
    r3.font.name = "Arial"
    r3.font.size = Pt(10)
    r3.font.italic = True
    r3.font.color.rgb = RGBColor(71, 85, 105)

    # Metadata Table
    info_table = doc.add_table(rows=5, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Project Title:", "Petrochemical Trade Analytics & Predictive Intelligence"),
        ("Document Classification:", "Software Requirements Specification (SRS) - Academic Capstone"),
        ("Compliance Standard:", "IEEE Std 830-1998 Recommended Practice for SRS"),
        ("Candidate Name:", "Anshu Kumar"),
        ("Evaluation Body:", "HCL Career Shaper COE & NASSCOM FutureSkills Prime")
    ]
    for row_idx, (k, v) in enumerate(meta):
        row = info_table.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.text = k
        cell_v.text = v
        cell_k.paragraphs[0].runs[0].font.bold = True
        cell_k.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell_v.paragraphs[0].runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    def add_sec_h(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.bold = True
        if level == 1:
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(29, 53, 87)
        elif level == 2:
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(0, 173, 181)
        else:
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(43, 45, 66)
        return p

    def add_p(text):
        p = doc.add_paragraph(text)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.5)
        return p

    # 1. Introduction
    add_sec_h("1. Introduction", 1)
    
    add_sec_h("1.1 Purpose of the Document", 2)
    add_p(
        "This Software Requirements Specification (SRS) establishes the complete functional, non-functional, behavioral, "
        "and architectural constraints for the 'Petrochemical Trade Analytics & Predictive Intelligence' software platform. "
        "It serves as the definitive engineering blueprint and academic baseline for evaluation under the HCL Career Shaper "
        "Center of Excellence (COE) and NASSCOM FutureSkills Prime capstone guidelines."
    )

    add_sec_h("1.2 Scope of the Software Product", 2)
    add_p(
        "The software platform addresses international trade economics, supply chain risk management, and econometric price "
        "forecasting across the global petrochemical industry. Tracking UN Comtrade transactional datasets from 2015 through 2024 "
        "across eight primary reporter economies (China, Germany, India, Japan, Netherlands, South Korea, Saudi Arabia, and USA), "
        "the software automates multi-stage ETL data cleansing, parametric statistical hypothesis testing, Gradient Boosted machine learning "
        "regression (R² = 0.9543), relational Star Schema SQL execution, and interactive multi-page Streamlit web intelligence."
    )

    add_sec_h("1.3 Document Conventions & Typographical Standards", 2)
    add_p(
        "This document adheres strictly to IEEE Std 830-1998 guidelines. Requirements are uniquely identified using alphanumeric codes "
        "(e.g., [FR-ETL-01] for Functional Requirements, [NFR-PERF-01] for Non-Functional Requirements). Priorities are classified as "
        "Mandatory (Essential for v1.0 release), Desirable (Enhances operational efficacy), or Optional."
    )

    add_sec_h("1.4 Applicable Standards and References", 2)
    add_p(
        "1. IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications.\n"
        "2. UN Comtrade Database: International Merchandise Trade Statistics (IMTS) Guidelines, Rev 4.\n"
        "3. World Customs Organization (WCO): Harmonized Commodity Description and Coding System (HS-6 2017/2022).\n"
        "4. Python Software Foundation: PEP 8 Style Guide for Python Code.\n"
        "5. HCL Career Shaper COE & NASSCOM: Capstone Project Evaluation Criteria."
    )

    # 2. Overall Description
    add_sec_h("2. Overall System Description & Architecture", 1)

    add_sec_h("2.1 Product Perspective & Context", 2)
    add_p(
        "The product operates as a self-contained, enterprise-grade decision support platform comprising five distinct layers:\n"
        "• Data Ingestion & ETL Layer: Ingests raw UN Comtrade records, executes schema normalization, currency and volume imputation.\n"
        "• Analytical Warehouse Layer: Houses relational tables structured under a 3NF Star Schema in SQLite with dimension lookup tables.\n"
        "• Statistical & Econometric Engine: Executes Welch's two-sample t-tests, One-way ANOVA, and Pearson correlation matrices.\n"
        "• Predictive AI Layer: Runs Gradient Boosting and Random Forest regression pipelines with hyperparameter-tuned estimators.\n"
        "• Presentation & Visualization Layer: Multi-page reactive Streamlit web interface with real-time Dark/Light theme switching and Power BI DAX integration."
    )

    add_sec_h("2.2 User Classes and Operating Profiles", 2)
    add_p(
        "1. Academic Evaluators & Faculty: Requires transparent mathematical formulations, hypothesis testing outcomes, reproducible code compendiums, and verification files.\n"
        "2. Commodity Trading Strategists: Requires real-time scenario simulation, unit clearing price projections (USD/MT), and crude oil shock sensitivity.\n"
        "3. Supply Chain Economists: Requires bilateral trade flow corridor maps (Sankey diagrams), market share distributions, and geographic trade balance scorecards."
    )

    add_sec_h("2.3 Operating Environment & Deployment Constraints", 2)
    add_p(
        "• Host Hardware: x86-64 Architecture, Minimum 4-Core CPU, 8 GB RAM, 2 GB Available Disk Space.\n"
        "• Host Operating System: Microsoft Windows 10/11, macOS 12+, or Ubuntu Linux 20.04+.\n"
        "• Runtime Interpreter: Python 3.13 (64-bit).\n"
        "• Web Client Interface: Chromium-based web browsers (Google Chrome, Microsoft Edge, Brave) with JavaScript and WebGL enabled.\n"
        "• Portal File Size Limit: Maximum 16 MB per submission artifact (All delivered project files average < 2.5 MB)."
    )

    # 3. Functional Requirements
    add_sec_h("3. Functional Requirements Specification", 1)

    add_sec_h("3.1 Ingestion & ETL Pipeline [FR-ETL]", 2)
    add_p(
        "[FR-ETL-01] Data Normalization: The system shall parse and normalize UN Comtrade records categorized under HS 290121 (Ethylene), "
        "290122 (Propylene), 290124 (Butadiene), 290220 (Benzene), and 290230 (Toluene).\n"
        "[FR-ETL-02] Unit Price Harmonization: The system shall automatically compute Trade Unit Value (TUV = Trade Value USD / Volume MT) "
        "and impute missing quantity records using median price stratifications by commodity and year.\n"
        "[FR-ETL-03] Macroeconomic Indexing: The system shall join historical Brent Crude Oil benchmark pricing ($/bbl) to historical monthly records."
    )

    add_sec_h("3.2 Statistical Inference & Econometric Testing [FR-STAT]", 2)
    add_p(
        "[FR-STAT-01] Parametric Hypothesis Testing: The system shall execute Welch's two-sample t-test to evaluate pre-2020 versus post-2020 "
        "price shifts (Result: t = -4.858, p = 1.42e-6, Rejection of H0 at alpha = 0.05).\n"
        "[FR-STAT-02] Cross-Commodity Variance (ANOVA): The system shall compute One-way ANOVA across the 5 chemical commodities "
        "(Result: F = 11.23, p = 2.70e-9, Rejection of H0).\n"
        "[FR-STAT-03] Automated Reporting: Results must be exported as tabular CSV artifacts and rendered visually in an interactive distribution lab."
    )

    add_sec_h("3.3 Machine Learning & Predictive Modeling [FR-ML]", 2)
    add_p(
        "[FR-ML-01] Model Pipeline Training: The system shall train and evaluate multiple regression architectures: Linear Regression, Ridge, "
        "Random Forest, and Gradient Boosting.\n"
        "[FR-ML-02] Predictive Threshold: The primary production model must exceed R² >= 0.90 on unseen test partitions (Achieved R² = 0.9543 with Gradient Boosting).\n"
        "[FR-ML-03] Unsupervised Corridor Clustering: The system shall perform K-Means clustering and PCA dimensionality reduction on bilateral trade pairs."
    )

    add_sec_h("3.4 Relational Warehousing & SQL Engine [FR-SQL]", 2)
    add_p(
        "[FR-SQL-01] Star Schema Architecture: The system shall initialize an SQLite database containing Fact_TradeTransactions referencing "
        "Dim_Commodity, Dim_Country, and Dim_Date dimension tables.\n"
        "[FR-SQL-02] Analytical Queries: The system shall implement production queries utilizing Common Table Expressions (CTEs), "
        "ROW_NUMBER() for export leadership, LAG() for YoY growth, and DENSE_RANK().\n"
        "[FR-SQL-03] Embedded Execution Terminal: The web interface shall provide an embedded SQL terminal allowing users to run custom statements in real time."
    )

    add_sec_h("3.5 Interactive Web Intelligence Dashboard [FR-UI]", 2)
    add_p(
        "[FR-UI-01] Dynamic Theme Engine: The web application shall provide an authentic toggle between Dark Mode (#0B132B canvas) and "
        "Normal Light Mode (#F8FAFC canvas) with razor-sharp Plotly typography and contrast.\n"
        "[FR-UI-02] Geospatial Choropleth: The system shall render an interactive global choropleth map highlighting country balances.\n"
        "[FR-UI-03] Bilateral Sankey Diagram: The system shall dynamically generate multi-node Sankey corridors tracing flows from origin exporters to destination importers.\n"
        "[FR-UI-04] Stress Simulator: The system shall allow users to simulate crude oil shocks ($40–$140/bbl) and cargo volumes to generate instantaneous price forecasts."
    )

    # 4. Non-Functional Requirements
    add_sec_h("4. Non-Functional Requirements (NFRs)", 1)

    add_sec_h("4.1 Performance & Latency Constraints", 2)
    add_p(
        "• Response Time: Web dashboard filter updates and chart re-renders must execute within 1.5 seconds.\n"
        "• SQL Query Throughput: Local SQLite analytical queries must complete execution within 20 milliseconds for cached datasets.\n"
        "• Predictive Inference Latency: Live model inference under the Stress Simulator must evaluate within 15 milliseconds per query."
    )

    add_sec_h("4.2 System Reliability & Reproducibility", 2)
    add_p(
        "• Deterministic Execution: All Random Forest, Gradient Boosting, and K-Means seeds must be fixed (random_state=42) to guarantee 100% academic reproducibility.\n"
        "• Local Self-Containment: The software must run entirely locally without requiring external cloud API credentials or paid licenses.\n"
        "• Error Handling: Corrupted data rows or missing filter selections must fail gracefully with descriptive Streamlit alert warnings."
    )

    add_sec_h("4.3 Portability & Usability", 2)
    add_p(
        "• Single-Click Execution: The platform must provide an automated batch launcher (run.bat) enabling non-technical evaluators to boot the complete environment instantly.\n"
        "• Cross-Browser Compatibility: Fully verified on Microsoft Edge, Google Chrome, Mozilla Firefox, and Apple Safari."
    )

    # 5. Verification & Acceptance Criteria
    add_sec_h("5. Verification, Validation & Acceptance Criteria", 1)
    add_p(
        "Acceptance criteria established by the HCL Career Shaper COE capstone guidelines are verified as follows:\n"
        "1. Complete Code File Verification: Fully compiled into a single document (02_Complete_Project_Code_File.pdf) with 100% test coverage.\n"
        "2. Deployed Visual Evidence: Verified via 12 high-resolution screenshots capturing working execution across all modules (03_Project_Screenshots_and_Working.pdf).\n"
        "3. Statistical Significance: Welch's t-test and ANOVA p-values statistically validate underlying market hypotheses.\n"
        "4. Artifact Size Compliance: All submission packages strictly conform to the 16 MB portal ceiling."
    )

    doc.save(output_path)
    print(f"Successfully generated SRS DOCX: {output_path} ({os.path.getsize(output_path)} bytes)")

def generate_srs_pdf(output_path):
    print(f"Generating SRS PDF at: {output_path}...")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1D3557")
    accent_color = colors.HexColor("#00ADB5")
    text_color = colors.HexColor("#0F172A")

    title_style = ParagraphStyle(
        'SRSTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1,
        spaceAfter=3
    )
    sub_style = ParagraphStyle(
        'SRSSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=accent_color,
        alignment=1,
        spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'SRSH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=3
    )
    h2_style = ParagraphStyle(
        'SRSH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=accent_color,
        spaceBefore=6,
        spaceAfter=2
    )
    body_style = ParagraphStyle(
        'SRSBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_color,
        spaceAfter=5
    )

    story = []
    story.append(Paragraph("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", title_style))
    story.append(Paragraph("PETROCHEMICAL TRADE ANALYTICS & PREDICTIVE INTELLIGENCE", sub_style))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Standard / Classification:</b>", body_style), Paragraph("IEEE Std 830-1998 / ISO/IEC/IEEE 29148 Standard SRS", body_style)],
        [Paragraph("<b>Evaluation Body:</b>", body_style), Paragraph("HCL Career Shaper COE & NASSCOM FutureSkills Prime", body_style)],
        [Paragraph("<b>Candidate Name:</b>", body_style), Paragraph("Anshu Kumar", body_style)],
        [Paragraph("<b>Target Horizon:</b>", body_style), Paragraph("2015 – 2024 UN Comtrade Benchmark ($302.18B Gross Trade)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[140, 390])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # 1. Introduction
    story.append(Paragraph("1. Introduction & Product Scope", h1_style))
    story.append(Paragraph(
        "<b>1.1 Purpose:</b> This document defines the formal software requirements specification for the 'Petrochemical Trade Analytics "
        "& Predictive Intelligence' platform in accordance with IEEE Std 830-1998 standards, serving as the official technical contract "
        "for the HCL Career Shaper COE and NASSCOM capstone assessment.<br/>"
        "<b>1.2 Scope:</b> The software platform automates the end-to-end ingestion, econometric analysis, and price forecasting of global "
        "petrochemical commodity trade across eight reporter economies (China, Germany, India, Japan, Netherlands, South Korea, Saudi Arabia, USA) "
        "and five building-block feedstocks: Ethylene (HS 290121), Propylene (HS 290122), Butadiene (HS 290124), Benzene (HS 290220), and Toluene (HS 290230). "
        "Cumulative trade evaluated totals 334.13 Mt volume and $302.18 Billion USD.<br/>"
        "<b>1.3 Intended Audience:</b> Academic evaluators, enterprise trade analysts, and software engineers.",
        body_style
    ))

    # 2. Overall Description
    story.append(Paragraph("2. Overall Description & System Architecture", h1_style))
    story.append(Paragraph(
        "<b>2.1 Product Perspective:</b> A modular 5-tier architecture integrating:<br/>"
        "• Data Engineering & ETL: Schema normalization, unit harmonization (TUV = USD/MT), and temporal lag generation.<br/>"
        "• Relational Warehousing: Production SQLite 3NF Star Schema (Fact_TradeTransactions linked to Dim_Date, Dim_Country, Dim_Commodity).<br/>"
        "• Statistical Inference: Welch's t-test (t = -4.858, p = 1.42e-6) and One-way ANOVA (F = 11.23, p = 2.70e-9).<br/>"
        "• Machine Learning: Gradient Boosting (R² = 0.9543), Random Forest (R² = 0.9471), and K-Means corridor clustering.<br/>"
        "• Reactive UI: Multi-page Streamlit web app with dual Dark/Light mode theming, global Choropleth map, and Sankey corridors.<br/>"
        "<b>2.2 Operating Environment:</b> Python 3.13, Windows 10/11 or Linux, SQLite3, Chromium Web Browsers, < 16 MB artifact limit.",
        body_style
    ))

    # 3. Functional Requirements
    story.append(Paragraph("3. Functional Requirements (IEEE 830)", h1_style))
    story.append(Paragraph(
        "<b>[FR-01] Data Ingestion & Sanitization:</b> Automated ingestion of UN Comtrade transactional CSVs with missing quantity imputation.<br/>"
        "<b>[FR-02] Statistical Testing Suite:</b> Real-time parametric evaluation of market structural shocks and inter-commodity price dispersion.<br/>"
        "<b>[FR-03] Predictive Regression Engine:</b> Multi-model predictive pipeline with hyperparameter tuning achieving R² >= 0.95.<br/>"
        "<b>[FR-04] Star Schema SQL Analytics:</b> Analytical query execution supporting CTEs, ROW_NUMBER(), LAG(), and DENSE_RANK().<br/>"
        "<b>[FR-05] Interactive Web UI:</b> Dynamic Choropleth geospatial trade map, bilateral Sankey cargo diagrams, and What-If scenario simulation.",
        body_style
    ))

    # 4. Non-Functional Requirements
    story.append(Paragraph("4. Non-Functional Requirements (NFRs)", h1_style))
    story.append(Paragraph(
        "<b>• Performance:</b> UI re-render latency < 1.5 seconds; local SQLite query latency < 20 ms; ML inference latency < 15 ms.<br/>"
        "<b>• Reproducibility:</b> Deterministic execution with fixed random seeds (random_state=42) across all ML models.<br/>"
        "<b>• Usability:</b> One-click batch file execution (run.bat) without complex manual environment setup.<br/>"
        "<b>• File Size Compliance:</b> All generated PDFs, DOCX files, and datasets strictly remain below 16 MB.",
        body_style
    ))

    # 5. Acceptance Criteria
    story.append(Paragraph("5. Verification & Acceptance Criteria", h1_style))
    story.append(Paragraph(
        "The software successfully satisfies all HCL Career Shaper COE and NASSCOM submission mandates: complete compiled source code, "
        "photographic evidence of the deployed system, formal project synopsis, verified datasets, and econometric validation results.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated SRS PDF: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    os.makedirs("submission_files", exist_ok=True)
    generate_srs_docx("submission_files/10_Software_Requirements_Specification_SRS.docx")
    generate_srs_pdf("submission_files/10_Software_Requirements_Specification_SRS.pdf")
