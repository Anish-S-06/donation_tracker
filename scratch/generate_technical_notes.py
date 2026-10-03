import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def build_technical_dossier():
    doc = Document()

    # Configure Margins (0.8 inch around for clean dense technical layout)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
        # Configure Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("SEVA SANKALP — Technical Architecture, Algorithms & Viva Defense Dossier")
        hrun.font.name = 'Times New Roman'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Page ")
        frun.font.name = 'Times New Roman'
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(100, 100, 100)
        # Add page number XML
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(fldSimple)
        frun2 = fp.add_run(" | Department of Computer Science & Engineering, MVGR College of Engineering")
        frun2.font.name = 'Times New Roman'
        frun2.font.size = Pt(8.5)
        frun2.font.color.rgb = RGBColor(120, 120, 120)

    # Styles & Formatting Helpers
    def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_table_borders(table, color="CCCCCC", sz="4"):
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

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(17)
        r.font.bold = True
        r.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.italic = True
        r.font.color.rgb = RGBColor(70, 70, 70)
        return p

    def add_meta_box(meta_dict):
        tbl = doc.add_table(rows=len(meta_dict), cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        set_table_borders(tbl, color="B0C4DE", sz="6")
        for idx, (k, v) in enumerate(meta_dict.items()):
            row = tbl.rows[idx]
            c0, c1 = row.cells[0], row.cells[1]
            c0.width = Inches(2.2)
            c1.width = Inches(4.6)
            set_cell_background(c0, "F0F4F8")
            set_cell_background(c1, "FFFFFF")
            set_cell_margins(c0, top=50, bottom=50, left=80, right=80)
            set_cell_margins(c1, top=50, bottom=50, left=80, right=80)
            
            p0 = c0.paragraphs[0]
            p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r0 = p0.add_run(k)
            r0.font.name = 'Times New Roman'; r0.font.size = Pt(9.5); r0.font.bold = True
            r0.font.color.rgb = RGBColor(16, 44, 87)
            
            p1 = c1.paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r1 = p1.add_run(v)
            r1.font.name = 'Times New Roman'; r1.font.size = Pt(9.5)
            r1.font.color.rgb = RGBColor(30, 30, 30)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(4)
        p_sp.paragraph_format.space_after = Pt(4)

    def add_sec_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r1 = p.add_run(num_str + " ")
        r1.font.name = 'Times New Roman'; r1.font.size = Pt(13.5); r1.font.bold = True
        r1.font.color.rgb = RGBColor(16, 44, 87)
        r2 = p.add_run(title_str.upper())
        r2.font.name = 'Times New Roman'; r2.font.size = Pt(13.5); r2.font.bold = True
        r2.font.color.rgb = RGBColor(16, 44, 87)
        return p

    def add_sub_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r1 = p.add_run(num_str + " " if num_str else "")
        r1.font.name = 'Times New Roman'; r1.font.size = Pt(11.5); r1.font.bold = True
        r1.font.color.rgb = RGBColor(30, 70, 120)
        r2 = p.add_run(title_str)
        r2.font.name = 'Times New Roman'; r2.font.size = Pt(11.5); r2.font.bold = True
        r2.font.color.rgb = RGBColor(30, 70, 120)
        return p

    def add_body(text, space_after=3.5):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        
        # Simple inline formatting parsing: **bold**, `code`
        tokens = text.split("**")
        is_bold = False
        for part in tokens:
            if not is_bold:
                code_tokens = part.split("`")
                is_code = False
                for c_part in code_tokens:
                    if not is_code:
                        r = p.add_run(c_part)
                        r.font.name = 'Times New Roman'; r.font.size = Pt(10.5)
                        r.font.color.rgb = RGBColor(30, 30, 30)
                    else:
                        r = p.add_run(c_part)
                        r.font.name = 'Consolas'; r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(160, 40, 40)
                    is_code = not is_code
            else:
                r = p.add_run(part)
                r.font.name = 'Times New Roman'; r.font.size = Pt(10.5); r.font.bold = True
                r.font.color.rgb = RGBColor(20, 20, 20)
            is_bold = not is_bold
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.12
        
        r_sym = p.add_run("▪  ")
        r_sym.font.name = 'Arial'; r_sym.font.size = Pt(9.5); r_sym.font.bold = True
        r_sym.font.color.rgb = RGBColor(16, 44, 87)
        
        if bold_prefix:
            prefix_clean = bold_prefix.lstrip("•▪- ").strip()
            r_b = p.add_run(prefix_clean + " ")
            r_b.font.name = 'Times New Roman'; r_b.font.size = Pt(10.5); r_b.font.bold = True
            r_b.font.color.rgb = RGBColor(20, 20, 20)
            
        r_t = p.add_run(text)
        r_t.font.name = 'Times New Roman'; r_t.font.size = Pt(10.5)
        r_t.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_callout(title, body_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.rows[0].cells[0].width = Inches(6.8)
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "F4F7FB")
        set_cell_margins(cell, top=70, bottom=70, left=120, right=100)
        
        # Left border thick navy
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:top w:val="none"/>'
            f'  <w:bottom w:val="none"/>'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="102C57"/>'
            f'  <w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title + "\n")
        r_t.font.name = 'Times New Roman'; r_t.font.size = Pt(10.5); r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(16, 44, 87)
        r_b = p.add_run(body_text)
        r_b.font.name = 'Times New Roman'; r_b.font.size = Pt(10.0)
        r_b.font.color.rgb = RGBColor(40, 40, 40)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(2)
        p_sp.paragraph_format.space_after = Pt(2)

    def add_table_data(headers, rows, col_widths=None, font_size=9.5):
        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        set_table_borders(tbl, color="BDC3C7", sz="4")
        
        # Header
        hdr = tbl.rows[0]
        trPr = hdr._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for idx, text in enumerate(headers):
            cell = hdr.cells[idx]
            if col_widths and idx < len(col_widths):
                cell.width = col_widths[idx]
            set_cell_background(cell, "102C57") # Dark Navy
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
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
                set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx != 0 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.line_spacing = 1.1
                
                # Check for bold prefixes like "Bcrypt:"
                if ":" in str(val) and len(str(val).split(":")[0]) < 25:
                    parts = str(val).split(":", 1)
                    rb = p.add_run(parts[0] + ":")
                    rb.font.name = 'Times New Roman'; rb.font.size = Pt(font_size); rb.font.bold = True
                    rb.font.color.rgb = RGBColor(20, 20, 20)
                    rt = p.add_run(parts[1])
                    rt.font.name = 'Times New Roman'; rt.font.size = Pt(font_size)
                    rt.font.color.rgb = RGBColor(40, 40, 40)
                else:
                    r = p.add_run(str(val))
                    r.font.name = 'Times New Roman'; r.font.size = Pt(font_size)
                    r.font.color.rgb = RGBColor(40, 40, 40)
                    
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(2)
        p_sp.paragraph_format.space_after = Pt(3)

    def add_code_block(code_lines):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.rows[0].cells[0].width = Inches(6.8)
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=60, bottom=60, left=100, right=80)
        set_table_borders(tbl, color="D0D5DD", sz="4")
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.05
        
        for idx, line in enumerate(code_lines):
            r = p.add_run(line + ("\n" if idx < len(code_lines) - 1 else ""))
            r.font.name = 'Consolas'
            r.font.size = Pt(9.0)
            if line.strip().startswith("#"):
                r.font.color.rgb = RGBColor(100, 110, 120)
                r.font.italic = True
            elif "def " in line or "class " in line or "return " in line or "import " in line:
                r.font.color.rgb = RGBColor(16, 44, 87)
                r.font.bold = True
            elif "@" in line:
                r.font.color.rgb = RGBColor(180, 50, 50)
            else:
                r.font.color.rgb = RGBColor(30, 30, 30)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(2)
        p_sp.paragraph_format.space_after = Pt(3)

    def add_viva_qa(q_num, question, answer_bullets):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(7)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        
        rq_num = p_q.add_run(f"Q{q_num}: ")
        rq_num.font.name = 'Times New Roman'; rq_num.font.size = Pt(11.0); rq_num.font.bold = True
        rq_num.font.color.rgb = RGBColor(180, 40, 40) # Crimson red
        
        rq = p_q.add_run(question)
        rq.font.name = 'Times New Roman'; rq.font.size = Pt(11.0); rq.font.bold = True
        rq.font.color.rgb = RGBColor(16, 44, 87)
        
        for b_prefix, b_text in answer_bullets:
            add_bullet(b_prefix, b_text)

    # =========================================================================
    # DOCUMENT CONTENT
    # =========================================================================

    # Title & Metadata
    add_title("SEVA SANKALP: TECHNICAL ARCHITECTURE, ALGORITHM SPECIFICATIONS, WORKFLOWS & VIVA DEFENSE DOSSIER")
    add_subtitle("Comprehensive Technical Master Notes & Oral Examination Guide for Project Reviewers & Evaluators")

    meta_info = {
        "Project Title": "Seva Sankalp — Hyperlocal Peer-to-Peer Donation & Statutory NGO Verification Platform",
        "Domain & Focus": "Web Engineering, Geospatial Computing, Anti-Fraud Systems, Cryptographic Verification, Civic Tech",
        "Team Members": "Neyigapula Meghana (21331A05D8), Sandaka Anish Nihaal (21331A05G5), Mudunuri Sruthi (21331A05E2), Praveen Sahu (21331A05G0)",
        "Project Guide": "Mr. S. Palavelli, M.Tech., (Ph.D.), Assistant Professor, Department of CSE",
        "Institution": "Maharaj Vijayaram Gajapathi Raj (MVGR) College of Engineering (Autonomous), Vizianagaram",
        "Key Technologies": "Python 3.10+, Flask, SQLAlchemy, SQLite/PostgreSQL, Leaflet.js, OpenStreetMap, Bcrypt, Jinja2, Bootstrap 5"
    }
    add_meta_box(meta_info)

    # -------------------------------------------------------------------------
    # SECTION 1: ARCHITECTURAL PARADIGM & SYSTEM ENGINEERING
    # -------------------------------------------------------------------------
    add_sec_heading("1.", "Architectural Paradigm & Engineering Design")
    
    add_sub_heading("1.1", "Model-View-Controller (MVC) Pattern with Modular Flask Blueprints")
    add_body("Seva Sankalp is engineered using the **Model-View-Controller (MVC)** architectural paradigm, implemented via Python Flask's native **Blueprint** mechanism. This design decouples presentation, business processing, and persistence into distinct layers:")
    add_bullet("Model Layer (`app/models.py`):", "Defines the object-relational data contracts using SQLAlchemy ORM. Models encapsulate business rules, constraints (e.g., `unique_user_ngo_like`), relationship cascades (`cascade='all, delete-orphan'`), password hashing algorithms, and dynamic state evaluation methods.")
    add_bullet("View Layer (`app/templates/`, `app/static/`):", "Utilizes the Jinja2 templating engine combined with Bootstrap 5, Leaflet.js, and custom responsive CSS. Views are strictly decoupled from database queries, receiving contextual data dictionaries and rendering semantic, accessible, mobile-optimized HTML5.")
    add_bullet("Controller Layer (`app/core/*_routes.py`):", "Decomposed into 8 isolated Blueprints (`auth_routes`, `resource_routes`, `request_routes`, `search_routes`, `profile_routes`, `admin_routes`, `points_routes`, `history_routes`). Controllers handle HTTP request dispatching, input validation, cryptographic session handling, and coordination between database models and external services.")

    add_sub_heading("1.2", "Application Factory Pattern & Configuration Decoupling")
    add_body("The application initialization follows the **Application Factory Pattern** (`create_app()` in `app/__init__.py`). Instead of binding the application instance globally, the factory dynamically configures extensions (`db`, `login_manager`, `mail`) based on runtime environments (`DevelopmentConfig`, `ProductionConfig`, `TestingConfig`). This guarantees zero state leakage across test suites and enables multiple worker processes in production WSGI servers.")

    add_sub_heading("1.3", "Architectural Trade-Off Analysis: Monolithic MVC vs. Microservices")
    add_body("During architectural formulation, a monolithic MVC design was deliberately chosen over a distributed microservices architecture based on concrete engineering metrics:")

    arch_headers = ["Evaluation Metric", "Monolithic MVC (Implemented)", "Distributed Microservices (Rejected)"]
    arch_rows = [
        ["Network Latency", "In-memory function calls (< 1 ms overhead); zero internal HTTP serialization.", "Inter-service HTTP/gRPC overhead (15-50 ms per request hop across services)."],
        ["ACID Data Integrity", "Single database engine guarantees immediate consistency via atomic SQL transactions.", "Requires distributed 2-Phase Commit (2PC) or Saga patterns; eventual consistency risks."],
        ["Deployment Overhead", "Single WSGI container deployment on PythonAnywhere / Gunicorn; minimal DevOps cost.", "Requires container orchestrators (Kubernetes/Docker), API gateways, service meshes."],
        ["State Management", "Flask-Login centralized session handling with secure HttpOnly cookie tokens.", "Requires distributed JWT token stores, OAuth authorization servers, and Redis sync."],
        ["Development Velocity", "Unified codebase, instant schema migrations, straightforward debugging and profiling.", "Complex multi-repo management, network failure modes, RPC versioning conflicts."]
    ]
    add_table_data(arch_headers, arch_rows, [Inches(1.5), Inches(2.65), Inches(2.65)])

    add_callout("Key Viva Takeaway (Architecture)", "When judges ask 'Why did you not use Microservices?', state: 'For a community-scale civic application, microservices introduce distributed network latency, data synchronization risks, and heavy infrastructure costs without adding value. Our modular Flask Blueprint architecture delivers identical clean separation of concerns with the ultra-low latency, immediate ACID transactional consistency, and zero DevOps overhead of a production-grade monolithic deployment.'")

    # -------------------------------------------------------------------------
    # SECTION 2: COMPLETE END-TO-END TECHNOLOGY STACK
    # -------------------------------------------------------------------------
    add_sec_heading("2.", "Complete End-to-End Technology Stack (Deep Dive)")
    add_body("Every tier of Seva Sankalp is built on open-source, industry-standard, production-proven technologies selected for speed, security, and developer ergonomics:")

    stack_headers = ["Layer / Domain", "Technology & Version", "Core Role in Seva Sankalp", "Engineering Justification over Alternatives"]
    stack_rows = [
        ["Frontend UI", "HTML5 & CSS3", "Semantic layouts, responsive flex/grid, dark mode", "Native browser performance, accessibility (WAI-ARIA), no heavy bundle build steps."],
        ["Frontend Styling", "Bootstrap 5.3", "Responsive grid, modals, alert banners, badges", "Rapid responsive prototyping; avoids React/Vue build complexity for SSR applications."],
        ["Geospatial GIS", "Leaflet.js 1.9.4", "Interactive map rendering, custom marker popups", "Lightweight (42 KB vs 300 KB Google Maps), zero commercial API billing, privacy-preserving."],
        ["Map Tiles", "OpenStreetMap (OSM)", "Tile layer imagery via OpenStreetMap Carto", "Free community-driven tile server; eliminates dependency on Google Cloud billing quotas."],
        ["Iconography", "FontAwesome 6.4", "Visual cues: heart like, pin, badges, status", "Scalable vector icons with clean semantic class integration across UI components."],
        ["Client Scripting", "Vanilla JavaScript (ES6+)", "Asynchronous Fetch API for likes, chat, map sync", "Native browser execution without NPM/Node compilation dependencies; zero bundle bloat."],
        ["Backend Runtime", "Python 3.10 / 3.13", "Core computational engine and business logic", "Robust standard library (`math`, `datetime`, `re`), clean syntax, excellent ORM support."],
        ["Web Framework", "Flask 3.0.x (WSGI)", "Routing, request handling, Blueprint modularity", "Microframework flexibility; avoids Django's rigid monolithic boilerplate and ORM lock-in."],
        ["Templating", "Jinja2 3.1.x", "Server-Side Rendering (SSR) & XSS protection", "Automatic context-aware HTML escaping, template inheritance, lightning-fast rendering."],
        ["Database ORM", "SQLAlchemy 2.0.x", "Object-Relational Mapping & query compilation", "Type-safe database abstraction, parameterized queries (SQLi immune), cascade automation."],
        ["Database Engine", "SQLite / PostgreSQL", "ACID persistence, relational data integrity", "SQLite for lightweight zero-config MVP; fully schema-compatible with PostgreSQL for cloud."],
        ["Authentication", "Flask-Login 0.6.x", "User session state machine & route protection", "Secure cookie-based authentication, user loader abstraction, automatic session teardown."],
        ["Password Security", "Bcrypt 4.x", "Blowfish cryptographic hashing with adaptive salt", "Computationally resistant to GPU/ASIC brute-force cracking, unlike MD5 or raw SHA-256."],
        ["Form Security", "Flask-WTF / CSRFProtect", "Cryptographic token injection on POST requests", "Stops Cross-Site Request Forgery via signed HMAC session tokens on all stateful forms."],
        ["Web Server Gateway", "Werkzeug WSGI", "HTTP request dispatching & secure file naming", "`secure_filename()` sanitization stops directory traversal attacks (`../../etc/passwd`)."],
        ["Production WSGI", "PythonAnywhere / Gunicorn", "Multi-worker concurrent request processing", "WSGI-compliant process management, automatic recycling of worker processes."]
    ]
    add_table_data(stack_headers, stack_rows, [Inches(1.2), Inches(1.4), Inches(2.2), Inches(2.0)], font_size=8.8)

    # -------------------------------------------------------------------------
    # SECTION 3: CORE ALGORITHMS & MATHEMATICAL FORMULATIONS
    # -------------------------------------------------------------------------
    add_sec_heading("3.", "Core Algorithms & Mathematical Formulations")

    add_sub_heading("3.1", "Algorithm 1: Spherical Geodesic Haversine Distance Search")
    add_body("Hyperlocal resource discovery requires calculating the precise great-circle distance between two geographic coordinates on Earth given by latitude ($\\phi$) and longitude ($\\lambda$).")
    
    add_bullet("Mathematical Formulation:", "Earth is an oblate spheroid, but for short-to-medium regional distances (1 to 50 km), modeling it as a sphere of mean radius $R = 6,371.0\\text{ km}$ yields accuracy within 0.3%. The Haversine trigonometric formulation is:")
    
    add_callout("The Haversine Equations", 
        "1. Latitude Delta:   Δφ = φ₂ - φ₁  (converted to radians: deg × π / 180)\n"
        "2. Longitude Delta:  Δλ = λ₂ - λ₁  (converted to radians: deg × π / 180)\n"
        "3. Square of Half Chord Length:\n"
        "      a = sin²(Δφ / 2) + cos(φ₁) · cos(φ₂) · sin²(Δλ / 2)\n"
        "4. Angular Distance in Radians:\n"
        "      c = 2 · atan2( √a, √(1 - a) )\n"
        "5. Great-Circle Distance:\n"
        "      d = R · c   (where R = 6,371.0 km)"
    )

    add_bullet("Why Not Flat Euclidean Distance?:", "A naive Pythagorean flat approximation $d = \\sqrt{(\\Delta x)^2 + (\\Delta y)^2}$ produces catastrophic errors. On Earth, lines of longitude converge toward the poles ($1^\\circ\\text{ lon} = 111.32\\text{ km} \\times \\cos(\\phi)$), whereas latitude lines remain constant ($1^\\circ\\text{ lat} \\approx 111\\text{ km}$). A flat calculation treats degrees as square, distorting distances by 15% to 40% even over modest city distances.")
    add_bullet("Algorithmic Implementation in `app/core/search_routes.py`:", "")

    haversine_code = [
        "import math",
        "",
        "def haversine(lat1, lon1, lat2, lon2):",
        "    R = 6371.0  # Earth's mean radius in kilometers",
        "    dlat = math.radians(lat2 - lat1)",
        "    dlon = math.radians(lon2 - lon1)",
        "    a = (math.sin(dlat / 2) ** 2 +",
        "         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)",
        "    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))",
        "    return R * c  # Returns great-circle distance in km"
    ]
    add_code_block(haversine_code)

    add_bullet("Computational Complexity & Spatial Optimization:", "Evaluating $N$ active resources in memory requires $O(N)$ trigonometric calculations. For scaling beyond 10,000 resources, Seva Sankalp supports **Bounding Box Pre-Filtering**: compute $[\text{lat} \\pm \\Delta \\text{lat}, \\text{lng} \\pm \\Delta \\text{lng}]$ where $\\Delta \\text{lat} = \\frac{\\text{radius}}{111.0}$ and $\\Delta \\text{lng} = \\frac{\\text{radius}}{111.0 \\cdot \\cos(\\text{lat})}$. The SQL database uses standard B-tree index scans on latitude and longitude in $O(\\log N)$ time, evaluating the exact Haversine equation only on the candidate subset.")

    add_sub_heading("3.2", "Algorithm 2: Anti-Flipping & Anti-Hoarding Sliding-Window Cooldown")
    add_body("Free redistribution platforms frequently suffer from predatory resellers and hoarders who collect donated electronics and appliances to sell on commercial marketplaces (e.g., OLX, Cashify). Seva Sankalp implements a multi-tier programmatic barrier:")

    add_bullet("1. Anti-Hoarding Concurrent Cap:", "A recipient cannot create a new request if they already have $\\ge 3$ active requests with status `Pending` across all platform resources: $\\text{COUNT}(\\text{Request}_{\\text{status='Pending'}, \\text{receiver}=\\text{current\\_user}}) < 3$. Time complexity: $O(1)$ indexed count.")
    add_bullet("2. Category Lock (Active Request Mutual Exclusion):", "A user cannot have more than 1 active request (`Pending` or `Accepted`) in the `Electronics` or `Household` categories concurrently.")
    add_bullet("3. Category-Specific Cooldown Windows:", "When an item in a high-value category is marked `Fulfilled`, a dynamic cooldown timer is stamped against the recipient's user ID. If $T_{\\text{current}} - T_{\\text{fulfilled}} < \\Delta t_{\\text{category}}$, subsequent requests for that category are strictly rejected:")
    
    cd_headers = ["Category", "Cooldown Window (Δt)", "Rationale & Resale Vulnerability", "Rule Enforcement Condition"]
    cd_rows = [
        ["Electronics", "365 Days (12 Months)", "Laptops, phones, tablets have high cash-out value; 1 year ensures genuine academic/work use.", "IF (now - last_fulfilled.updated_at).days < 365 THEN REJECT"],
        ["Household", "180 Days (6 Months)", "Appliances (fans, stoves, blenders) have durable utility; 6 months prevents household hoarding.", "IF (now - last_fulfilled.updated_at).days < 180 THEN REJECT"],
        ["Books & Clothes", "0 Days (No Cooldown)", "Low resale value; educational and clothing needs recur frequently throughout the year.", "Allowed immediately subject to the global 3-request pending cap."]
    ]
    add_table_data(cd_headers, cd_rows, [Inches(1.2), Inches(1.5), Inches(2.3), Inches(1.8)])

    add_bullet("4. Mandatory Impact Proof Gating:", "Before submitting any new request, the platform queries whether the recipient has fulfilled requests lacking an uploaded receipt photo: $\\text{DonationHistory.receipt\\_photo} == \\text{None}$. If unproven transactions exist, all new requests are locked until the user uploads physical photo proof of impact.")

    add_sub_heading("3.3", "Algorithm 3: Fraud-Proof Karma Ledger & Anti-Gaming Engine")
    add_body("Gamification badges and Karma points encourage community participation but are vulnerable to Sybil attacks (users creating fake dummy accounts to donate fictitious items back and forth). Seva Sankalp eliminates point gaming through an idempotent, multi-check audit ledger:")

    add_bullet("1. Client IP Collision Detection:", "Upon transaction fulfillment, the server retrieves `current_user.last_login_ip` and `receiver.last_login_ip`. If $\\text{IP}_{\\text{donor}} == \\text{IP}_{\\text{receiver}}$ (and $\\text{IP} \\neq \\text{'127.0.0.1'}$), points awarded are reset to **0**, and a fraud audit log is generated. The physical handover proceeds to avoid penalizing legitimate users, but no gaming reward is granted.")
    add_bullet("2. Sliding 7-Day Velocity Cap (Max 300 Points):", "To prevent artificial point surges, the engine calculates the sum of all points earned by the user over the trailing 7 days: $\\sum_{t \\in T_{7\\text{d}}} t.\\text{amount}$. If $\\text{sum} + \\text{points\\_awarded} > 300$, points awarded are clamped to 0.")
    add_bullet("3. Tier Level Calculation Function:", "Badges are programmatically updated following the fulfillment transaction:")
    
    tier_code = [
        "# app/core/request_routes.py - Karma Points Allocation",
        "points_awarded = 50",
        "if current_user.last_login_ip == receiver.last_login_ip and current_user.last_login_ip != '127.0.0.1':",
        "    points_awarded = 0  # Same-network collision detected",
        "",
        "if points_awarded > 0:",
        "    seven_days_ago = datetime.utcnow() - timedelta(days=7)",
        "    recent_points = db.session.query(func.sum(PointsTransaction.amount)).filter(",
        "        PointsTransaction.user_id == current_user.id,",
        "        PointsTransaction.created_at >= seven_days_ago).scalar() or 0",
        "    if recent_points + points_awarded > 300:",
        "        points_awarded = 0  # Velocity cap exceeded",
        "",
        "if points_awarded > 0:",
        "    current_user.points_balance += points_awarded",
        "    if current_user.points_balance >= 5000: current_user.badge_level = 'Platinum'",
        "    elif current_user.points_balance >= 1000: current_user.badge_level = 'Gold'",
        "    elif current_user.points_balance >= 500: current_user.badge_level = 'Silver'",
        "    elif current_user.points_balance >= 100: current_user.badge_level = 'Bronze'"
    ]
    add_code_block(tier_code)

    add_sub_heading("3.4", "Algorithm 4: Statutory NGO & DigiLocker e-KYC Verification Pipeline")
    add_body("To prevent fly-by-night fraudulent charities from collecting public goods and monetary donations, non-profits undergo strict administrative auditing against statutory government registries:")
    add_bullet("NITI Aayog NGO Darpan ID Validation:", "Verified against the statutory central portal format `^[A-Z]{2}/\\d{4}/\\d{7}$` (e.g., `AP/2021/0284719`), representing state code, registration year, and 7-digit sequential unique identity.")
    add_bullet("Income Tax Department Organization PAN:", "Verified against India's statutory 10-character alphanumeric structure `^[A-Z]{5}[0-9]{4}[A-Z]{1}$` where the 4th character must be 'C' (Company), 'T' (Trust), or 'A' (Association of Persons).")
    add_bullet("DigiLocker e-KYC Integration Flow:", "DigiLocker allows users to prove credentials (Aadhaar, MeeSeva Income Certificates) without sharing raw identity numbers. The simulated/production pipeline uses OAuth 2.0 PKCE with API Setu to obtain a cryptographically signed XML document, validating eligibility without exposing unredacted records.")
    add_bullet("Confidential EWS / Low-Income Gating:", "When a donor marks a resource as `requires_income_proof = True`, only recipients with `income_verification_status == 'approved'` can submit requests. Crucially, donors never see the recipient's private financial certificate; the system displays an official verified badge, preserving beneficiary dignity while satisfying donor intent.")

    add_sub_heading("3.5", "Algorithm 5: Bcrypt Cryptographic Key Derivation & Password Storage")
    add_body("User passwords are never stored in plaintext or reversible encryption. Seva Sankalp uses the **Bcrypt** cryptographic password-hashing function based on the Blowfish block cipher:")
    add_bullet("Salt Generation:", "A cryptographically secure pseudo-random 128-bit salt is generated per user via `bcrypt.gensalt()`. This completely defeats pre-computed rainbow table attacks.")
    add_bullet("Adaptive Cost Factor (Work Factor = 12):", "The algorithm executes $2^{12} = 4,096$ iterations of the Blowfish key schedule. Even if an attacker gains read access to the database, cracking a single 8-character password via brute-force requires prohibitive GPU processing time, whereas legitimate login verification takes only ~100 ms on the web server.")
    add_bullet("Timing Attack Defense:", "Password verification invokes `bcrypt.checkpw()`, which performs constant-time string comparison, neutralizing side-channel timing analysis.")

    # -------------------------------------------------------------------------
    # SECTION 4: TECHNICAL WORKFLOWS & STATE MACHINES
    # -------------------------------------------------------------------------
    add_sec_heading("4.", "System Technical Workflows & State Machines")

    add_sub_heading("4.1", "Workflow 1: User Onboarding & DigiLocker e-KYC Flow")
    add_bullet("Step 1 (Form Submission):", "User fills registration form with email, password, and phone number.")
    add_bullet("Step 2 (DigiLocker Verification Option):", "User can click 'Register with DigiLocker'. The system initiates an OAuth 2.0 redirection handshake, requests citizen identity scopes, and fetches verified profile metadata.")
    add_bullet("Step 3 (Password Hashing):", "Controller invokes `user.set_password(pwd)`, generating a 128-bit salt and 60-character modular crypt format string (`$2b$12$...`).")
    add_bullet("Step 4 (OTP Verification):", "A 6-digit cryptographic OTP is generated and cached with a 10-minute expiry timestamp. User confirms email before account activation.")

    add_sub_heading("4.2", "Workflow 2: Donor Resource Publishing & Geocoding")
    add_bullet("Step 1 (Input & Image Upload):", "Donor enters title, description, category (`Electronics`, `Books`, `Clothing`, `Household`), condition, and uploads an image.")
    add_bullet("Step 2 (MIME Validation & Sanitization):", "Controller uses `werkzeug.utils.secure_filename()` to strip path separators, validates file extension against an allowlist (`png`, `jpg`, `jpeg`, `webp`), and writes to `static/uploads/resources/` with a unique timestamped filename.")
    add_bullet("Step 3 (Geocoding & Persistence):", "Coordinates (`location_lat`, `location_lng`) and address are captured via browser Geolocation API or map pin click and committed to the `resources` table with status `Available`.")

    add_sub_heading("4.3", "Workflow 3: Hyperlocal Search & Distance Filtering")
    add_bullet("Step 1 (Client Coordinate Capture):", "Browser obtains user GPS via `navigator.geolocation.getCurrentPosition()` or user enters search radius (1–50 km).")
    add_bullet("Step 2 (AJAX Request):", "Frontend dispatches `GET /search/api/resources?lat=18.11&lng=83.40&radius=10&category=Electronics`.")
    add_bullet("Step 3 (Server-Side Haversine Calculation):", "Flask queries all `status='Available'` resources, computes Haversine distance, discards items where `distance > radius`, and sorts by ascending distance.")
    add_bullet("Step 4 (Leaflet Map Render):", "Client receives JSON, clears existing map layers, and plots custom interactive SVG markers. Clicking a marker displays item thumbnail, distance badge, and a 'Request Item' action button.")

    add_sub_heading("4.4", "Workflow 4: Request Pipeline, Verification & Anti-Fraud Execution")
    add_body("When a recipient clicks 'Send Request', the system executes a sequential 6-gate safety validation before creating the transaction:")
    add_bullet("Gate 1 (Account Status):", "Verify `current_user.verification_status == 'approved'` and `current_user.is_ngo == False`.")
    add_bullet("Gate 2 (Pending Impact Proof):", "Query `DonationHistory` for unproven past fulfillments; block if receipts are missing.")
    add_bullet("Gate 3 (Anti-Hoarding Cap):", "Verify active pending requests count is strictly $< 3$.")
    add_bullet("Gate 4 (EWS / Income Gate):", "If `resource.requires_income_proof`, verify `current_user.income_verification_status == 'approved'`.")
    add_bullet("Gate 5 (Electronics Cooldown):", "If category is `Electronics`, ensure 0 active electronics requests and $\\ge 365$ days since last fulfilled electronics item.")
    add_bullet("Gate 6 (Household Cooldown):", "If category is `Household`, ensure 0 active household requests and $\\ge 180$ days since last fulfilled household item.")
    add_bullet("Commit:", "Create record in `requests` table with status `Pending`; trigger email notification to donor.")

    add_sub_heading("4.5", "Workflow 5: Handover Coordination & In-App Messaging")
    add_bullet("Step 1 (Donor Decision):", "Donor views recipient profile, trust score, and badge. Donor clicks 'Accept' or 'Reject'.")
    add_bullet("Step 2 (Chat Channel Initialization):", "When status transitions to `Accepted`, an in-app chat channel unlocks (`/request/<id>/messages`).")
    add_bullet("Step 3 (Safe Coordination):", "Donor and recipient exchange logistics details. Crucially, private phone numbers and personal home addresses are never exposed publicly, preventing harassment.")

    add_sub_heading("4.6", "Workflow 6: Fulfillment, Impact Proof & Karma Audit")
    add_bullet("Step 1 (Handover Completion):", "After physical exchange, donor clicks 'Mark as Fulfilled'. Both resource and request transition to `Fulfilled`.")
    add_bullet("Step 2 (Anti-Gaming Check):", "Server inspects `last_login_ip` of both parties and checks trailing 7-day points velocity.")
    add_bullet("Step 3 (Ledger Record):", "If legitimate, 50 Karma points are appended to `points_transactions` and `user.points_balance` is incremented.")
    add_bullet("Step 4 (Mandatory Impact Receipt):", "Recipient is required to upload a photo of the item in active use, closing the accountability loop.")

    add_sub_heading("4.7", "Workflow 7: Statutory NGO Support & Community Endorsements (❤️ Likes)")
    add_bullet("Step 1 (Registration):", "NGO submits Darpan ID, PAN number, registration certificate, and UPI VPA ID (`ngo@upi`).")
    add_bullet("Step 2 (Admin Review):", "Admin audits statutory credentials and approves the NGO, publishing it to `/support-ngos`.")
    add_bullet("Step 3 (Direct UPI Support):", "Citizens scan the dynamically rendered UPI QR code (`upi://pay?pa=...&pn=...`) to donate directly to the NGO's bank account with 0 platform cuts.")
    add_bullet("Step 4 (❤️ Community Like Toggle):", "Authenticated users can click the heart button. JavaScript dispatches `POST /like-ngo/<id>`. The controller toggles the `NGOLike` record idempotently and returns `{ liked: true/false, likes_count: N }`, updating the UI instantly without page reload.")

    # -------------------------------------------------------------------------
    # SECTION 5: EXHAUSTIVE VIVA VOCE & TECHNICAL DEFENSE Q&A (45 QUESTIONS)
    # -------------------------------------------------------------------------
    add_sec_heading("5.", "Exhaustive Viva Voce & Technical Defense Q&A (45 Master Questions)")
    add_body("Below are 45 rigorous technical questions categorized across software engineering disciplines, complete with authoritative model answers tailored for judge evaluations:")

    # Category 1: Architecture & Frameworks
    add_sub_heading("5.1", "Category 1: System Architecture & Framework Decisions")

    add_viva_qa(1, "Why did you choose Flask over Django or Node.js/Express?", [
        ("Granular Architectural Control:", "Django is an opinionated framework that imposes rigid conventions, heavyweight ORM defaults, and built-in admin overhead that was unnecessary for our custom anti-fraud and geolocation workflows."),
        ("Microframework Lightweight Footprint:", "Flask provides a lightweight WSGI core allowing us to select precisely the extensions we need (SQLAlchemy 2.0, Flask-Login, Bcrypt) without bundle bloat."),
        ("Native Python Scientific Ecosystem:", "Python gives us direct access to mathematical libraries (`math`, `datetime`, future AI integrations) which Node.js lacks natively.")
    ])

    add_viva_qa(2, "What is the Application Factory Pattern and why did you use it?", [
        ("Explanation:", "Instead of instantiating `app = Flask(__name__)` globally at the module level, we define a function `create_app(config_name)` inside `app/__init__.py` that instantiates, configures, and binds extensions to the app dynamically."),
        ("Benefits:", "1) Prevents circular imports between route Blueprints and models. 2) Allows isolated testing with different configurations (e.g., in-memory SQLite for tests vs file-based SQLite in production). 3) Enables WSGI servers to spawn clean worker processes.")
    ])

    add_viva_qa(3, "How do Flask Blueprints work under the hood?", [
        ("Concept:", "A Blueprint is a recording mechanism for routes and handlers that can be registered onto a Flask application instance. It represents a logical slice of the application."),
        ("Implementation in Seva Sankalp:", "We created 8 independent Blueprints (`auth_bp`, `resource_bp`, `request_bp`, etc.) each with its own URL prefix (e.g., `/request`, `/search`). When `app.register_blueprint()` is called in the factory, Flask attaches these routes to the central Werkzeug URL map.")
    ])

    add_viva_qa(4, "How is state managed across requests in your web application?", [
        ("Stateless HTTP with Cryptographic Cookies:", "HTTP is inherently stateless. Flask-Login uses cryptographically signed session cookies stored in the client browser."),
        ("Security Attributes:", "The session cookie contains an encrypted user identifier. It is marked `HttpOnly` (inaccessible to JavaScript, stopping XSS cookie theft) and `SameSite=Lax` (stopping CSRF cookie leakage)."),
        ("User Loader:", "On every incoming request, `@login_manager.user_loader` extracts the user ID from the session and retrieves the active `User` model from the database into `flask_login.current_user`.")
    ])

    add_viva_qa(5, "What happens when two users try to request the same item at the exact same millisecond (Race Condition)?", [
        ("Current Concurrency Control:", "SQLite serializes write transactions using a database-level lock. Only one `INSERT` into `requests` executes first."),
        ("Application Level Mutual Exclusion:", "The controller executes `already_requested = DonationRequest.query.filter_by(resource_id=..., receiver_id=...).first()`. Once the donor accepts one request, the resource transitions to `status = 'Requested'` or `Fulfilled`, automatically invalidating subsequent acceptance actions."),
        ("Production Database Lock:", "In PostgreSQL, this is handled via `SELECT FOR UPDATE` or a composite unique constraint on `(resource_id, receiver_id)` enforcing database-level atomicity.")
    ])

    add_viva_qa(6, "What is the role of Werkzeug in your application?", [
        ("WSGI Foundation:", "Werkzeug is the comprehensive WSGI web application library powering Flask underneath. It parses HTTP headers, cookies, URL routing rules, and multi-part form file data."),
        ("Security Utility:", "We explicitly use `werkzeug.utils.secure_filename()` on uploaded documents to strip dangerous characters like `../` and null bytes, preventing directory traversal exploits.")
    ])

    add_viva_qa(7, "Why did you implement Server-Side Rendering (SSR) with Jinja2 instead of a React/Vue SPA?", [
        ("Zero Bundle Overhead:", "Single-Page Applications require multi-megabyte JavaScript bundles, client-side hydration delays, and complex Webpack/Vite build toolchains that slow down low-bandwidth mobile users in rural areas."),
        ("Instant First Contentful Paint (FCP):", "Jinja2 compiles semantic HTML directly on the server in ~15 ms, delivering immediate rendering on budget smartphones."),
        ("Enhanced Security:", "CSRF tokens are injected directly into server-rendered forms, avoiding token storage vulnerabilities in browser `localStorage`.")
    ])

    # Category 2: Algorithms & Mathematics
    add_sub_heading("5.2", "Category 2: Core Algorithms & Mathematical Formulations")

    add_viva_qa(8, "Derive the Haversine formula and explain why it is preferred over the Spherical Law of Cosines.", [
        ("Derivation Basis:", "The Haversine formula calculates the angular distance between points on a sphere from their latitudes and longitudes using half-angles: $\\text{haversin}(\\theta) = \\sin^2(\\theta / 2) = \\frac{1 - \\cos \\theta}{2}$."),
        ("Numerical Precision at Small Distances:", "The classic Spherical Law of Cosines uses $\\cos(c) = \\sin(\\phi_1)\\sin(\\phi_2) + \\cos(\\phi_1)\\cos(\\phi_2)\\cos(\\Delta \\lambda)$. For nearby points (e.g., 500 meters apart), $\\cos(c)$ is extremely close to 1.0 (e.g., 0.99999998). Floating-point roundoff error in computers causes severe precision loss (catastrophic cancellation). Haversine avoids this by working with $\\sin^2(\\Delta / 2)$, maintaining floating-point accuracy down to centimeters.")
    ])

    add_viva_qa(9, "What is the time complexity of your geospatial search?", [
        ("Current Complexity:", "$O(N)$ where $N$ is the number of available resources. For each item, the Haversine function evaluates 7 trigonometric operations in memory."),
        ("Practical Benchmark:", "In Python, 1,000 resources are evaluated in approximately 1.8 milliseconds, which is imperceptible to web users."),
        ("Scalability Pathway to $O(\\log N)$:", "For $N > 100,000$, we apply Bounding Box SQL filtering: `WHERE location_lat BETWEEN lat - Δ AND lat + Δ`, which uses standard B-tree database indexes in $O(\\log N)$ time, calculating Haversine only on the surviving bounding-box candidates.")
    ])

    add_viva_qa(10, "Explain the exact logic of the Anti-Flipping cooldown algorithm.", [
        ("Temporal Delta Calculation:", "When a request is submitted, we query the most recent fulfilled request for that user in that category: `fulfilled = Request.query.filter_by(receiver_id=uid, status='Fulfilled').order_by(updated_at.desc()).first()`."),
        ("Cooldown Check:", "We compute `days_passed = (datetime.utcnow() - fulfilled.updated_at).days`. For `Electronics`, if `days_passed < 365`, the request is rejected and the user is told `Cooldown unlocks in (365 - days_passed) days`. For `Household`, the threshold is 180 days.")
    ])

    add_viva_qa(11, "How does your system prevent fake self-donations between friends or on the same device?", [
        ("Dual-Layer IP & Network Check:", "Upon fulfillment, the server evaluates `current_user.last_login_ip == receiver.last_login_ip`. If they match (and are not localhost), the transaction is flagged and `points_awarded` is forced to 0."),
        ("Weekly Velocity Limiter:", "Even if bad actors use VPNs to cycle IP addresses, the rolling 7-day query caps points to 300 maximum per week, destroying any incentive for bot-driven point farming.")
    ])

    add_viva_qa(12, "Why are Karma points non-transferable?", [
        ("Sybil Attack Mitigation:", "If points were transferable, bad actors could create 50 bot accounts, harvest beginner points, and transfer them into a single primary account to unlock Platinum status fraudulently. Non-transferability guarantees that trust scores reflect genuine individual community service.")
    ])

    add_viva_qa(13, "What regex pattern validates the NITI Aayog NGO Darpan ID?", [
        ("Regex:", "`^[A-Z]{2}/\\d{4}/\\d{7}$`"),
        ("Structural Breakdown:", "`[A-Z]{2}` represents the 2-letter state code (e.g., `AP`, `MH`, `DL`); `/` is the mandatory delimiter; `\\d{4}` is the 4-digit registration year; and `\\d{7}` is the 7-digit unique sequential non-profit identifier issued by NITI Aayog.")
    ])

    add_viva_qa(14, "How is the community ❤️ Like button toggle made idempotent?", [
        ("Database Constraint:", "`NGOLike` has `__table_args__ = (db.UniqueConstraint('user_id', 'ngo_id'),)`."),
        ("Toggle Logic:", "The controller executes `like = NGOLike.query.filter_by(user_id=uid, ngo_id=nid).first()`. If `like` exists, `db.session.delete(like)` is called. If not, `db.session.add(NGOLike(user_id=uid, ngo_id=nid))` is called. Because of the unique constraint, no race condition can ever produce duplicate likes for the same user.")
    ])

    add_viva_qa(15, "How does the Bcrypt algorithm ensure passwords cannot be cracked with modern GPUs?", [
        ("Memory-Hard Algorithm:", "Unlike SHA-256 or MD5 which are fast mathematical hashes designed for message verification, Bcrypt requires 4 KB of high-speed memory for Blowfish S-boxes during key expansion. This memory-hard requirement drastically throttles massively parallel GPU and ASIC hardware crackers.")
    ])

    # Category 3: Database & Data Integrity
    add_sub_heading("5.3", "Category 3: Database Design, Schema & Concurrency")

    add_viva_qa(16, "Explain how referential integrity and cascading deletes work in your SQLAlchemy models.", [
        ("Parent-Child Relationship:", "In `app/models.py`, `Request` defines `messages = db.relationship('Message', backref='request', cascade='all, delete-orphan')`."),
        ("Operational Benefit:", "If a donor deletes an expired listing or an admin removes a fraudulent request, SQLAlchemy automatically cascades the deletion down to all associated chat messages, preventing orphaned child records from corrupting database foreign key integrity.")
    ])

    add_viva_qa(17, "What are ACID properties and how does your database maintain them?", [
        ("Atomicity:", "Every fulfillment operation (updating request status, creating history record, awarding Karma points) executes inside a single `db.session.commit()`. If any step fails, `db.session.rollback()` reverts all modifications completely."),
        ("Consistency:", "Enforced via foreign key constraints (`db.ForeignKey('users.id')`) and column data type constraints."),
        ("Isolation:", "Transactions are isolated by the database engine, preventing dirty reads or phantom reads."),
        ("Durability:", "Once `db.session.commit()` returns, changes are written to persistent disk storage.")
    ])

    add_viva_qa(18, "Why did you use SQLite for development and how will you transition to PostgreSQL?", [
        ("Development Efficiency:", "SQLite requires zero background server configuration, zero port bindings, and lives inside a single portable file (`donation_tracker.db`), allowing immediate local execution and test reproducibility."),
        ("PostgreSQL Production Transition:", "Because our entire schema is mapped via SQLAlchemy ORM without raw vendor-specific SQL, moving to PostgreSQL requires merely changing `SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@host:5432/dbname'` in `config.py` and running `flask db upgrade`.")
    ])

    add_viva_qa(19, "What is the difference between `lazy=True`, `lazy='dynamic'`, and `lazy='joined'` in SQLAlchemy?", [
        ("`lazy=True` (Select Loading):", "Loads related child records only when accessed as an attribute (default). Suitable for collections of modest size like a request's messages."),
        ("`lazy='dynamic'`:", "Returns a SQLAlchemy query object instead of a list. Used on `user.liked_ngos` so we can chain `.count()` or `.filter()` directly on the database engine without loading thousands of like objects into RAM."),
        ("`lazy='joined'` (Eager Loading):", "Emits an inner/left join in the initial SQL query, eliminating the N+1 query problem when displaying items and donors together.")
    ])

    add_viva_qa(20, "What is the N+1 Query Problem and how can it be avoided in your application?", [
        ("The Problem:", "If you query 100 resources and then loop through them displaying `resource.donor.email`, a naive ORM emits 1 initial query for resources + 100 separate queries for each donor (101 total queries), choking database performance."),
        ("The Solution:", "Using SQLAlchemy eager loading via `Resource.query.options(db.joinedload(Resource.donor)).all()`. This issues a single `LEFT OUTER JOIN` query, reducing database roundtrips from 101 to exactly 1.")
    ])

    add_viva_qa(21, "How are user profile images and documents stored in the database?", [
        ("Best Practice Architecture:", "Binary file blobs (BLOBs) are NEVER stored directly in database rows, as that causes catastrophic database bloat and slow backups."),
        ("File System + DB Pointer:", "Files are saved to disk under `app/static/uploads/documents/` and `app/static/uploads/resources/`. The database stores only the sanitized relative string path (`VARCHAR(255)`) to the asset.")
    ])

    add_viva_qa(22, "What database indexes are essential for Seva Sankalp in a production environment?", [
        ("Key Indexes:", "1) `users(email)`: Unique index for $O(1)$ login lookups. 2) `resources(status, category)`: Composite index for fast marketplace filtering. 3) `resources(location_lat, location_lng)`: Geospatial index for bounding-box queries. 4) `requests(receiver_id, status)`: Fast evaluation of anti-hoarding and cooldown limits. 5) `ngo_likes(user_id, ngo_id)`: Unique composite index for instant like state lookup.")
    ])

    add_viva_qa(23, "Explain the database schema relationship for direct UPI tracking (`UPIDonationClick`).", [
        ("Tracking Mechanism:", "When a donor clicks to scan an NGO's UPI QR code, an asynchronous record is logged in `upi_donation_clicks` with `donor_id`, `ngo_id`, and `timestamp`. This provides the NGO and admin with intent metrics without touching sensitive bank credentials.")
    ])

    # Category 4: Web Security & Privacy
    add_sub_heading("5.4", "Category 4: Web Security, Cryptography & Privacy Compliance")

    add_viva_qa(24, "How does your platform prevent Cross-Site Request Forgery (CSRF)?", [
        ("CSRF Protection Mechanism:", "We implement Flask-WTF / CSRFProtect. Every state-modifying form includes a hidden input `<input type='hidden' name='csrf_token' value='{{ csrf_token() }}'>`."),
        ("Cryptographic Validation:", "The token is an HMAC-SHA256 signature combining the user's session identifier and server secret key with a timestamp. An external malicious site cannot forge this signed token, blocking cross-origin unauthorized submissions.")
    ])

    add_viva_qa(25, "How does Seva Sankalp prevent SQL Injection attacks?", [
        ("SQLAlchemy Parameterization:", "All database interactions execute via SQLAlchemy ORM. The ORM translates Python queries into parameterized SQL statements with placeholders (`?` or `:val`). User inputs are transmitted separately from the SQL command structure, rendering injection attacks such as `' OR '1'='1` entirely inert.")
    ])

    add_viva_qa(26, "How does Jinja2 protect against Cross-Site Scripting (XSS)?", [
        ("Context-Aware Auto-Escaping:", "By default, Jinja2 automatically escapes all dynamic expressions `{{ variable }}`. Characters with special HTML meaning (`<`, `>`, `&`, `\"`, `'`) are converted to their safe HTML entities (`&lt;`, `&gt;`, `&amp;`, `&#34;`, `&#39;`)."),
        ("Strict Script Policy:", "We never use the `| safe` filter on unverified user-generated strings, preventing malicious attackers from injecting `<script>` payloads into resource titles or chat messages.")
    ])

    add_viva_qa(27, "How does your architecture comply with India's Digital Personal Data Protection (DPDP) Act, 2023?", [
        ("Purpose Limitation:", "Personal data (Aadhaar, MeeSeva certificates) is collected strictly for verification and never monetized or shared with third parties."),
        ("Beneficiary Privacy & Dignity:", "Underprivileged recipients upload income certificates for Admin review only. Donors only see a binary 'Verified Low-Income' badge. Financial PDFs are never publicly exposed or downloadable by peers."),
        ("Right to Erasure:", "When an account is deleted, cascaded relationships ensure personal records, documents, and messages are permanently purged.")
    ])

    add_viva_qa(28, "What is Directory Traversal and how do you prevent it in document uploads?", [
        ("The Vulnerability:", "If an attacker uploads a file named `../../../../etc/passwd` or `../../../app/routes.py`, a naive file writer would overwrite critical system files outside the upload folder."),
        ("Our Defense:", "We wrap all uploaded filenames in `werkzeug.utils.secure_filename()`, which strips path traversal sequences (`../`), slashes, and control characters, leaving only safe alphanumeric tokens.")
    ])

    add_viva_qa(29, "How do you protect against session hijacking and session fixation?", [
        ("Session Regeneration:", "Upon successful login, Flask-Login generates a brand new session identifier, invalidating any pre-authentication session tokens (preventing fixation)."),
        ("Cookie Hardening:", "Cookies are marked `HttpOnly` (immune to JavaScript retrieval via XSS) and `SameSite=Lax` (immune to CSRF transmission).")
    ])

    add_viva_qa(30, "How do you prevent malicious file uploads (e.g., executing a PHP or Python shell)?", [
        ("Multi-Layer Defense:", "1) Extension allowlist: Only `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf` are permitted. 2) Static serving: Web servers do not execute scripts inside `/static/uploads/`; files are served with MIME-type `application/octet-stream` or image headers. 3) Filenames are hashed with unique timestamps.")
    ])

    add_viva_qa(31, "How does your in-app chat ensure end-to-end authorization?", [
        ("Authorization Guard:", "In `app/core/request_routes.py`, `get_messages(req_id)` and `send_message(req_id)` explicitly verify: `if current_user.id not in [req.receiver_id, req.resource.donor_id] and current_user.role != 'admin': return 403 Forbidden`. No third party can eavesdrop on handover conversations.")
    ])

    # Category 5: Frontend & Geospatial
    add_sub_heading("5.5", "Category 5: Frontend Engineering & Geospatial Integration")

    add_viva_qa(32, "How does Leaflet.js render map tiles without lagging the client browser?", [
        ("Tile Slippy Map Architecture:", "Leaflet slices the world into $256 \\times 256$ pixel image tiles. It computes which tile coordinates $(x, y, z)$ intersect the browser viewport and downloads only visible tiles asynchronously using HTTP GET. As the user pans, off-screen tiles are purged from the DOM to conserve mobile memory.")
    ])

    add_viva_qa(33, "Why did you use OpenStreetMap instead of Google Maps API?", [
        ("Zero Cost & No Quotas:", "Google Maps requires a credit card and charges $7 per 1,000 requests after a free quota. For a free student/civic project, OpenStreetMap tiles are 100% free and open-source."),
        ("User Privacy:", "OpenStreetMap does not profile or track users across the web, aligning with our privacy-first civic mission.")
    ])

    add_viva_qa(34, "Explain how the asynchronous community ❤️ Like button works without refreshing the page.", [
        ("JavaScript Fetch Flow:", "1) User clicks heart button. 2) JavaScript intercepts event, prevents default page navigation. 3) Dispatches `fetch('/like-ngo/' + ngoId, { method: 'POST', headers: { 'X-CSRFToken': token } })`. 4) Server toggles database record and returns `{ liked: true, likes_count: 42 }`. 5) JavaScript immediately toggles `.active` CSS class and updates inner text count.")
    ])

    add_viva_qa(35, "How do you handle dark mode styling without flickering on page reload?", [
        ("CSS Variables & LocalStorage:", "Theme variables (`--bg-primary`, `--text-primary`) are defined in `:root` and `[data-theme='dark']`. JavaScript reads `localStorage.getItem('theme')` in the `<head>` tag before DOM rendering begins, setting the attribute instantly and eliminating flash of unstyled content (FOUC).")
    ])

    add_viva_qa(36, "How are UPI QR codes rendered dynamically for supported NGOs?", [
        ("Standardized UPI VPA String:", "According to NPCI specifications, UPI transactions follow the URI schema: `upi://pay?pa={upi_id}&pn={ngo_name}&cu=INR`. We feed this dynamic string into a client-side QR generation script or secure CDN API, rendering a clean, scannable QR code matching any UPI app (Google Pay, PhonePe, Paytm).")
    ])

    add_viva_qa(37, "What happens if a user disables browser GPS location permissions?", [
        ("Graceful Degradation:", "If `navigator.geolocation` fails or is denied by the user, the map falls back to a default regional center (Vizianagaram / Visakhapatnam coordinates: `[18.11, 83.40]`) and alerts the user to enter their town or pincode manually.")
    ])

    # Category 6: Scalability & Production Readiness
    add_sub_heading("5.6", "Category 6: Scalability, Production Deployment & Edge Cases")

    add_viva_qa(38, "What will break first if 100,000 active users join Seva Sankalp tomorrow, and how will you fix it?", [
        ("Bottleneck 1: SQLite File Locking:", "SQLite locks the entire database file during writes. At high concurrency, requests will queue and throw `sqlite3.OperationalError: database is locked`. Fix: Migrate immediately to PostgreSQL with connection pooling (PgBouncer)."),
        ("Bottleneck 2: In-Memory Haversine:", "Iterating 100,000 items in Python will take ~200 ms per search. Fix: Use PostGIS extension on PostgreSQL with spatial R-tree indexes (`ST_DWithin`)."),
        ("Bottleneck 3: Synchronous Email Delivery:", "Sending OTP emails blocks the worker thread for 1-2 seconds. Fix: Offload email dispatching to Celery with Redis as a message broker.")
    ])

    add_viva_qa(39, "How would you implement Redis caching in Seva Sankalp?", [
        ("High-Impact Caching Areas:", "1) Cache `/support-ngos` list in Redis with a 1-hour TTL, since approved NGO lists change infrequently. 2) Cache user leaderboard and Karma scores in a Redis Sorted Set (`ZADD` / `ZREVRANGE`) for $O(\\log N)$ instant leaderboard queries.")
    ])

    add_viva_qa(40, "How do you deploy Seva Sankalp on a production Linux server using Gunicorn and Nginx?", [
        ("Architecture:", "Nginx acts as the reverse proxy on port 80/443 handling SSL termination and static files directly. Gunicorn runs behind Nginx as the WSGI application server with $W = (2 \\times \\text{CPUs}) + 1$ worker processes communicating via a local Unix socket (`/tmp/sevasankalp.sock`).")
    ])

    add_viva_qa(41, "How does the platform handle network drops during chat messaging?", [
        ("Resilient Error Handling:", "The client-side AJAX fetch includes a `.catch(error => { showToast('Network connection lost. Message not delivered.'); button.disabled = false; })` block, preventing messages from being lost in limbo without user notification.")
    ])

    add_viva_qa(42, "What database backup strategy would you implement for production?", [
        ("Automated Strategy:", "1) Daily automated snapshots using `pg_dump` with gzip compression piped to secure AWS S3 cold storage. 2) Point-In-Time Recovery (PITR) via Write-Ahead Logging (WAL) archiving, allowing database restoration to any exact second in the past 14 days.")
    ])

    # Category 7: Future Technical Upgrades
    add_sub_heading("5.7", "Category 7: Future Technical Upgrades & Emerging Technologies")

    add_viva_qa(43, "How will production DigiLocker verification be implemented via API Setu?", [
        ("Government Integration:", "We will register Seva Sankalp as a verified consumer entity on the Government of India's **API Setu** gateway. The user will be redirected to the official DigiLocker consent screen, authenticate via Aadhaar OTP, and API Setu will return a cryptographically signed JSON/XML payload verifying their BPL or MeeSeva Income status directly to our webhook.")
    ])

    add_viva_qa(44, "How will direct Google Login be integrated?", [
        ("Google Identity Services (OAuth 2.0):", "We will configure OAuth 2.0 client credentials in Google Cloud Console, render the Google One-Tap SDK, receive a signed JWT ID token on the callback route, verify the cryptographic signature using Google's public keys via `google-auth` library, and log the user in automatically.")
    ])

    add_viva_qa(45, "How will mediated UPI payments work with Razorpay Webhooks?", [
        ("Payment Gateway Architecture:", "Instead of only showing static QR codes, donors can enter custom amounts for NGO relief campaigns. Razorpay generates an order ID, opens standard checkout, and triggers an asynchronous server webhook with a signed HMAC-SHA256 signature upon bank capture. The server verifies the signature, credits the campaign ledger, and automatically generates an 80G tax exemption PDF receipt.")
    ])

    # -------------------------------------------------------------------------
    # SECTION 6: QUICK REVISION CHEAT-SHEET
    # -------------------------------------------------------------------------
    add_sec_heading("6.", "Quick Revision Cheat-Sheet (Summary Matrix)")
    add_body("Use this rapid-fire reference matrix for the 5 minutes immediately before entering the viva defense room:")

    rev_headers = ["Parameter / Metric", "Technical Specification in Seva Sankalp", "Exam / Viva Defense Formula or Reference"]
    rev_rows = [
        ["Haversine Earth Radius (R)", "6,371.0 Kilometers", "d = 2R · atan2(√a, √(1-a)); a = sin²(Δφ/2) + cos φ₁ cos φ₂ sin²(Δλ/2)"],
        ["Electronics Cooldown Window", "365 Days (12 Months)", "(now - last_fulfilled.updated_at).days >= 365"],
        ["Household Cooldown Window", "180 Days (6 Months)", "(now - last_fulfilled.updated_at).days >= 180"],
        ["Anti-Hoarding Request Limit", "Maximum 3 Active Pending Requests", "Request.query.filter_by(receiver_id=id, status='Pending').count() < 3"],
        ["Karma Points Awarded", "50 Points per Fulfilled Exchange", "PointsTransaction(user_id=id, amount=50, type='Earned')"],
        ["Karma Velocity Cap", "Maximum 300 Points per 7 Days", "SUM(amount for last 7 days) + 50 <= 300"],
        ["Same-Network Fraud Check", "IP Collision Check (Donor vs Receiver)", "IF donor.last_login_ip == receiver.last_login_ip THEN points = 0"],
        ["Karma Badge Tiers", "Bronze: 100 | Silver: 500 | Gold: 1000 | Plat: 5000", "current_user.points_balance thresholding"],
        ["Darpan ID Regex Pattern", "14 Characters: 2 letters, 4 year, 7 digits", "^[A-Z]{2}/\\d{4}/\\d{7}$"],
        ["PAN Card Regex Pattern", "10 Characters alphanumeric", "^[A-Z]{5}[0-9]{4}[A-Z]{1}$ (4th char: C, T, or A)"],
        ["Password Hashing Algorithm", "Bcrypt (Blowfish cipher, salt, cost 12)", "bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())"],
        ["CSRF Protection Mechanism", "HMAC-SHA256 Token Injection", "Flask-WTF CSRFProtect middleware on all stateful POST requests"],
        ["Database Cascade Rule", "cascade='all, delete-orphan'", "Guarantees no orphaned messages or requests on resource deletion"],
        ["Leaflet Tile Provider", "OpenStreetMap Carto Tile Layer", "L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')"],
        ["Like Button Idempotency", "UniqueConstraint('user_id', 'ngo_id')", "Prevents duplicate likes; toggles state dynamically via AJAX"]
    ]
    add_table_data(rev_headers, rev_rows, [Inches(1.8), Inches(2.3), Inches(2.7)], font_size=8.8)

    # Save DOCX
    out_docx = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Seva_Sankalp_Technical_Architecture_and_Viva_Guide.docx"
    doc.save(out_docx)
    print(f"Successfully generated DOCX: {out_docx}")

if __name__ == "__main__":
    build_technical_dossier()
