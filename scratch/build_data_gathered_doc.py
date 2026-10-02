import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_bw_sample_table(doc, title, headers, data, col_widths=None):
    # Table Title (e.g., "Sample Users Table:")
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(title)
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(12)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    num_rows = len(data) + 1
    num_cols = len(headers)
    tbl = doc.add_table(rows=num_rows, cols=num_cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, color="000000", sz="4")

    # Header Row
    hdr_row = tbl.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        set_cell_background(cell, "FFFFFF")
        set_cell_margins(cell, top=80, bottom=80, left=110, right=110)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(h_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)

    # Data Rows
    for r_idx, row_values in enumerate(data):
        row = tbl.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for c_idx in range(num_cols):
            val = str(row_values[c_idx]) if c_idx < len(row_values) else ""
            cell = row.cells[c_idx]
            set_cell_background(cell, "FFFFFF")
            set_cell_margins(cell, top=70, bottom=70, left=110, right=110)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05

            if len(val) <= 6 or re.match(r'^\d+(\.\d+)?$', val.strip()):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0, 0, 0)

    if col_widths and len(col_widths) == num_cols:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)

def generate_data_gathered_doc(out_docx_path):
    doc = docx.Document()

    # Academic Margins: Left 1.25", Top 1.0", Bottom 1.0", Right 1.0"
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

    # Main Heading
    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(10)
    p_h1.paragraph_format.space_after = Pt(12)
    p_h1.paragraph_format.keep_with_next = True
    r_h1 = p_h1.add_run("3. DATA GATHERING / DATA USED")
    r_h1.font.name = 'Times New Roman'
    r_h1.font.size = Pt(16)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(0, 0, 0)

    # Subheading 3.1
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(8)
    p_h2.paragraph_format.space_after = Pt(6)
    p_h2.paragraph_format.keep_with_next = True
    r_h2 = p_h2.add_run("3.1 Overview of Platform Datasets & Entities")
    r_h2.font.name = 'Times New Roman'
    r_h2.font.size = Pt(14)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(0, 0, 0)

    # Body description
    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_desc.paragraph_format.space_before = Pt(0)
    p_desc.paragraph_format.space_after = Pt(6)
    p_desc.paragraph_format.line_spacing = 1.0
    r_desc = p_desc.add_run(
        "Seva Sankalp is an interactive peer-to-peer resource redistribution web platform. Rather than analyzing static third-party datasets, the application manages multi-tenant relational data models generated by registered community donors, grassroots recipients, and verified charitable NGOs. The core data entities captured, preprocessed, and maintained within the SQLite/PostgreSQL relational database include:"
    )
    r_desc.font.name = 'Times New Roman'
    r_desc.font.size = Pt(12)
    r_desc.font.color.rgb = RGBColor(0, 0, 0)

    # Bullet points matching reference image style
    bullets = [
        ("User Profile Data: ", "Registered accounts, authentication secrets, role permissions, and e-KYC status."),
        ("Resource Data: ", "Physical goods catalog, descriptions, conditions, and spherical GPS coordinates."),
        ("Request Data: ", "Beneficiary donation requests, approval lifecycles, and anti-flipping cooldown logs."),
        ("Statutory NGO Data: ", "Government NITI Aayog Darpan IDs, Organization PAN numbers, and verified UPI VPAs."),
        ("Donation History Data: ", "Audit logs of fulfilled exchanges, mutual ratings, and photographic impact proofs."),
        ("Points Ledger Data: ", "Append-only transactions recording earned and redeemed Karma points."),
        ("Handover Communication Data: ", "In-app secure chat logs coordinating physical item handovers.")
    ]

    for b_lead, b_text in bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.left_indent = Inches(0.35)
        p_b.paragraph_format.space_before = Pt(1)
        p_b.paragraph_format.space_after = Pt(2)
        p_b.paragraph_format.line_spacing = 1.0
        r_lead = p_b.add_run(b_lead)
        r_lead.font.name = 'Times New Roman'
        r_lead.font.size = Pt(12)
        r_lead.font.bold = True
        r_lead.font.color.rgb = RGBColor(0, 0, 0)
        r_t = p_b.add_run(b_text)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(0, 0, 0)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 1. Sample Users Table
    # -------------------------------------------------------------
    t1_headers = ["id", "email", "role", "verification.status", "trust.score", "points.balance", "created.at"]
    t1_data = [
        ["1", "admin@sevasankalp.org", "admin", "approved", "100", "0", "2026-06-08 09:42:09"],
        ["2", "donor@gmail.com", "user", "approved", "48", "350", "2026-06-08 09:42:09"],
        ["3", "receiver@gmail.com", "user", "approved", "25", "100", "2026-06-08 09:42:10"],
        ["4", "anish.sandaka1806@gmail.com", "user", "approved", "85", "450", "2026-06-08 09:56:33"],
        ["5", "srinivas.sandaka75@gmail.com", "user", "approved", "60", "200", "2026-07-05 11:12:10"]
    ]
    add_bw_sample_table(doc, "Sample Users Table:", t1_headers, t1_data, 
                        col_widths=[Inches(0.4), Inches(2.1), Inches(0.65), Inches(1.15), Inches(0.65), Inches(0.65), Inches(1.2)])

    # -------------------------------------------------------------
    # 2. Sample Resources Table
    # -------------------------------------------------------------
    t2_headers = ["id", "donor.id", "title", "category", "condition", "location.lat", "location.lng", "status", "created.at"]
    t2_data = [
        ["1", "4", "rice (1kg)", "Food", "Good", "17.9107", "83.4538", "Available", "2026-07-02 14:58:25"],
        ["2", "5", "NCERT class 10 science", "Books", "Fair", "18.0184", "83.5709", "Available", "2026-07-05 12:19:05"],
        ["3", "4", "wheat flour (1kg)", "Food", "Good", "18.2773", "83.8950", "Available", "2026-07-06 09:50:54"],
        ["4", "2", "Lenovo ThinkPad Laptop", "Electronics", "Good", "18.1067", "83.3978", "Fulfilled", "2026-08-10 10:15:30"]
    ]
    add_bw_sample_table(doc, "Sample Resources Table:", t2_headers, t2_data,
                        col_widths=[Inches(0.35), Inches(0.55), Inches(1.6), Inches(0.8), Inches(0.65), Inches(0.75), Inches(0.75), Inches(0.65), Inches(1.15)])

    # -------------------------------------------------------------
    # 3. Sample Farmer / Beneficiary Requests Table
    # -------------------------------------------------------------
    t3_headers = ["id", "resource.id", "receiver.id", "status", "created.at", "updated.at"]
    t3_data = [
        ["1", "1", "3", "Fulfilled", "2026-07-03 14:30:15", "2026-07-05 11:25:37"],
        ["2", "2", "3", "Fulfilled", "2026-07-05 12:45:00", "2026-07-06 14:20:10"],
        ["3", "4", "5", "Fulfilled", "2026-08-11 09:15:20", "2026-08-14 16:30:45"],
        ["4", "3", "5", "Pending", "2026-08-20 11:00:00", "2026-08-20 11:00:00"]
    ]
    add_bw_sample_table(doc, "Sample Resource Requests Table:", t3_headers, t3_data,
                        col_widths=[Inches(0.4), Inches(0.9), Inches(0.9), Inches(0.85), Inches(1.6), Inches(1.6)])

    # -------------------------------------------------------------
    # 4. Sample Statutory NGO Profiles Table
    # -------------------------------------------------------------
    t4_headers = ["id", "ngo.name", "darpan.id", "org.pan", "upi.id", "verification.status", "created.at"]
    t4_data = [
        ["6", "Global Heart Foundation", "AP/2021/0284910", "AABTG4921E", "globalheart@upi", "approved", "2026-06-28 05:25:14"],
        ["7", "Team Water Welfare Trust", "AP/2022/0319482", "AAATE1234F", "9848294904@ptyes", "approved", "2026-06-29 14:57:00"],
        ["10", "Vidya Jyothi Rural Trust", "DL/2020/0192841", "AAATV9812K", "vidyajyothi@upi", "approved", "2026-08-01 11:15:00"]
    ]
    add_bw_sample_table(doc, "Sample Statutory NGO Profiles Table:", t4_headers, t4_data,
                        col_widths=[Inches(0.35), Inches(1.75), Inches(1.15), Inches(0.8), Inches(1.05), Inches(1.05), Inches(1.1)])

    # -------------------------------------------------------------
    # 5. Sample Donation History Table
    # -------------------------------------------------------------
    t5_headers = ["id", "request.id", "donor.rating", "receiver.rating", "receipt.photo", "impact.message", "completed.at"]
    t5_data = [
        ["1", "1", "5.0", "5.0", "uploads/impact/receipt_1.jpg", "Ration received, helped family during exam week.", "2026-07-05 11:25:37"],
        ["2", "2", "5.0", "4.8", "uploads/impact/receipt_2.jpg", "Received class 10 science textbooks. Thank you!", "2026-07-06 14:20:10"],
        ["3", "3", "5.0", "5.0", "uploads/impact/receipt_3.jpg", "Working laptop received for engineering studies.", "2026-08-14 16:30:45"]
    ]
    add_bw_sample_table(doc, "Sample Donation History Table:", t5_headers, t5_data,
                        col_widths=[Inches(0.35), Inches(0.75), Inches(0.75), Inches(0.8), Inches(1.3), Inches(1.8), Inches(1.1)])

    # -------------------------------------------------------------
    # 6. Sample Points Transaction (Karma Ledger) Table
    # -------------------------------------------------------------
    t6_headers = ["id", "user.id", "amount", "transaction.type", "description", "created.at"]
    t6_data = [
        ["1", "4", "50", "earned_donation", "Fulfilled donation of 1kg rice", "2026-07-05 11:25:37"],
        ["2", "5", "50", "earned_donation", "Fulfilled donation of NCERT textbooks", "2026-07-06 14:20:10"],
        ["3", "2", "50", "earned_donation", "Fulfilled donation of ThinkPad laptop", "2026-08-14 16:30:45"]
    ]
    add_bw_sample_table(doc, "Sample Points Transaction (Karma Ledger) Table:", t6_headers, t6_data,
                        col_widths=[Inches(0.4), Inches(0.65), Inches(0.65), Inches(1.2), Inches(2.15), Inches(1.2)])

    # -------------------------------------------------------------
    # 7. Sample Handover Messages Table
    # -------------------------------------------------------------
    t7_headers = ["id", "request.id", "sender.id", "content", "created.at"]
    t7_data = [
        ["1", "1", "3", "Hello, is this item available for pickup near Pusapatirega?", "2026-07-03 14:31:00"],
        ["2", "1", "4", "Yes, available! Can we meet tomorrow evening at 5 PM?", "2026-07-03 14:35:20"],
        ["3", "1", "3", "Perfect, 5 PM at RTC Complex junction works for me.", "2026-07-03 14:36:10"]
    ]
    add_bw_sample_table(doc, "Sample Handover Messages Table:", t7_headers, t7_data,
                        col_widths=[Inches(0.4), Inches(0.75), Inches(0.75), Inches(3.15), Inches(1.2)])

    # Subheading 3.2
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_before = Pt(14)
    p_p2.paragraph_format.space_after = Pt(6)
    p_p2.paragraph_format.keep_with_next = True
    r_p2 = p_p2.add_run("3.2 Preprocessing and Data Cleaning")
    r_p2.font.name = 'Times New Roman'
    r_p2.font.size = Pt(14)
    r_p2.font.bold = True
    r_p2.font.color.rgb = RGBColor(0, 0, 0)

    preproc_bullets = [
        ("Coordinate Clamping: ", "GPS latitude and longitude pairs submitted through Leaflet map clicks are parsed as 64-bit floating point numbers and validated within real geographical bounds (-90 to +90 and -180 to +180)."),
        ("Image Resizing & EXIF Stripping: ", "Uploaded listing images and impact receipts are downsampled via Pillow (PIL) to maximum 800x800 resolution at 80% JPEG compression, automatically removing embedded GPS EXIF metadata to protect donor home privacy."),
        ("Format Regularization: ", "NITI Aayog NGO Darpan IDs (e.g. DL/2021/0123456) and Organization PAN numbers (10 alphanumeric characters) are converted to uppercase and checked against strict regex patterns prior to persistence.")
    ]

    for p_lead, p_text in preproc_bullets:
        p_pb = doc.add_paragraph(style='List Bullet')
        p_pb.paragraph_format.left_indent = Inches(0.35)
        p_pb.paragraph_format.space_before = Pt(1)
        p_pb.paragraph_format.space_after = Pt(2)
        p_pb.paragraph_format.line_spacing = 1.0
        r_lead = p_pb.add_run(p_lead)
        r_lead.font.name = 'Times New Roman'
        r_lead.font.size = Pt(12)
        r_lead.font.bold = True
        r_lead.font.color.rgb = RGBColor(0, 0, 0)
        r_t = p_pb.add_run(p_text)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(0, 0, 0)

    doc.save(out_docx_path)
    print(f"Successfully generated separate data tables document at: {out_docx_path}")

if __name__ == '__main__':
    target_docx = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Seva_Sankalp_Data_Gathered_Tables.docx"
    brain_docx = r"C:\Users\SANDAKA ANISH NIHAAL\.gemini\antigravity\brain\0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2\Seva_Sankalp_Data_Gathered_Tables.docx"
    generate_data_gathered_doc(target_docx)
    import shutil
    shutil.copy2(target_docx, brain_docx)
    print("Copied to brain artifacts.")
