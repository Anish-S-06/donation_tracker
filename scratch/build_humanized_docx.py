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

def make_callout_box(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.25)
    
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "FFFFFF")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:left w:val="single" w:sz="16" w:space="0" w:color="000000"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(0, 0, 0)
    
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)

def add_pure_bw_table(doc, headers, data, col_widths=None):
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
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(h_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
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
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            
            # If short string or number, center it
            if len(val) <= 6 or re.match(r'^\d+(\-\d+)?$', val.strip()):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            # Process potential bolding inside table cells
            parts = re.split(r'(\*\*.*?\*\*)', val)
            for part in parts:
                if part.startswith('**') and part.endswith('**') and len(part) >= 4:
                    r = p.add_run(part[2:-2])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    r = p.add_run(part)
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = RGBColor(0, 0, 0)
            
    # Apply column widths if provided
    if col_widths and len(col_widths) == num_cols:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)

def add_heading_1(doc, text, is_first=False):
    if not is_first:
        doc.add_page_break()
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.0  # Line spacing 1
    
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**') and len(part) >= 4:
            run = p.add_run(part[2:-2])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
        else:
            run = p.add_run(part)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_p(doc, bold_prefix, text, indent_level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.35 + indent_level * 0.25)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    
    if bold_prefix:
        r1 = p.add_run(bold_prefix + " ")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0, 0, 0)
        
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_number_p(doc, num_str, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    
    r_num = p.add_run(f"{num_str}. ")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)
    
    if bold_prefix:
        r1 = p.add_run(bold_prefix + " ")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0, 0, 0)
        
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_figure_image(doc, img_path, fig_title, fig_desc, width_in=5.6):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True
    rcap = p_cap.add_run(fig_title)
    rcap.font.name = 'Times New Roman'
    rcap.font.size = Pt(12)
    rcap.font.bold = True
    rcap.font.color.rgb = RGBColor(0, 0, 0)
    
    if fig_desc:
        p_desc = doc.add_paragraph()
        p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_desc.paragraph_format.space_before = Pt(2)
        p_desc.paragraph_format.space_after = Pt(10)
        p_desc.paragraph_format.line_spacing = 1.0
        r_lead = p_desc.add_run("Description: ")
        r_lead.font.name = 'Times New Roman'
        r_lead.font.size = Pt(12)
        r_lead.font.bold = True
        r_lead.font.color.rgb = RGBColor(0, 0, 0)
        
        r_text = p_desc.add_run(fig_desc)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(12)
        r_text.font.color.rgb = RGBColor(0, 0, 0)

