"""
Complete Project Source Code Document Generator (DOCX & PDF)
Module: src/generate_code_document.py
Compiles all codebase modules into a single, beautifully formatted, indexed academic code file.
Produces:
- submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.docx
- submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.pdf
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

CODE_FILES = [
    {
        "category": "1. Data Engineering & ETL Pipeline",
        "path": "src/etl/generate_dataset.py",
        "description": "UN Comtrade benchmark dataset generator and macroeconomic feature synthesizer."
    },
    {
        "category": "1. Data Engineering & ETL Pipeline",
        "path": "src/etl/clean_data.py",
        "description": "Data cleaning, schema normalization, outlier filtering, and TUV imputation."
    },
    {
        "category": "1. Data Engineering & ETL Pipeline",
        "path": "src/etl/aggregate_data.py",
        "description": "Multidimensional trade aggregation across annual, quarterly, and country matrices."
    },
    {
        "category": "1. Data Engineering & ETL Pipeline",
        "path": "src/etl/feature_engineering.py",
        "description": "Time-series lag engineering, rolling averages, and Brent crude price indexation."
    },
    {
        "category": "1. Data Engineering & ETL Pipeline",
        "path": "src/etl/train_test_split.py",
        "description": "Chronological train/test dataset partitioner with stratified feature scaling."
    },
    {
        "category": "2. Statistical Inference & Econometric Testing",
        "path": "src/stats/descriptive_stats.py",
        "description": "Parametric descriptive statistics, skewness, kurtosis, and correlation matrices."
    },
    {
        "category": "2. Statistical Inference & Econometric Testing",
        "path": "src/stats/hypothesis_testing.py",
        "description": "Econometric hypothesis testing suite (Welch's t-test, One-way ANOVA, Pearson elasticity)."
    },
    {
        "category": "3. Machine Learning & Predictive Modeling",
        "path": "src/ml/train_models.py",
        "description": "Supervised model training (Gradient Boosting, Random Forest, Ridge, Linear Regression) & evaluation."
    },
    {
        "category": "3. Machine Learning & Predictive Modeling",
        "path": "src/ml/unsupervised_clustering.py",
        "description": "Unsupervised K-Means bilateral trade clustering and Principal Component Analysis (PCA)."
    },
    {
        "category": "3. Machine Learning & Predictive Modeling",
        "path": "src/ml/generate_visualizations.py",
        "description": "Publication-grade Matplotlib & Seaborn econometric visual analytics generation."
    },
    {
        "category": "4. Big Data Distributed Architecture",
        "path": "src/bigdata/pyspark_pipeline.py",
        "description": "PySpark distributed big data processing pipeline for multi-million row trade data."
    },
    {
        "category": "5. Relational Database & Star Schema SQL",
        "path": "database/schema.sql",
        "description": "DDL Schema definition for Star-Schema Fact and Dimension tables."
    },
    {
        "category": "5. Relational Database & Star Schema SQL",
        "path": "database/setup_database.py",
        "description": "Database initialization, dimension extraction, and fact table population script."
    },
    {
        "category": "5. Relational Database & Star Schema SQL",
        "path": "database/analytical_queries.sql",
        "description": "Advanced analytical SQL queries with CTEs, ROW_NUMBER, LAG, and DENSE_RANK."
    },
    {
        "category": "6. Interactive Web Dashboard UI",
        "path": "app.py",
        "description": "Streamlit enterprise command center with live Dark/Light theming, Choropleth map, and Sankey."
    },
    {
        "category": "7. Automation & Deployment Manifests",
        "path": "requirements.txt",
        "description": "Project dependencies and frozen library specifications."
    },
    {
        "category": "7. Automation & Deployment Manifests",
        "path": "run.bat",
        "description": "One-click local execution batch launcher."
    }
]

def generate_code_docx(output_path):
    print(f"Generating Complete Code DOCX at: {output_path}...")
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Cover Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = title_p.add_run("PETROCHEMICAL TRADE ANALYTICS\n")
    r1.font.name = "Arial"
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(29, 53, 87)

    r2 = title_p.add_run("COMPREHENSIVE PROJECT SOURCE CODE COMPENDIUM\n")
    r2.font.name = "Arial"
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0, 173, 181)

    r3 = title_p.add_run("Complete End-to-End Codebase: ETL, Statistics, Machine Learning, Big Data, SQL, and Streamlit UI\n")
    r3.font.name = "Arial"
    r3.font.size = Pt(10)
    r3.font.italic = True
    r3.font.color.rgb = RGBColor(100, 116, 139)

    # Info Box Table
    info_table = doc.add_table(rows=5, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Program / Submission:", "HCL Career Shaper COE & NASSCOM FutureSkills Prime"),
        ("Project Title:", "Petrochemical Trade Analytics & Predictive Intelligence"),
        ("Author / Candidate:", "[Student Full Name] | ID: [Student Roll / LMS ID]"),
        ("Total Code Files:", f"{len(CODE_FILES)} Source Code Modules"),
        ("Submission Deadline:", "1st November 2026, 6:00 PM")
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

    # Table of Contents
    toc_h = doc.add_paragraph()
    r_toc = toc_h.add_run("TABLE OF CONTENTS - CODE MODULES")
    r_toc.font.name = "Arial"
    r_toc.font.size = Pt(14)
    r_toc.font.bold = True
    r_toc.font.color.rgb = RGBColor(29, 53, 87)

    toc_table = doc.add_table(rows=len(CODE_FILES) + 1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = toc_table.rows[0]
    hdr.cells[0].text = "#"
    hdr.cells[1].text = "Source File & Path"
    hdr.cells[2].text = "Functional Scope"
    for c in hdr.cells:
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)

    for i, item in enumerate(CODE_FILES):
        row = toc_table.rows[i + 1]
        row.cells[0].text = str(i + 1)
        row.cells[1].text = item["path"]
        row.cells[2].text = item["description"]
        for c in row.cells:
            c.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_page_break()

    # Append each code file
    for i, item in enumerate(CODE_FILES):
        path = item["path"]
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            code_content = f.read()

        line_count = len(code_content.splitlines())

        # Section Header
        sh = doc.add_paragraph()
        sh.paragraph_format.space_before = Pt(14)
        sh.paragraph_format.space_after = Pt(2)
        r_sh = sh.add_run(f"Module {i+1}: {path}")
        r_sh.font.name = "Arial"
        r_sh.font.size = Pt(12)
        r_sh.font.bold = True
        r_sh.font.color.rgb = RGBColor(29, 53, 87)

        # Meta Header
        mh = doc.add_paragraph()
        mh.paragraph_format.space_after = Pt(6)
        r_mh = mh.add_run(f"Category: {item['category']} | Scope: {item['description']} | Lines: {line_count}")
        r_mh.font.name = "Arial"
        r_mh.font.size = Pt(8.5)
        r_mh.font.italic = True
        r_mh.font.color.rgb = RGBColor(71, 85, 105)

        # Code Block Table
        code_table = doc.add_table(rows=1, cols=1)
        code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = code_table.rows[0].cells[0]
        
        # Style cell background
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
        cell._tc.get_or_add_tcPr().append(shd)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(2)
        cp.paragraph_format.space_after = Pt(2)
        cp.paragraph_format.line_spacing = 1.0

        # Truncate overly massive lines if any, otherwise write line by line
        for line_num, line in enumerate(code_content.splitlines(), start=1):
            if line_num > 1:
                cp = cell.add_paragraph()
                cp.paragraph_format.space_before = Pt(0)
                cp.paragraph_format.space_after = Pt(0)
                cp.paragraph_format.line_spacing = 1.0

            run_num = cp.add_run(f"{line_num:4d}  ")
            run_num.font.name = "Consolas"
            run_num.font.size = Pt(7.5)
            run_num.font.color.rgb = RGBColor(148, 163, 184)

            run_code = cp.add_run(line)
            run_code.font.name = "Consolas"
            run_code.font.size = Pt(7.5)
            run_code.font.color.rgb = RGBColor(15, 23, 42)

        doc.add_paragraph().paragraph_format.space_after = Pt(12)

    doc.save(output_path)
    print(f"Successfully generated Complete Code DOCX: {output_path} ({os.path.getsize(output_path)} bytes)")

def generate_code_pdf(output_path):
    print(f"Generating Complete Code PDF at: {output_path}...")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1D3557")
    accent_color = colors.HexColor("#00ADB5")
    text_color = colors.HexColor("#0F172A")

    title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1,
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        'CodeSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        alignment=1,
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'CodeH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=2
    )
    desc_style = ParagraphStyle(
        'CodeDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#475569"),
        spaceAfter=4
    )
    code_style = ParagraphStyle(
        'CodeFont',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=text_color
    )

    story = []
    story.append(Paragraph("PETROCHEMICAL TRADE ANALYTICS", title_style))
    story.append(Paragraph("COMPREHENSIVE PROJECT SOURCE CODE COMPENDIUM", sub_style))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Curriculum Track:</b>", desc_style), Paragraph("HCL Career Shaper COE & NASSCOM FutureSkills Prime", desc_style)],
        [Paragraph("<b>Author / Candidate:</b>", desc_style), Paragraph("[Student Full Name] | ID: [Student Roll / LMS ID]", desc_style)],
        [Paragraph("<b>Scope & Modules:</b>", desc_style), Paragraph(f"Complete End-to-End Codebase ({len(CODE_FILES)} Source Files)", desc_style)],
        [Paragraph("<b>Submission Date:</b>", desc_style), Paragraph("1st November 2026, 6:00 PM", desc_style)]
    ]
    t = Table(meta_data, colWidths=[120, 420])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    for i, item in enumerate(CODE_FILES):
        path = item["path"]
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        story.append(Paragraph(f"Module {i+1}: {path}", h2_style))
        story.append(Paragraph(f"Category: {item['category']} | Scope: {item['description']} | Total Lines: {len(lines)}", desc_style))

        # In ReportLab, Preformatted can split across pages when not nested in a single table cell
        clean_lines = []
        for l_idx, line in enumerate(lines, start=1):
            clean_l = line.replace("\t", "    ").rstrip("\r\n")
            if len(clean_l) > 105:
                clean_l = clean_l[:105] + "..."
            clean_lines.append(f"{l_idx:4d} | {clean_l}")

        # Chunk into blocks of 50 lines so Preformatted flows naturally across pages
        chunk_size = 50
        for c_idx in range(0, len(clean_lines), chunk_size):
            chunk_text = "\n".join(clean_lines[c_idx:c_idx + chunk_size])
            p_code = Preformatted(chunk_text, code_style)
            story.append(p_code)

        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"Successfully generated Complete Code PDF: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    os.makedirs("submission_files", exist_ok=True)
    generate_code_docx("submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.docx")
    generate_code_pdf("submission_files/02_Petrochemical_Trade_Analytics_Complete_Code_File.pdf")
