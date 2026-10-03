import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_tech_stack_doc():
    doc = Document()

    # Set margins to 0.65 inch for clean 3-page density
    for s in doc.sections:
        s.top_margin = Inches(0.65)
        s.bottom_margin = Inches(0.65)
        s.left_margin = Inches(0.7)
        s.right_margin = Inches(0.7)

        # Header & Footer
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("SEVA SANKALP — End-to-End Technology Stack & Feature Architecture")
        hrun.font.name = 'Times New Roman'; hrun.font.size = Pt(8.5); hrun.font.color.rgb = RGBColor(120, 120, 120)

        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Page ")
        frun.font.name = 'Times New Roman'; frun.font.size = Pt(8.5); frun.font.color.rgb = RGBColor(100, 100, 100)
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(fldSimple)
        frun2 = fp.add_run(" of 3 | MVGR College of Engineering (Autonomous)")
        frun2.font.name = 'Times New Roman'; frun2.font.size = Pt(8.5); frun2.font.color.rgb = RGBColor(120, 120, 120)

    def set_cell_margins(cell, top=45, bottom=45, left=65, right=65):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_table_borders(table, color="D0D5DD", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text.upper())
        r.font.name = 'Times New Roman'; r.font.size = Pt(11.5); r.font.bold = True
        r.font.color.rgb = RGBColor(16, 44, 87)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'; r.font.size = Pt(10.0); r.font.bold = True
        r.font.color.rgb = RGBColor(30, 70, 120)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(0.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.08
        
        r_sym = p.add_run("▪ ")
        r_sym.font.name = 'Arial'; r_sym.font.size = Pt(8.5); r_sym.font.bold = True
        r_sym.font.color.rgb = RGBColor(16, 44, 87)
        
        if bold_prefix:
            prefix_clean = bold_prefix.lstrip("•▪- ").strip()
            r_b = p.add_run(prefix_clean + " ")
            r_b.font.name = 'Times New Roman'; r_b.font.size = Pt(9.5); r_b.font.bold = True
            r_b.font.color.rgb = RGBColor(20, 20, 20)
            
        r_t = p.add_run(text)
        r_t.font.name = 'Times New Roman'; r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_table(headers, rows, col_widths=None, font_size=8.5):
        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        set_table_borders(tbl, color="BDC3C7", sz="4")
        
        hdr = tbl.rows[0]
        trPr = hdr._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for idx, text in enumerate(headers):
            cell = hdr.cells[idx]
            if col_widths and idx < len(col_widths):
                cell.width = col_widths[idx]
            set_cell_background(cell, "102C57")
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = 'Times New Roman'; r.font.size = Pt(font_size); r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
        for r_idx, r_data in enumerate(rows):
            row = tbl.rows[r_idx + 1]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            bg_col = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(r_data):
                cell = row.cells[c_idx]
                if col_widths and c_idx < len(col_widths):
                    cell.width = col_widths[c_idx]
                set_cell_background(cell, bg_col)
                set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx != 0 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.space_before = Pt(0.5)
                p.paragraph_format.space_after = Pt(0.5)
                r = p.add_run(str(val))
                r.font.name = 'Times New Roman'; r.font.size = Pt(font_size)
                r.font.color.rgb = RGBColor(30, 30, 30)
                
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(1)
        p_sp.paragraph_format.space_after = Pt(2)

    # -------------------------------------------------------------
    # DOCUMENT HEADER
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(1)
    r = p_title.add_run("SEVA SANKALP — END-TO-END TECH STACK & FEATURE SPECIFICATION")
    r.font.name = 'Times New Roman'; r.font.size = Pt(14); r.font.bold = True
    r.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("Comprehensive Technical Notes on Frontend, Backend, Database, Security & Feature Implementations")
    r_sub.font.name = 'Times New Roman'; r_sub.font.size = Pt(9.5); r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(70, 70, 70)

    # Meta banner
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(6)
    r_m = p_meta.add_run("B.Tech CSE Project Review Dossier | MVGR College of Engineering (Autonomous) | Python 3.10+ & Flask Architecture")
    r_m.font.name = 'Times New Roman'; r_m.font.size = Pt(8.5); r_m.font.bold = True
    r_m.font.color.rgb = RGBColor(100, 100, 100)

    # -------------------------------------------------------------
    # 1. CORE PROGRAMMING LANGUAGES & RUNTIMES
    # -------------------------------------------------------------
    add_h1("1. Core Programming Languages & Operating Runtimes")
    add_bullet("Python (Version 3.10+ / 3.13):", "Primary backend programming language. Executes business logic, mathematically computes Haversine distances (`math`), calculates sliding-window cooldowns (`datetime`), enforces statutory regex pattern checks (`re`), and interacts with the ORM layer.")
    add_bullet("JavaScript (ECMAScript 2020 / ES6+):", "Primary client-side scripting language. Powers asynchronous Fetch API requests (NGO likes, in-app messaging, dynamic map filtering), client-side coordinate acquisition (`navigator.geolocation`), and DOM mutations without page reloads.")
    add_bullet("HTML5 (HyperText Markup Language 5):", "Defines the semantic structure of the presentation tier, including form controls, microdata, canvas/SVG rendering hooks, and accessible UI hierarchies across mobile and desktop viewports.")
    add_bullet("CSS3 (Cascading Style Sheets 3):", "Provides responsive layout orchestration using CSS Grid and Flexbox, custom properties (`--bg-primary`, `--accent`), keyframe transitions, and a flash-free dark/light mode engine.")
    add_bullet("SQL (Structured Query Language):", "Underlying query language compiled dynamically by SQLAlchemy ORM to manage relational schema integrity, indexed table lookups, and transactional ACID commits.")

    # -------------------------------------------------------------
    # 2. FRONTEND ENGINEERING STACK & FEATURE IMPLEMENTATION
    # -------------------------------------------------------------
    add_h1("2. Frontend Engineering Stack & Feature Mapping")
    
    fe_headers = ["Frontend Technology", "Version / Spec", "Platform Features Powered", "Technical Role & Implementation Detail"]
    fe_rows = [
        ["HTML5 & Semantic Web", "W3C Recommendation", "All Web Pages & Forms", "Provides accessible document structure, native form validation (`required`, `pattern`), multi-part image upload inputs, and accessibility (WAI-ARIA)."],
        ["CSS3 & Theme Variables", "CSS3 Standards", "Global Styling & Theme Toggle", "Implements dynamic CSS custom properties for instant dark/light mode switching (`[data-theme='dark']`) stored in `localStorage`, eliminating visual flickering."],
        ["Bootstrap", "v5.3.2 (CDN)", "Responsive Grid & Modals", "Delivers 12-column responsive layout, interactive modal dialogs (DigiLocker verification, document viewers), alert banners, and mobile navigation toggles."],
        ["Leaflet.js", "v1.9.4 (Open Source)", "Interactive Community Map", "Lightweight client GIS engine (42 KB). Binds to HTML div `#map`, computes viewport tile coordinates $(x,y,z)$, and plots custom interactive SVG resource pins."],
        ["OpenStreetMap (OSM)", "Carto Tile Layer", "Geospatial Tile Rendering", "Serves free raster map imagery via `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`; eliminates commercial Google Maps API billing and tracking."],
        ["FontAwesome", "v6.4.0 (SVG/Font)", "Iconography & Visual Cues", "Renders scalable vector icons including community heart (`fa-heart`), location pins, verified NGO badges, trust stars, and status indicators."],
        ["Vanilla JavaScript (ES6+)", "Native Browser Engine", "AJAX Likes, Chat & Search", "Executes asynchronous `fetch()` API calls with CSRF token headers, handles dynamic radius slider input events, and performs optimistic UI DOM updates."]
    ]
    add_table(fe_headers, fe_rows, [Inches(1.5), Inches(1.05), Inches(1.75), Inches(2.7)], font_size=8.0)

    # -------------------------------------------------------------
    # 3. BACKEND ENGINEERING STACK & FEATURE IMPLEMENTATION
    # -------------------------------------------------------------
    add_h1("3. Backend Engineering Stack & Feature Mapping")

    be_headers = ["Backend Technology", "Version / Spec", "Platform Features Powered", "Technical Role & Implementation Detail"]
    be_rows = [
        ["Flask (WSGI Framework)", "v3.0.x (Python)", "Core Web Application Engine", "Implements Application Factory Pattern (`create_app()`) and 8 modular Blueprints (`auth`, `resource`, `request`, `search`, `profile`, `admin`, `points`, `history`)."],
        ["Jinja2 Templating Engine", "v3.1.x", "Server-Side Rendering (SSR)", "Compiles dynamic HTML templates with context dictionaries, provides template inheritance (`base.html`), and enforces automatic context-aware XSS auto-escaping."],
        ["SQLAlchemy (ORM)", "v2.0.x", "Data Persistence & Models", "Maps Python classes to database tables (`User`, `Resource`, `Request`, `NGOLike`), generates parameterized queries (SQLi immune), and enforces cascading deletes."],
        ["Flask-Login", "v0.6.x", "User Session State Machine", "Manages user login state, session cookies (`HttpOnly`, `SameSite=Lax`), user loader callbacks (`@login_manager.user_loader`), and `@login_required` route guards."],
        ["Bcrypt", "v4.x (Blowfish)", "Password Hashing & Auth", "Applies Blowfish cipher key expansion with 128-bit random salt (`bcrypt.gensalt()`) and cost factor 12 ($2^{12} = 4,096$ rounds) for GPU-proof password security."],
        ["Flask-WTF / CSRFProtect", "v1.2.x", "Form & POST Security", "Injects signed HMAC-SHA256 tokens into all POST forms; validates session token matches request token, stopping Cross-Site Request Forgery."],
        ["Werkzeug Toolkit", "v3.0.x", "WSGI Dispatching & Uploads", "Handles HTTP request dispatching, file stream buffering, and uses `secure_filename()` to sanitize uploaded image/document paths against directory traversal."],
        ["Python Standard Library", "Python 3.10+", "Math, Cooldown & Security", "`math`: Computes Haversine spherical trigonometric distance.\n`datetime`: Enforces 365d/180d cooldowns & 7-day velocity caps.\n`re`: Validates statutory Darpan ID & PAN regex."]
    ]
    add_table(be_headers, be_rows, [Inches(1.5), Inches(1.05), Inches(1.75), Inches(2.7)], font_size=8.0)

    # -------------------------------------------------------------
    # 4. DATABASE, PERSISTENCE & FILE STORAGE STACK
    # -------------------------------------------------------------
    add_h1("4. Database, Persistence & Storage Stack")
    add_bullet("SQLite 3 (Development & Local Environment):", "Zero-configuration, serverless, transactional ACID-compliant single-file database (`donation_tracker.db`). Provides immediate testability and reproducible local execution with zero port bindings.")
    add_bullet("PostgreSQL Dialect Compatibility (Production Readiness):", "The entire persistence tier is defined via SQLAlchemy ORM without raw vendor-specific SQL. Transitioning to cloud PostgreSQL requires solely switching the connection URI string (`postgresql://...`), unlocking row-level concurrency, connection pooling (`psycopg2`), and PostGIS spatial extensions.")
    add_bullet("Local Protected File System Vault (`app/static/uploads/`):", "Binary images and PDFs are NEVER stored directly as BLOBs in database rows to prevent database bloat. Instead, sanitized files are saved into segmented disk directories (`documents/`, `resources/`, `profile_photos/`, `ngo_gallery/`), while the database stores lightweight string URI paths (`VARCHAR(255)`).")
    add_bullet("Cascade Relationship Automation (`cascade='all, delete-orphan'`):", "Ensures strict referential integrity. When a listing or user is deleted, all dependent chat messages (`Message`) and requests (`Request`) are purged automatically, eliminating orphaned records.")

    # -------------------------------------------------------------
    # 5. FEATURE-TO-TECHNOLOGY TRACEABILITY MATRIX
    # -------------------------------------------------------------
    add_h1("5. Feature-to-Technology Traceability Matrix")

    mat_headers = ["Feature Name", "Frontend Stack", "Backend / Controller Stack", "Security / Storage / Algorithmic Layer"]
    mat_rows = [
        ["User Registration & Auth", "HTML5 Forms, Bootstrap 5 Modals, JavaScript", "Flask `auth_routes.py`, Flask-Login, Email OTP", "Bcrypt (Cost 12), SHA-256 OTP (10 min expiry), `users` table"],
        ["DigiLocker e-KYC Verification", "DigiLocker Branded Modal UI, SVG Icons", "Flask `auth_routes.py` OAuth 2.0 PKCE Handshake", "Cryptographic token verification, verified metadata auto-fill"],
        ["Hyperlocal Radius Search", "Leaflet.js 1.9.4, OpenStreetMap Tiles, Slider UI", "Flask `search_routes.py`, `api_resources()`", "Haversine Formula: $d = 2R \\cdot \\text{atan2}(\\sqrt{a}, \\sqrt{1-a})$ ($R=6,371$ km)"],
        ["Anti-Hoarding Protection", "Bootstrap Dynamic Warning Alert Badges", "Flask `request_routes.py`, `send_request()`", "Active Request Counter: $\\text{count}(\\text{Pending}) < 3$ threshold limit"],
        ["Anti-Flipping Cooldowns", "Dynamic Cooldown Expiry Alert Banners", "Flask `request_routes.py` Temporal Engine", "12-Month (365d) Electronics & 6-Month (180d) Appliance Cooldowns"],
        ["Low-Income (EWS) Gating", "Confidential Verified Beneficiary Badge UI", "Flask `profile_routes.py`, `admin_routes.py`", "EWS Document Vault; blinded badge protects beneficiary dignity"],
        ["In-App Handover Messaging", "Asynchronous AJAX Chat Window, Auto-Scroll", "Flask `request_routes.py`, `get_messages()`", "End-to-End Authorization check; cascade delete-orphan cleanup"],
        ["Statutory NGO Verification", "Document Upload Form (PAN & Auth Letter)", "Flask `admin_routes.py` Approval Engine", "Regex: Darpan (`^[A-Z]{2}/\\d{4}/\\d{7}$`), PAN (`^[A-Z]{5}[0-9]{4}[A-Z]{1}$`)"],
        ["Direct Zero-Cut UPI Support", "Dynamic QR Code Renderer, One-Click Intent", "Flask `support_ngos.py`, `UPIDonationClick`", "NPCI UPI URI schema: `upi://pay?pa={upi_id}&pn={name}&cu=INR`"],
        ["Community ❤️ Like Toggle", "Interactive SVG Heart, Asynchronous Counter", "Flask `points_routes.py`, `/like-ngo/<id>`", "Atomic DB Constraint: `UniqueConstraint('user_id', 'ngo_id')`"],
        ["Fraud-Proof Karma Points", "Public Leaderboard, Tier Badges (Bronze-Plat)", "Flask `points_routes.py`, Points Engine", "IP Collision Check (same Wi-Fi $\\implies 0$ pts) + 300 pts/7d velocity cap"],
        ["Mandatory Impact Proof", "Camera / File Receipt Upload Interface", "Flask `profile_routes.py`, `upload_impact_proof()`", "Receipt Lockout Gate: Blocks new requests if past items unproven"]
    ]
    add_table(mat_headers, mat_rows, [Inches(1.6), Inches(1.5), Inches(1.8), Inches(2.1)], font_size=7.8)

    # -------------------------------------------------------------
    # 6. INFRASTRUCTURE & DEPLOYMENT STACK
    # -------------------------------------------------------------
    add_h1("6. Infrastructure, Version Control & Production Deployment Stack")
    add_bullet("WSGI Web Server:", "PythonAnywhere WSGI Runner / Gunicorn Multi-Worker Server. Spawns $(2 \\times \\text{CPUs}) + 1$ concurrent worker threads communicating via Unix sockets for parallel request processing.")
    add_bullet("Version Control & Collaboration:", "Git version control hosted on GitHub. Modular feature branching, atomic commits, and synchronized production deployment via `git pull`.")
    add_bullet("Environment & Dependency Isolation:", "Python `virtualenv` managing explicit dependency trees captured in `requirements.txt` (`Flask`, `SQLAlchemy`, `Flask-Login`, `bcrypt`, `Flask-WTF`, `docx2pdf`).")

    # Save DOCX
    out_docx = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Seva_Sankalp_Tech_Stack_Specification.docx"
    doc.save(out_docx)
    print(f"Successfully generated DOCX: {out_docx}")

if __name__ == "__main__":
    create_tech_stack_doc()