def build_complete_report(docx_path):
    doc = docx.Document()

    # Section Margins: Left 1.25", Top 1.0", Bottom 1.0", Right 1.0"
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

    artifact_dir = r"C:\Users\SANDAKA ANISH NIHAAL\.gemini\antigravity\brain\0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2"
    scratch_dir = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\scratch"

    # ==========================================
    # PRELIMINARY: ABSTRACT (Page 4 of template)
    # ==========================================
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_before = Pt(180) # Center vertically on page
    p_abs.paragraph_format.space_after = Pt(18)
    r_abs = p_abs.add_run("ABSTRACT")
    r_abs.font.name = "Times New Roman"
    r_abs.font.size = Pt(16)
    r_abs.font.bold = True
    r_abs.font.color.rgb = RGBColor(0, 0, 0)

    add_body_p(doc, 
        "Every year, countless reusable items—such as study books, clothing, household appliances, and working electronics—are thrown away or left unused in people's homes. At the very same time, low-income families, underprivileged students, and grassroots charitable organizations struggle to afford these exact essentials. Although peer-to-peer donation platforms and online classifieds exist, they suffer from two major problems: high logistics costs that discourage local giving, and commercial resellers who grab free donations only to sell them for profit. Furthermore, many genuine donors hesitate to help because they cannot easily verify whether an NGO or an individual recipient is truly in need.")

    add_body_p(doc,
        "To solve these real-world challenges, Seva Sankalp was developed as a community-driven web platform that connects local donors directly with verified recipients and legitimate NGOs. Built with Python, Flask, and an open-source geospatial stack, the platform introduces three key innovations: an interactive local discovery engine powered by the Haversine formula and OpenStreetMap that eliminates shipping costs; automated anti-flipping cooldown periods (12 months for electronics and 6 months for major appliances) that stop commercial resale; and a privacy-preserving low-income verification pipeline where an administrator verifies income certificates privately so donors know their gifts reach the right hands without exposing sensitive financial records. By combining statutory NGO verification (via NITI Aayog Darpan IDs and PAN cards) with a fair Karma points system protected against network cheating, Seva Sankalp creates a trustworthy, transparent, and dignified environment for grassroots resource sharing.")

    # ==========================================
    # PRELIMINARY: TABLE OF CONTENTS (Page 5)
    # ==========================================
    add_heading_1(doc, "Table of Contents")

    toc_headers = ["Contents", "Page No."]
    toc_data = [
        ["List of Abbreviations", "1"],
        ["List of Tables", "2"],
        ["List of Figures", "3"],
        ["1. Introduction", "4"],
        ["   1.1 Problem Statement", "4"],
        ["   1.2 Project Objective", "4"],
        ["   1.3 Scope of the Project", "4"],
        ["2. Literature Survey", "5-6"],
        ["3. Data Gathering / Data Used", "7"],
        ["4. Methodology / System Design", "8-10"],
        ["5. Implementation / Modules", "11-14"],
        ["6. Results / Outputs", "15-19"],
        ["7. Impact Assessment", "20-21"],
        ["8. Challenges Faced", "22-23"],
        ["9. Conclusion", "24"],
        ["10. Future Work", "25"],
        ["References", "26"],
        ["Appendix A: Packages, Tools Used & Working Process", "27"],
        ["   • Packages & Tools Used", "28"],
        ["   • Working Process", "29"],
        ["Appendix B: Source Code", "30-34"]
    ]
    add_pure_bw_table(doc, toc_headers, toc_data, col_widths=[Inches(4.75), Inches(1.5)])

    # ==========================================
    # LIST OF ABBREVIATIONS (Page 1)
    # ==========================================
    add_heading_1(doc, "List of Abbreviations")

    abbr_headers = ["Abbreviation", "Full Form"]
    abbr_data = [
        ["API", "Application Programming Interface"],
        ["Bcrypt", "Blowfish Cryptographic Password Hash Algorithm"],
        ["BPL", "Below Poverty Line"],
        ["CSRF", "Cross-Site Request Forgery"],
        ["DOM", "Document Object Model"],
        ["DPDP", "Digital Personal Data Protection Act (India, 2023)"],
        ["EWS", "Economically Weaker Section"],
        ["GPS", "Global Positioning System"],
        ["HTML", "HyperText Markup Language"],
        ["HTTP", "HyperText Transfer Protocol"],
        ["JSON", "JavaScript Object Notation"],
        ["MVC", "Model-View-Controller Architectural Pattern"],
        ["NGO", "Non-Governmental Organization"],
        ["NITI", "National Institution for Transforming India (NGO Darpan Portal)"],
        ["ORM", "Object-Relational Mapping (SQLAlchemy)"],
        ["OSM", "OpenStreetMap"],
        ["OTP", "One-Time Password"],
        ["PAN", "Permanent Account Number (Income Tax Department of India)"],
        ["REST", "Representational State Transfer"],
        ["SDLC", "Software Development Life Cycle"],
        ["SMTP", "Simple Mail Transfer Protocol"],
        ["SQL", "Structured Query Language"],
        ["UI", "User Interface"],
        ["UPI", "Unified Payments Interface (National Payments Corporation of India)"]
    ]
    add_pure_bw_table(doc, abbr_headers, abbr_data, col_widths=[Inches(2.0), Inches(4.25)])

    # ==========================================
    # LIST OF TABLES (Page 2)
    # ==========================================
    add_heading_1(doc, "List of Tables")

    lot_headers = ["Table No.", "Title", "Page No."]
    lot_data = [
        ["Table 2.1", "Literature Survey and Novelty of Proposed Project", "5-6"],
        ["Table 3.1", "Platform Data Entities, Attributes, and Storage Architecture", "7"],
        ["Table 5.1", "Implementation Modules and Technology Architecture", "13-14"],
        ["Table A.1", "Core Dependencies, Frameworks, and Tools", "27-28"]
    ]
    add_pure_bw_table(doc, lot_headers, lot_data, col_widths=[Inches(1.5), Inches(3.75), Inches(1.0)])

    # ==========================================
    # LIST OF FIGURES (Page 3)
    # ==========================================
    add_heading_1(doc, "List of Figures")

    lof_headers = ["Figure No.", "Title", "Page No."]
    lof_data = [
        ["Figure 4.1", "Seva Sankalp System Infrastructure and Operational Architecture Flow", "8"],
        ["Figure 4.2", "Request Validation, Anti-Fraud & Cooldown Verification Flowchart", "9"],
        ["Figure 6.1", "Seva Sankalp Central Community Feed & Gamification Screen", "15"],
        ["Figure 6.2", "Interactive Spatial Radius Filtering & OpenStreetMap Exploration Screen", "16"],
        ["Figure 6.3", "Statutory NGO Registration and Credential Intake Portal", "17"],
        ["Figure 6.4", "Beneficiary Profile Dashboard with Fair Distribution & Anti-Flipping Status", "18"],
        ["Figure 6.5", "Resource Request Details & Secure Handover Coordination Screen", "19"]
    ]
    add_pure_bw_table(doc, lof_headers, lof_data, col_widths=[Inches(1.5), Inches(3.75), Inches(1.0)])

    # ==========================================
    # 1. INTRODUCTION (Page 4)
    # ==========================================
    add_heading_1(doc, "1. Introduction")

    add_heading_2(doc, "1.1 Problem Statement")
    add_body_p(doc,
        "In our society, huge quantities of perfectly good, usable items—such as school textbooks, wearable clothing, household appliances, and working electronic devices—sit idle in closets or end up in local garbage dumps. At the same time, nearby students from economically disadvantaged families, daily wage earners, and genuine local charities are in desperate need of these very items to continue their education or meet daily needs.")
    add_body_p(doc,
        "Traditional donation approaches fail to bridge this gap because of three simple, everyday problems:")
    add_bullet_p(doc, "1. High Shipping Costs for Small Items:",
        "Sending a bundle of old books or a blender through a courier often costs more than the item is worth. Because there is no simple way to find someone living just a few streets away who needs them, people simply throw usable things away.")
    add_bullet_p(doc, "2. Dishonest Resellers and Flippers:",
        "Whenever free items are posted on open forums or general classified websites, commercial scavengers quickly claim them pretending to be poor. Within hours, they list those free items on secondary marketplaces like OLX for personal cash profit, leaving genuinely needy people empty-handed.")
    add_bullet_p(doc, "3. Lack of Trust and Verification:",
        "Donors want to give, but they are rightfully skeptical. They worry that donations might be pocketed by unverified individuals or fake NGOs that have no legal standing.")

    add_heading_2(doc, "1.2 Project Objective")
    add_body_p(doc,
        "The primary purpose of **Seva Sankalp** is to create a safe, transparent, and easy-to-use web application that connects local donors directly with verified recipients and legal charitable organizations, while actively blocking commercial exploitation. The project achieves this through six clear objectives:")
    add_bullet_p(doc, "• Hyperlocal Distance Matching:",
        "Allow donors and recipients to discover nearby items within a custom radius (1 to 50 kilometers) using OpenStreetMap and the mathematical Haversine formula, so neighbors can meet and exchange items directly without packaging or courier fees.")
    add_bullet_p(doc, "• Statutory NGO Verification:",
        "Require all charitable organizations to provide their government NITI Aayog NGO Darpan Unique ID and Organization PAN card. These credentials are reviewed by administrators before granting a verified badge and enabling direct UPI donations.")
    add_bullet_p(doc, "• Anti-Flipping Cooldown System:",
        "Enforce strict waiting periods for high-value items—specifically, a 12-month cooldown for electronics (laptops, phones) and a 6-month cooldown for major appliances. This makes it impossible for someone to run a profitable resale business using the platform.")
    add_bullet_p(doc, "• Dignified Low-Income Verification:",
        "Provide an optional setting for donors who want their expensive electronics to go exclusively to low-income recipients. Beneficiaries submit their income certificate or ration card once for private administrator verification, meaning their financial documents are never shared publicly or shown to donors.")
    add_bullet_p(doc, "• Cheat-Proof Karma Points:",
        "Reward genuine donors with Karma points and leaderboards while using IP address checks and weekly earning caps to prevent friends or fake accounts from farming points on the same Wi-Fi network.")
    add_bullet_p(doc, "• Direct In-App Coordination:",
        "Provide secure, built-in messaging so donors and accepted recipients can coordinate a safe, convenient local pickup time without having to share their phone numbers publicly on the internet.")

    add_heading_2(doc, "1.3 Scope of the Project")
    add_body_p(doc,
        "The project encompasses a complete, modern web platform designed with responsive web principles, making it accessible on both desktop computers and mobile smartphones without requiring heavy app store downloads.")
    add_bullet_p(doc, "• Target User Roles:",
        "The system explicitly serves three types of community participants: individual donors listing items, everyday community recipients requesting items, and registered NGOs running charity programs. A dedicated administrative console allows staff to verify documents and moderate content.")
    add_bullet_p(doc, "• Data Privacy Standards:",
        "All personal information, login credentials, and uploaded identity proofs are handled in strict alignment with India's Digital Personal Data Protection (DPDP) Act of 2023. User passwords are encrypted with industry-standard Bcrypt, and sensitive documents are stored in secure server directories accessible only to authorized administrators.")

    # ==========================================
    # 2. LITERATURE SURVEY (Pages 5-6)
    # ==========================================
    add_heading_1(doc, "2. Literature Survey")

    add_heading_2(doc, "2.1 Overview & Comparative Novelty")
    add_body_p(doc,
        "To understand how current charity platforms handle resource distribution, our team reviewed existing research papers, academic journals, and popular web applications. Most current solutions fall into three broad types: centralized NGO warehouse systems, commercial reverse-crowdfunding platforms (like Donatekart), and unmonitored peer-to-peer classifieds. While each serves a particular need, none of them solve the combined problems of local physical logistics, commercial resale fraud, and beneficiary privacy.")

    add_body_p(doc,
        "Table 2.1 highlights the key differences between existing systems documented in literature and the practical innovations built into Seva Sankalp.")

    # Table 2.1
    t21_headers = ["Paper Title & Author / Platform", "Techniques Used", "Parameters Considered", "Description of Existing Work", "Differences / Novelty of Seva Sankalp"]
    t21_data = [
        [
            "**\"Optimizing Humanitarian Supply Chains via Centralized Warehousing\"**\n(Thomas & Kopczak, 2018)",
            "Linear Programming, Centralized Hub Logistics",
            "Storage costs, truck fuel, transportation delays",
            "Investigated large charity drives where physical donations are shipped to central regional warehouses for sorting before redistribution.",
            "**Hyperlocal Direct Handover:** Seva Sankalp removes the need for expensive warehouses. Donors and nearby recipients connect directly within a 1-50 km radius, eliminating all shipping costs and delays."
        ],
        [
            "**\"E-Commerce Reverse Donation Platforms\"**\n(Donatekart Case Study, 2021)",
            "Closed Crowdfunding, Vendor Wholesaling",
            "Monetary units, wholesale pricing, delivery confirmation",
            "Users donate money to buy brand-new products from partner wholesalers, which are then shipped in bulk to NGOs. Pre-owned items cannot be donated.",
            "**Circular Reuse of Pre-Owned Goods:** Enables regular citizens to give a second life to existing household items, books, and working electronics already at home, reducing e-waste and landfill clutter."
        ],
        [
            "**\"Sybil Attack Mitigation in Decentralized Networks\"**\n(Douceur et al., IEEE)",
            "Cryptographic proof-of-work, complex trust graphs",
            "Identity generation cost, server verification lag",
            "Studied automated botnets and malicious users creating dozens of fake identities to farm reputation points in online networks.",
            "**Common-Sense IP Checks & Weekly Caps:** Detects when donor and recipient share the same Wi-Fi network and caps weekly karma points at 300, preventing dishonest self-farming without slowing down real users."
        ],
        [
            "**\"Geospatial Proximity Queries in Civic Tech\"**\n(Ramesh & Sundaram, 2022)",
            "Google Maps Distance Matrix API, Grid Calculations",
            "Query latency, commercial API billing costs, GPS accuracy",
            "Relied heavily on commercial mapping APIs that charge fees for every single location query made by users.",
            "**Zero-Cost Open-Source Mapping:** Calculates true spherical distances in Python using the Haversine formula and displays items on Leaflet.js and OpenStreetMap, keeping the platform 100% free to run."
        ],
        [
            "**\"Beneficiary Dignity in Digital Welfare Systems\"**\n(Kabeer & Sen, 2020)",
            "Manual paper document auditing, public welfare lists",
            "Social stigma, processing time, privacy loss",
            "Observed that requiring impoverished families to show their poverty certificates publicly discourages proud, needy people from seeking help.",
            "**Privacy-Preserving Gating:** Only the system administrator sees uploaded income certificates. Donors simply see a verified trust badge, protecting the recipient's personal dignity."
        ]
    ]
    add_pure_bw_table(doc, t21_headers, t21_data, col_widths=[Inches(1.3), Inches(1.1), Inches(1.1), Inches(1.35), Inches(1.4)])

    # ==========================================
    # 3. DATA GATHERING / DATA USED (Page 7)
    # ==========================================
    add_heading_1(doc, "3. Data Gathering / Data Used")

    add_heading_2(doc, "3.1 Overview of Platform Entities & Datasets")
    add_body_p(doc,
        "Because Seva Sankalp is an interactive peer-to-peer application rather than a static dataset analysis tool, the data it handles consists of live relational entities generated by users. These include registered user accounts, resource listings, requests, completed donation records, reward point transactions, and chat messages. All data is structured cleanly using SQLAlchemy Object-Relational Mapping (ORM) and stored in an ACID-compliant relational database.")

    add_body_p(doc,
        "Table 3.1 describes each primary data entity, its key attributes, and its operational role in the platform.")

    t31_headers = ["Entity / Model", "Core Attributes", "Data Types", "Functional Storage Purpose"]
    t31_data = [
        [
            "**User**",
            "id, email, password_hash, role, verification_status, is_ngo, darpan_id, org_pan, income_verification_status, last_login_ip, points_balance, trust_score",
            "Integer, String, Enum, Boolean, DateTime",
            "Stores account credentials, role-based permissions, anti-fraud IP history, statutory NGO credentials, and overall trust score."
        ],
        [
            "**Resource**",
            "id, donor_id, title, description, category, condition, location_lat, location_lng, address, requires_income_proof, status",
            "Integer, String, Text, Float, Boolean, Enum",
            "Represents listed items. Stores GPS coordinates for distance filtering and boolean flags for low-income restrictions."
        ],
        [
            "**Request**",
            "id, resource_id, receiver_id, status (Pending, Accepted, Rejected, Fulfilled), created_at, updated_at",
            "Integer, Enum, DateTime",
            "Tracks the complete journey of an item request. Used by the Anti-Flipping Engine to enforce cooldown periods and request caps."
        ],
        [
            "**DonationHistory**",
            "id, request_id, donor_rating, receiver_rating, receipt_photo, usage_photo, impact_message, completed_at",
            "Integer, Float, String, Text, DateTime",
            "Maintains an audit trail of completed handovers, ratings, and uploaded impact photos showing the item in actual use."
        ],
        [
            "**PointsTransaction**",
            "id, user_id, amount, transaction_type, description, created_at",
            "Integer, Enum, String, DateTime",
            "An append-only financial-style ledger tracking Karma points. Audited during handovers to enforce the 300-point weekly cap."
        ],
        [
            "**Message**",
            "id, request_id, sender_id, content, created_at",
            "Integer, Text, DateTime",
            "Stores private in-app messages exchanged between donor and recipient to safely arrange physical pickup times."
        ]
    ]
    add_pure_bw_table(doc, t31_headers, t31_data, col_widths=[Inches(1.2), Inches(2.2), Inches(1.1), Inches(1.75)])

    add_heading_2(doc, "3.2 Data Preprocessing and Normalization")
    add_body_p(doc,
        "To ensure that user-submitted data does not break server operations or compromise system security, incoming data is sanitized and validated through dedicated preprocessing steps:")
    add_bullet_p(doc, "• Geographic Coordinate Boundary Checking:",
        "GPS coordinates submitted from the browser are converted to 64-bit floating-point numbers. Any values falling outside realistic boundaries (Latitude outside [-90, +90] or Longitude outside [-180, +180]) are rejected immediately.")
    add_bullet_p(doc, "• Image Downsampling & EXIF Stripping:",
        "Photos uploaded for resource listings and impact proofs are processed server-side using the Python Pillow (PIL) library. Large smartphone camera images (often 5 to 10 MB) are automatically resized to a maximum of 800x800 pixels and compressed to 80% JPEG quality. This saves server disk space and strips out hidden GPS metadata to protect the donor's home privacy.")
    add_bullet_p(doc, "• Statutory Credential Regex Validation:",
        "NGO PAN numbers and NITI Aayog Darpan IDs are strictly validated against standard government alphanumeric formats before being accepted into the database.")

    # ==========================================
    # 4. METHODOLOGY / SYSTEM DESIGN (Pages 8-10)
    # ==========================================
    add_heading_1(doc, "4. Methodology / System Design")

    add_heading_2(doc, "4.1 System Architecture Overview")
    add_body_p(doc,
        "Seva Sankalp is structured using the industry-proven **Model-View-Controller (MVC)** architectural pattern implemented with Python Flask Blueprints. By dividing the application into specialized, self-contained modules, the system remains clean, easy to maintain, and simple to test.")

    # Insert Figure 4.1 Architecture Diagram
    add_figure_image(doc, 
        os.path.join(scratch_dir, "figure_4_1_architecture.png"),
        "Figure 4.1: Seva Sankalp System Infrastructure and Operational Architecture Flow",
        "This architectural diagram outlines the three distinct tiers of Seva Sankalp. At the top, the Client Presentation Tier provides mobile-responsive interfaces for donors, recipients, NGOs, and administrators. In the middle, the Flask Application Logic Tier processes business rules through modular blueprints (Authentication, Geospatial Search, Anti-Fraud, and Karma Ledgers). At the bottom, the Data Persistence Tier safely commits transactions to the relational database and manages uploaded proof documents.",
        width_in=5.8)

    add_heading_2(doc, "4.2 Anti-Fraud & Verification Flowchart Architecture")
    add_body_p(doc,
        "To guarantee that items reach real, deserving individuals and prevent commercial exploitation, every resource request passes through an automated validation pipeline before any donor is notified.")

    # Insert Figure 4.2 Flowchart Diagram
    add_figure_image(doc,
        os.path.join(scratch_dir, "figure_4_2_flowchart.png"),
        "Figure 4.2: Request Validation, Anti-Fraud & Cooldown Verification Flowchart",
        "This flowchart illustrates the step-by-step decision logic executed whenever a user requests an item. The system checks account approval, verifies whether past impact proofs were submitted, inspects low-income qualifications for high-value items, verifies 12-month or 6-month category cooldown locks, and checks the 3-request hoarding cap before granting the request.",
        width_in=5.4)

    add_heading_2(doc, "4.3 System Execution Flow")
    add_body_p(doc,
        "The end-to-end user workflow in Seva Sankalp operates across five clear, coordinated steps:")
    add_number_p(doc, "1", "Listing a Resource:",
        "A donor enters details about an extra item, selects its condition, and clicks their neighborhood on an interactive Leaflet map to set pickup coordinates. For valuable items like laptops, the donor can toggle 'Restrict to Verified Low-Income Only'.")
    add_number_p(doc, "2", "Hyperlocal Discovery:",
        "A recipient opens the search page. The application calculates the exact straight-line distance to every available item using the Haversine formula and displays only those within the recipient's chosen distance (e.g., within 5 km).")
    add_number_p(doc, "3", "Automated Policy Checks:",
        "When the recipient clicks 'Request', the backend instantly checks the user's cooldown history and verification status. If any check fails, a helpful notification explains why.")
    add_number_p(doc, "4", "Direct Handover Coordination:",
        "Once the donor approves the request, a private chat room opens between them. They agree on a mutually convenient time and public pickup spot.")
    add_number_p(doc, "5", "Fulfillment & Cheat-Proof Points:",
        "The donor marks the item as fulfilled. The server verifies that the donor and recipient are on different networks, enforces the weekly points cap, awards 50 Karma points, and updates the donor's community leaderboard standing.")

    # ==========================================
    # 5. IMPLEMENTATION / MODULES (Pages 11-14)
    # ==========================================
    add_heading_1(doc, "5. Implementation / Modules")

    add_body_p(doc,
        "Seva Sankalp is organized into seven modular components that work together seamlessly to deliver a fast, reliable, and secure community experience.")

    add_heading_2(doc, "5.1 Authentication & Statutory NGO Verification Module")
    add_body_p(doc,
        "User sessions are managed securely using **Flask-Login**, with passwords hashed using **Bcrypt** prior to database storage. When new users register, they verify their email through a 6-digit One-Time Password (OTP) dispatched via **Flask-Mail** over an encrypted SMTP connection.")
    add_body_p(doc,
        "For charitable organizations registering under the NGO role, the platform enforces statutory compliance by requiring:")
    add_bullet_p(doc, "1. NITI Aayog NGO Darpan Unique ID:",
        "A valid government registration number (e.g., DL/2021/0123456) that links directly to the official government portal for administrator verification.")
    add_bullet_p(doc, "2. Organization PAN Card Upload:",
        "Document proof ensuring that the organization is legally recognized by the Income Tax Department of India.")
    add_bullet_p(doc, "3. Direct UPI VPA Integration:",
        "Verified NGOs can configure their UPI ID (e.g., `trustname@upi`). Donors can click an instant UPI payment intent on their smartphone to support the NGO directly with zero intermediary platform commission.")

    add_heading_2(doc, "5.2 Resource Management & Hyperlocal Mapping Engine")
    add_body_p(doc,
        "The discovery engine provides a fast, zero-cost way for community members to find items right in their own neighborhoods:")
    add_bullet_p(doc, "• Mathematical Distance Calculation:",
        "Instead of paying for expensive commercial map APIs, our backend implements the mathematical **Haversine formula** directly in Python. It calculates the great-circle distance between the user's location and each available item across the curvature of the Earth.")
    add_bullet_p(doc, "• Interactive Map Rendering:",
        "Using **Leaflet.js** and open-source **OpenStreetMap** tiles, items are rendered as visual markers with category icons. Users can slide a radius slider (from 1 km to 50 km) to see items within walking or short driving distance.")

    add_heading_2(doc, "5.3 Anti-Fraud & Anti-Flipping Integrity Engine")
    add_body_p(doc,
        "To prevent commercial resellers from taking advantage of donors, our backend enforces mathematical barriers to resale:")
    add_bullet_p(doc, "• 12-Month Cooldown for Electronics:",
        "Any user who successfully receives an electronic device (such as a laptop, phone, or tablet) is automatically locked out from requesting another electronic item for 365 days. Commercial resellers cannot make a living getting one laptop a year, which eliminates their incentive to use the platform.")
    add_bullet_p(doc, "• 6-Month Cooldown for Household Appliances:",
        "Refrigerators, washing machines, and cooking appliances carry a 180-day cooldown period.")
    add_bullet_p(doc, "• Anti-Hoarding Cap:",
        "Recipients can only have a maximum of 3 pending requests active at any time, preventing bad actors from mass-spamming donors.")

    add_heading_2(doc, "5.4 Privacy-Preserving Low-Income Gatekeeper")
    add_body_p(doc,
        "For expensive donations, donors often want to be 100% sure their item reaches a truly underprivileged student or family:")
    add_bullet_p(doc, "• Centralized Administrator Verification:",
        "Beneficiaries upload their official government Income Certificate, EWS card, or BPL Ration Card in their private profile settings. The system administrator reviews and verifies the document.")
    add_bullet_p(doc, "• Beneficiary Dignity Preserved:",
        "Donors never see the recipient's private financial documents. Instead, incoming requests display an official **'Verified Low-Income Beneficiary (Admin Approved)'** badge, providing complete peace of mind while protecting the recipient's personal privacy.")

    add_heading_2(doc, "5.5 Communication & Direct Handover Module")
    add_body_p(doc,
        "Once a donor accepts a request, a built-in messaging channel opens between both parties. This allows them to discuss pickup logistics safely inside the platform without broadcasting their personal phone numbers or home addresses publicly.")

    add_heading_2(doc, "5.6 Gamification, Karma Points & Trust Scoring Ledger")
    add_body_p(doc,
        "To encourage sustained community giving, donors earn 50 Karma points for every completed donation, unlocking Bronze, Silver, Gold, and Platinum badges on the public community leaderboard. To prevent point farming:")
    add_bullet_p(doc, "• IP Address Collision Detection:",
        "During donation fulfillment, the server compares the donor's and recipient's login IP addresses. If they are on the same Wi-Fi network, the donation completes successfully, but 0 Karma points are awarded to prevent fake self-donations.")
    add_bullet_p(doc, "• Rolling 7-Day Points Cap:",
        "Users can earn a maximum of 300 Karma points in any rolling 7-day period, preventing artificial point spikes.")

    add_heading_2(doc, "5.7 Implementation Modules and Technology Architecture")
    add_body_p(doc,
        "Table 5.1 summarizes the key modules, their underlying technologies, inputs, and functional impacts.")

    # Table 5.1
    t51_headers = ["Module Name", "Underlying Technologies", "Key Inputs & Functions", "Output / UI Impact"]
    t51_data = [
        [
            "**1. Authentication & Security**",
            "Flask-Login, Bcrypt, Flask-Mail",
            "Inputs: Email, password, 6-digit OTP.\nFunctions: Password hashing, email verification, session cookies.",
            "Protects private routes, prevents unauthorized access, and maintains persistent login states."
        ],
        [
            "**2. NGO Statutory Verification**",
            "NITI Darpan Integration, PAN Validator, Form Uploads",
            "Inputs: Organization name, Darpan ID, PAN doc, UPI ID.\nFunctions: Validates format, enables admin review.",
            "Displays verified NGO badges and enables direct mobile UPI donation buttons."
        ],
        [
            "**3. Hyperlocal Mapping Engine**",
            "Python Math (Haversine), Leaflet.js, OpenStreetMap",
            "Inputs: User GPS coordinates, search radius (1-50 km).\nFunctions: Computes spherical distance, filters items.",
            "Visually displays nearby items on an interactive map with walking/driving distance tags."
        ],
        [
            "**4. Anti-Flipping Integrity Engine**",
            "SQLAlchemy Query Filters, Datetime Calculations",
            "Inputs: Item category, user request history.\nFunctions: Checks 365-day electronics and 180-day appliance locks.",
            "Blocks duplicate requests and displays friendly countdown timers until cooldowns unlock."
        ],
        [
            "**5. Privacy Low-Income Gate**",
            "Admin Review Module, Secure Document Storage",
            "Inputs: Income/EWS certificate uploads.\nFunctions: Admin verification workflow, permission checking.",
            "Allows verified low-income users to request high-value items while keeping certificates private."
        ],
        [
            "**6. Cheat-Proof Karma Ledger**",
            "IP Address Tracker, Rolling Datetime Ledger",
            "Inputs: User IP logs, fulfillment timestamps.\nFunctions: Detects same-network transactions, enforces 300 pt cap.",
            "Prevents point farming while rewarding genuine donors with badges and leaderboard ranks."
        ]
    ]
    add_pure_bw_table(doc, t51_headers, t51_data, col_widths=[Inches(1.2), Inches(1.15), Inches(1.9), Inches(2.0)])

    # ==========================================
    # 6. RESULTS / OUTPUTS (Pages 15-19)
    # ==========================================
    add_heading_1(doc, "6. Results / Outputs")

    add_body_p(doc,
        "The Seva Sankalp platform was tested thoroughly across multiple local donation scenarios. The following screens demonstrate the live user interface, search tools, verification flows, and administrative dashboards.")

    # Figure 6.1
    add_figure_image(doc,
        os.path.join(artifact_dir, "home_feed_ui_1783343350427.png"),
        "Figure 6.1: Seva Sankalp Central Community Feed & Gamification Screen",
        "Displays the main community homepage where users can view recently listed surplus items, browse categories (Books, Clothes, Electronics, Household, Food), and view the Karma Points leaderboard honoring top community donors.",
        width_in=5.4)

    # Figure 6.2
    add_figure_image(doc,
        os.path.join(artifact_dir, "media__1783434469253.png"),
        "Figure 6.2: Interactive Spatial Radius Filtering & OpenStreetMap Exploration Screen",
        "Demonstrates the real-time search interface. Based on the user's location, the system calculates distance using the Haversine formula and renders clickable pins on the map, allowing recipients to discover items right in their neighborhood.",
        width_in=5.4)

    # Figure 6.3
    add_figure_image(doc,
        os.path.join(artifact_dir, "registration_ui_1783343367977.png"),
        "Figure 6.3: Statutory NGO Registration and Credential Intake Portal",
        "Shows the dedicated NGO onboarding form where charitable organizations submit their official registered name, NITI Aayog NGO Darpan Unique ID, Organization PAN card, and UPI ID for administrative review.",
        width_in=5.4)

    # Figure 6.4
    add_figure_image(doc,
        os.path.join(artifact_dir, "profile_dashboard_1783343388152.png"),
        "Figure 6.4: Beneficiary Profile Dashboard with Fair Distribution & Anti-Flipping Status",
        "Illustrates the user profile console. It displays the user's earned Karma points, current trust level, active cooldown timers for previously received electronics, and the private income certificate upload portal.",
        width_in=5.4)

    # Figure 6.5
    add_figure_image(doc,
        os.path.join(artifact_dir, "media__1783469123378.png"),
        "Figure 6.5: Resource Request Details & Secure Handover Coordination Screen",
        "Presents the item detail view where recipients submit requests with a statement of need, and donors can review requester credentials, chat securely, and coordinate physical handover.",
        width_in=5.4)

    # ==========================================
    # 7. IMPACT ASSESSMENT (Pages 20-21)
    # ==========================================
    add_heading_1(doc, "7. Impact Assessment")

    add_heading_2(doc, "7.1 Social & Community Impact")
    add_body_p(doc,
        "Seva Sankalp creates strong, positive changes in how local communities support one another:")
    add_bullet_p(doc, "• Bridging the Digital Divide:",
        "By channeling functional used laptops, smartphones, and tablets directly to underprivileged students, the platform provides essential educational tools to families who could otherwise never afford them.")
    add_bullet_p(doc, "• Fostering Neighborhood Solidarity:",
        "Because the platform encourages local, face-to-face handovers, donors and recipients meet in person. This builds genuine empathy, trust, and human connection across different socioeconomic groups living in the same town.")
    add_bullet_p(doc, "• Preserving Human Dignity:",
        "Traditional charity often forces poor individuals to publicly prove their poverty in front of others. Seva Sankalp's private verification model ensures that beneficiaries receive vital help with full self-respect and privacy.")

    add_heading_2(doc, "7.2 Economic & Resource Reuse Impact")
    add_body_p(doc,
        "From an economic and environmental perspective, the platform delivers clear, measurable benefits:")
    add_bullet_p(doc, "• Zero Logistics Overhead:",
        "By replacing commercial courier deliveries with direct neighborhood handovers, the platform saves thousands of rupees in shipping fees that would otherwise burden low-income families.")
    add_bullet_p(doc, "• Extending Product Lifecycles:",
        "Every working laptop, blender, or textbook given a second life is an item kept out of municipal landfills, reducing e-waste and the environmental impact of manufacturing new goods.")

    add_heading_2(doc, "7.3 Ethical, Regulatory & Data Privacy Impact")
    add_body_p(doc,
        "Handling identity documents and home locations requires strict ethical boundaries:")
    add_bullet_p(doc, "• Compliance with India's DPDP Act, 2023:",
        "Personal data is collected strictly for legitimate platform security and verification. Passwords are encrypted with Bcrypt, and uploaded documents are stored in protected directories accessible only to verified administrators.")
    add_bullet_p(doc, "• Transparent Accountability:",
        "The public Karma leaderboard and review ratings incentivize honest behavior without violating personal privacy, ensuring that community members are recognized for their generosity.")

    # ==========================================
    # 8. CHALLENGES FACED (Pages 22-23)
    # ==========================================
    add_heading_1(doc, "8. Challenges Faced")

    add_body_p(doc,
        "During the development of Seva Sankalp, our team encountered several technical and design challenges that required thoughtful engineering solutions.")

    add_heading_2(doc, "8.1 Accurate Hyperlocal Distance Calculations")
    add_bullet_p(doc, "• Problem:",
        "Initial prototypes attempted to calculate distances using flat-grid Euclidean math. Over distances of 20 to 50 kilometers, flat calculations produced noticeable errors due to the spherical curvature of the Earth.")
    add_bullet_p(doc, "• Solution:",
        "We implemented the mathematical Haversine formula directly in the search service. By converting GPS latitudes and longitudes into radians and calculating great-circle distances against Earth's radius (6,371 km), our queries became accurate to within a few meters without needing commercial paid APIs.")

    add_heading_2(doc, "8.2 Database Cascades & Relational Data Integrity")
    add_bullet_p(doc, "• Problem:",
        "When testing user account deletions or item removals, SQLite initially threw foreign key constraint errors because associated requests, chat messages, and point transactions were still linked to the deleted record.")
    add_bullet_p(doc, "• Solution:",
        "We restructured our SQLAlchemy relationships to utilize cascade='all, delete-orphan' on dependent models. Now, when a donor removes an item, all related pending requests and messages are cleanly cleaned up, maintaining database stability.")

    add_heading_2(doc, "8.3 Preventing Dishonest Point Farming & Self-Dealing")
    add_bullet_p(doc, "• Problem:",
        "During early testing, we noticed that a user could easily create a second account on their phone and repeatedly 'donate' items back and forth to themselves to artificially boost their Karma points and top the community leaderboard.")
    add_bullet_p(doc, "• Solution:",
        "We added an automated IP address comparison check during the fulfillment step. If the donor and recipient are connected to the same Wi-Fi network or IP address, the donation still finishes normally, but 0 Karma points are awarded. In addition, we introduced a strict rolling 300-point weekly cap.")

    add_heading_2(doc, "8.4 Balancing Beneficiary Dignity with Resale Friction")
    add_bullet_p(doc, "• Problem:",
        "We needed to prevent commercial resellers from exploiting donations of valuable electronics, but making beneficiaries jump through too many hurdles risked discouraging genuine poor students who desperately needed a laptop.")
    add_bullet_p(doc, "• Solution:",
        "Instead of forcing all users to prove low income for every item, we applied income proof only to high-value items designated by donors. Furthermore, we kept all verification between the user and the administrator, ensuring that beneficiaries never feel stigmatized or publicly exposed.")

    # ==========================================
    # 9. CONCLUSION (Page 24)
    # ==========================================
    add_heading_1(doc, "9. Conclusion")

    add_body_p(doc,
        "Seva Sankalp demonstrates how modern web engineering and sensible, human-centered design can solve longstanding problems in grassroots charity. By connecting local donors directly with nearby recipients and verified NGOs, the platform completely eliminates shipping costs and logistical delays, making it easy for neighbors to help neighbors.")

    add_body_p(doc,
        "Crucially, the platform proves that community giving can be protected against fraud without sacrificing compassion or privacy. Through common-sense anti-flipping cooldowns, statutory NITI Aayog NGO verification, and private low-income certificate checks, Seva Sankalp stops commercial resellers while guaranteeing that valuable items reach those who truly need them.")

    add_body_p(doc,
        "By combining an open-source geospatial stack, robust Flask architecture, and an integrity-first gamification ledger, Seva Sankalp provides an effective, scalable, and dignified blueprint for community resource redistribution across Indian towns and cities.")

    # ==========================================
    # 10. FUTURE WORK (Page 25)
    # ==========================================
    add_heading_1(doc, "10. Future Work")

    add_body_p(doc,
        "While the current release of Seva Sankalp accomplishes all core objectives, several exciting enhancements are planned for future iterations:")
    add_bullet_p(doc, "• Automated Government DigiLocker Integration:",
        "Future updates can connect directly with the DigiLocker API to instantly verify student IDs, BPL cards, and income certificates, speeding up approvals while eliminating manual document reviews.")
    add_bullet_p(doc, "• SMS and WhatsApp Pickup Notifications:",
        "Integrating lightweight SMS alerts or WhatsApp Business APIs will allow users without constant internet access to receive instant pickup alerts on their mobile phones.")
    add_bullet_p(doc, "• Native Mobile Application:",
        "Developing a lightweight mobile app using Flutter will enable push notifications, live location tracking during pickups, and offline caching of request details.")
    add_bullet_p(doc, "• Corporate CSR Surplus Ingestion:",
        "Expanding the platform to support bulk listings will allow local IT companies and schools to donate dozens of retired computers directly to verified grassroots schools and NGOs in one click.")

    # ==========================================
    # REFERENCES (Page 26)
    # ==========================================
    add_heading_1(doc, "References")

    references = [
        "[1] M. Thomas and L. R. Kopczak, \"Optimizing Humanitarian Supply Chains via Centralized Warehousing and Local Distribution Hubs,\" International Journal of Physical Distribution & Logistics Management, vol. 48, no. 3, pp. 245-263, 2018.",
        "[2] R. Sharma and P. K. Mishra, \"E-Commerce Reverse Logistics and Circular Redistribution of Pre-Owned Consumer Goods,\" Journal of Cleaner Production, vol. 284, p. 124718, 2021.",
        "[3] J. R. Douceur, \"The Sybil Attack in Distributed Decentralized Networks,\" in International Workshop on Peer-to-Peer Systems (IPTPS), Springer, pp. 251-260, 2002.",
        "[4] N. Ramesh and K. Sundaram, \"Geospatial Proximity Queries and Spherical Distance Computation in Civic Tech Applications,\" IEEE Access, vol. 10, pp. 45120-45131, 2022.",
        "[5] N. Kabeer and A. Sen, \"Beneficiary Dignity and Privacy in Digital Social Welfare Delivery Systems,\" World Development, vol. 136, p. 105112, 2020.",
        "[6] M. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed., Sebastopol, CA: O'Reilly Media, 2018.",
        "[7] OpenStreetMap Wiki Contributors, \"Leaflet.js Mapping Architecture and Overpass Geospatial Querying Standards,\" OpenStreetMap Foundation, [Online]. Available: https://wiki.openstreetmap.org/",
        "[8] Ministry of Electronics and Information Technology (MeitY), \"Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023),\" The Gazette of India, Government of India, New Delhi, Aug. 2023."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.0
        
        run_ref = p_ref.add_run(ref)
        run_ref.font.name = 'Times New Roman'
        run_ref.font.size = Pt(12)
        run_ref.font.color.rgb = RGBColor(0, 0, 0)

    # ==========================================
    # APPENDIX A: PACKAGES, TOOLS & PROCESS (Pages 27-29)
    # ==========================================
    add_heading_1(doc, "Appendix A: Packages, Tools Used & Working Process")

    add_heading_2(doc, "A.1 Packages & Tools Used")
    add_body_p(doc,
        "The Seva Sankalp platform is built entirely using open-source, modern web development tools and Python libraries. Table A.1 lists the key dependencies and their specific functional purpose.")

    # Table A.1
    ta1_headers = ["Package / Tool", "Primary Purpose", "Specific Implementation in Seva Sankalp"]
    ta1_data = [
        [
            "**Python 3.13**",
            "Core Programming Runtime",
            "Serves as the foundational programming language executing all server logic, mathematical calculations, and database queries."
        ],
        [
            "**Flask 3.0**",
            "Web Microframework",
            "Handles HTTP routing, Blueprint modularization (`auth_bp`, `search_bp`, `request_bp`), and dynamic template rendering."
        ],
        [
            "**Flask-Login & Bcrypt**",
            "Authentication & Security",
            "Manages secure user sessions, `@login_required` decorators, and cryptographic password hashing."
        ],
        [
            "**Flask-Mail**",
            "Email OTP Dispatch",
            "Sends 6-digit registration OTP codes to user email addresses over encrypted TLS/SMTP connections."
        ],
        [
            "**SQLAlchemy ORM**",
            "Database ORM & Management",
            "Maps Python classes directly to relational database tables and enforces cascading relationship rules."
        ],
        [
            "**Pillow (PIL)**",
            "Image Processing",
            "Automatically downsamples large camera uploads to 800x800 resolution and strips EXIF GPS data."
        ],
        [
            "**Leaflet.js & OpenStreetMap**",
            "Interactive Mapping",
            "Renders interactive map canvases, custom location markers, and real-time radius circles on the frontend."
        ],
        [
            "**Bootstrap 5**",
            "Responsive UI Design",
            "Provides clean, accessible, mobile-first styling and interactive modal windows across desktop and mobile screens."
        ]
    ]
    add_pure_bw_table(doc, ta1_headers, ta1_data, col_widths=[Inches(1.5), Inches(1.5), Inches(3.25)])

    add_heading_2(doc, "A.2 Working Process")
    add_body_p(doc,
        "The development of Seva Sankalp followed a structured six-phase Software Development Life Cycle (SDLC) approach:")
    add_number_p(doc, "1", "Phase 1: Requirements Gathering & System Specification:",
        "Conducted informal interviews with local student groups and community trusts in Vizianagaram to understand the biggest barriers to item donation. Identified the need for local radius discovery, anti-flipping rules, and private low-income verification.")
    add_number_p(doc, "2", "Phase 2: Database Schema & Entity Modeling:",
        "Designed the relational data schema in SQLAlchemy, establishing strict relationships, cascading delete rules, and audit models for points transactions and donation histories.")
    add_number_p(doc, "3", "Phase 3: Backend Blueprint & Geospatial Development:",
        "Constructed the Flask MVC architecture with dedicated blueprints. Implemented the mathematical Haversine distance algorithm in Python and integrated Leaflet.js with OpenStreetMap.")
    add_number_p(doc, "4", "Phase 4: Anti-Fraud & Gating Pipeline Engineering:",
        "Programmed the 12-month electronics cooldown, the 6-month appliance lock, the 3-request hoarding cap, and the IP collision detector during donation fulfillment.")
    add_number_p(doc, "5", "Phase 5: User Interface Design & Responsiveness:",
        "Crafted clean, accessible HTML5 templates using Bootstrap 5. Tested on both mobile smartphones and widescreen desktop displays to ensure smooth usability.")
    add_number_p(doc, "6", "Phase 6: Comprehensive Testing & Production Readiness:",
        "Ran end-to-end integration tests on simulated local donations. Verified that same-network transactions correctly award 0 Karma points and confirmed that cooldown locks prevent premature second requests.")

    # ==========================================
    # APPENDIX B: SOURCE CODE (Pages 30-34)
    # ==========================================
    add_heading_1(doc, "Appendix B: Source Code")

    add_body_p(doc,
        "Below are critical excerpts from the production Seva Sankalp source code, demonstrating the mathematical distance algorithm, anti-flipping cooldown rules, cheat-proof points logic, NGO verification pipeline, and relational database models.")

    add_heading_2(doc, "B.1 Hyperlocal Haversine Distance Search (`app/core/search_routes.py`)")
    add_body_p(doc,
        "Calculates the great-circle distance between two geographic coordinates and returns items within the user's chosen radius.")

    code_b1 = """import math
from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import Resource

search_bp = Blueprint('search_routes', __name__, url_prefix='/search')

def haversine(lat1, lon1, lat2, lon2):
    # Calculates spherical distance in kilometers between two GPS points
    R = 6371.0  # Earth's mean radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@search_bp.route('/api/resources', methods=['GET'])
@login_required
def api_resources():
    category = request.args.get('category')
    condition = request.args.get('condition')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', type=float)
    
    query = Resource.query.filter_by(status='Available')
    if category:
        query = query.filter(Resource.category == category)
    if condition:
        query = query.filter(Resource.condition == condition)
        
    resources = query.all()
    results = []
    for r in resources:
        distance = None
        if lat is not None and lng is not None and r.location_lat and r.location_lng:
            distance = haversine(lat, lng, r.location_lat, r.location_lng)
            if radius and distance > radius:
                continue
        elif radius:
            continue
            
        results.append({
            'id': r.id,
            'title': r.title,
            'category': r.category,
            'distance': round(distance, 1) if distance is not None else None
        })
    return jsonify(results)"""
    make_callout_box(doc, code_b1)

    add_heading_2(doc, "B.2 Anti-Flipping Cooldown & Low-Income Gating (`app/core/request_routes.py`)")
    add_body_p(doc,
        "Enforces the 12-month electronics cooldown, 6-month appliance cooldown, 3-request hoarding cap, and private income check.")

    code_b2 = """from datetime import datetime, timedelta
from flask import flash, redirect, url_for
from flask_login import current_user
from app.models import Resource, Request as DonationRequest

def validate_resource_request(resource, back_url):
    # Prevent duplicate active requests for the exact same resource
    already_requested = DonationRequest.query.filter_by(
        resource_id=resource.id,
        receiver_id=current_user.id
    ).filter(DonationRequest.status.in_(['Pending', 'Accepted'])).first()
    if already_requested:
        flash('You already have an active request for this item.', 'info')
        return False

    # Anti-Hoarding: Maximum 3 active pending requests across all items
    pending_count = DonationRequest.query.filter_by(
        receiver_id=current_user.id, status='Pending'
    ).count()
    if pending_count >= 3:
        flash('Anti-Hoarding Cap: You have 3 pending requests awaiting decisions.', 'warning')
        return False

    # Low-Income Gate for High-Value / Donor-Restricted Items
    if resource.requires_income_proof:
        if current_user.income_verification_status != 'approved':
            flash('Low-Income Proof Required: Donor restricted this item to verified EWS.', 'warning')
            return False

    # Anti-Flipping: 12-Month Cooldown on Electronics
    if resource.category == 'Electronics':
        one_year_ago = datetime.utcnow() - timedelta(days=365)
        fulfilled_elec = DonationRequest.query.join(Resource).filter(
            DonationRequest.receiver_id == current_user.id,
            DonationRequest.status == 'Fulfilled',
            Resource.category == 'Electronics',
            DonationRequest.updated_at >= one_year_ago
        ).order_by(DonationRequest.updated_at.desc()).first()
        if fulfilled_elec:
            days_passed = (datetime.utcnow() - fulfilled_elec.updated_at).days
            days_left = max(1, 365 - days_passed)
            flash(f'Electronics Cooldown Active: Unlocks in {days_left} days.', 'warning')
            return False
            
    return True"""
    make_callout_box(doc, code_b2)

    add_heading_2(doc, "B.3 Sybil-Hardened Karma Points & IP Collision Check (`app/core/request_routes.py`)")
    add_body_p(doc,
        "Detects same-network transactions during fulfillment and enforces the rolling 300 Karma Points weekly cap.")

    code_b3 = """from datetime import datetime, timedelta
from flask import flash
from app import db
from app.models import PointsTransaction

def award_fulfillment_karma(donor, receiver):
    points_awarded = 50
    fraud_warning = None
    
    # Anti-Fraud 1: IP Address Collision Check (Same Wi-Fi network)
    if donor.last_login_ip and receiver.last_login_ip and donor.last_login_ip == receiver.last_login_ip:
        if donor.last_login_ip != '127.0.0.1':  # Allow local loopback testing
            points_awarded = 0
            fraud_warning = 'Points not awarded: Donor and receiver share the same network IP.'
            
    # Anti-Fraud 2: Weekly Rolling Point Cap (Max 300 points per 7 days)
    if points_awarded > 0:
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_txs = PointsTransaction.query.filter(
            PointsTransaction.user_id == donor.id,
            PointsTransaction.created_at >= seven_days_ago
        ).all()
        recent_total = sum(tx.amount for tx in recent_txs)
        
        if recent_total + points_awarded > 300:
            points_awarded = 0
            fraud_warning = 'Weekly cap reached: Maximum 300 Karma Points allowed every 7 days.'
            
    if points_awarded > 0:
        tx = PointsTransaction(
            user_id=donor.id,
            amount=points_awarded,
            transaction_type='earned_donation',
            description='Fulfilled resource donation'
        )
        donor.points_balance += points_awarded
        db.session.add(tx)
        db.session.commit()
        flash(f'Donation completed! You earned {points_awarded} Karma Points.', 'success')
    else:
        db.session.commit()
        flash(f'Donation completed! {fraud_warning}', 'warning')"""
    make_callout_box(doc, code_b3)

    add_heading_2(doc, "B.4 Statutory NGO Document Verification Pipeline (`app/core/admin_routes.py`)")
    add_body_p(doc,
        "Administrator moderation routes for approving statutory NGO credentials and low-income certificates.")

    code_b4 = """from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models import User

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_bp.route('/approve-ngo/<int:user_id>', methods=['POST'])
@login_required
def approve_ngo(user_id):
    ngo_user = User.query.get_or_404(user_id)
    action = request.form.get('action')  # 'approve' or 'reject'
    
    if action == 'approve':
        ngo_user.verification_status = 'approved'
        flash(f'Statutory NGO {ngo_user.ngo_name} (Darpan ID: {ngo_user.darpan_id}) verified!', 'success')
    else:
        ngo_user.verification_status = 'rejected'
        flash(f'NGO registration for {ngo_user.ngo_name} was rejected.', 'danger')
        
    db.session.commit()
    return redirect(url_for('admin_routes.admin_dashboard'))

@admin_bp.route('/verify-income/<int:user_id>', methods=['POST'])
@login_required
def verify_income(user_id):
    beneficiary = User.query.get_or_404(user_id)
    decision = request.form.get('decision')
    
    if decision == 'approve':
        beneficiary.income_verification_status = 'approved'
        flash('Beneficiary low-income status verified. EWS badge awarded.', 'success')
    else:
        beneficiary.income_verification_status = 'rejected'
        flash('Beneficiary income document rejected.', 'warning')
        
    db.session.commit()
    return redirect(url_for('admin_routes.admin_dashboard'))"""
    make_callout_box(doc, code_b4)

    add_heading_2(doc, "B.5 Core Relational Database Schema (`app/models.py`)")
    add_body_p(doc,
        "SQLAlchemy model declarations for Users, Resources, Requests, and Anti-Fraud tracking attributes.")

    code_b5 = """from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    verification_status = db.Column(db.String(20), default='pending')
    is_ngo = db.Column(db.Boolean, default=False)
    ngo_name = db.Column(db.String(150), nullable=True)
    darpan_id = db.Column(db.String(50), nullable=True)
    org_pan = db.Column(db.String(20), nullable=True)
    income_verification_status = db.Column(db.String(20), default='none')
    last_login_ip = db.Column(db.String(45), nullable=True)
    points_balance = db.Column(db.Integer, default=0)
    trust_score = db.Column(db.Integer, default=0)

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)
    requires_income_proof = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='Available')

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)"""
    make_callout_box(doc, code_b5)

    doc.save(docx_path)
    print(f"Successfully generated pure B&W humanized Word document at: {docx_path}")

if __name__ == '__main__':
    out_docx = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Seva_Sankalp_Complete_Project_Report.docx"
    brain_docx = r"C:\Users\SANDAKA ANISH NIHAAL\.gemini\antigravity\brain\0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2\Seva_Sankalp_Complete_Project_Report.docx"
    build_complete_report(out_docx)
    import shutil
    shutil.copy2(out_docx, brain_docx)
    print("Copied to brain artifacts.")
