from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Seva Sankalp - Technology Stack Documentation', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(4)
        
    def chapter_body(self, body):
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 6, body)
        self.ln(4)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Backend
pdf.chapter_title('1. Backend Architecture')
pdf.chapter_body('''\
Framework: Flask (Python 3)
Flask is a lightweight WSGI web application framework. The project uses the Flask Application Factory pattern (`create_app`) and Blueprints to divide the application into modular components (Core, Auth, Frontend, Admin, etc.) making it highly scalable and maintainable.

Server / Hosting Platform: PythonAnywhere (Production), Werkzeug (Development)
The platform is hosted on PythonAnywhere, utilizing its WSGI server capabilities.

Database: SQLite (Development) / MariaDB (Production ready via SQLAlchemy)
SQLite is used for local database management.

ORM (Object-Relational Mapping): Flask-SQLAlchemy
Used to map Python classes (User, Resource, Request, DonationHistory, Message, etc.) to database tables. It abstracts raw SQL into Pythonic code.

Database Migrations: Flask-Migrate (Alembic)
Handles database schema updates and version control safely without losing data.
''')

# Frontend
pdf.chapter_title('2. Frontend Technologies')
pdf.chapter_body('''\
Markup & Structure: HTML5 (Jinja2 Templating Engine)
Jinja2 enables dynamic HTML generation (e.g., loops, conditionals) directly from the Flask backend before sending it to the user.

Styling Framework: Bootstrap 5 (CSS & JavaScript components)
Provides responsive grid systems, modals, offcanvas sidebars, and pre-built UI components ensuring a mobile-first, professional design.

Custom Styling: Vanilla CSS3
Custom gradients (text-gradient, bg-gradient-primary), glassmorphism effects, hover micro-animations, and premium shadow utilities to achieve a modern, rich aesthetic.

Icons: Bootstrap Icons (bi-icons) & FontAwesome
Used extensively for UI indicators, badges, and navigation icons.

Notifications: Toastify-JS
A lightweight JavaScript library used to display non-intrusive, elegant "toast" notifications in the corner of the screen for success/error messages.
''')

# Mapping & Geolocation
pdf.chapter_title('3. Geolocation & Mapping System')
pdf.chapter_body('''\
Mapping Library: Leaflet.js
An open-source JavaScript library used for mobile-friendly interactive maps on the "Search & Map" page.

Map Tiles: OpenStreetMap (OSM)
Provides the actual graphical map tiles rendered by Leaflet.

Geolocation API: HTML5 Navigator Geolocation
Used to capture the user's real-time latitude and longitude to filter nearby resources. Includes a fallback mechanism where users can manually click the map to set their location if GPS fails.

Distance Calculations: Haversine Formula (Backend Python)
A mathematical formula implemented in the backend to calculate the precise distance (in kilometers) between two coordinates over the earth's spherical surface, used for strict radius filtering.
''')

# Authentication & Security
pdf.chapter_title('4. Authentication & Security')
pdf.chapter_body('''\
Session Management: Flask-Login
Handles user sessions, `current_user` proxies, and route protection decorators (e.g., `@login_required`).

Password Hashing: Bcrypt
A strong, computationally expensive cryptographic hash function used to securely store user passwords.

Email Verification (OTP): Flask-Mail
Configured with an SMTP server (Gmail) to send 6-digit One-Time Passwords (OTPs) to verify user emails during registration.

Role-Based Access Control (RBAC): Custom Python Decorators
Custom `@role_required` decorators are implemented to strictly lock down specific routes (e.g., Admin Dashboard) to authorized users only.

CSRF Protection: Flask-WTF / Secure Forms (Implicit)
Protects against Cross-Site Request Forgery attacks.
''')

# Core Features & Logic
pdf.chapter_title('5. Core Platform Features & Integrations')
pdf.chapter_body('''\
Real-Time Messaging System:
Built with AJAX (fetch API) and backend Python polling to allow Donors and Receivers to communicate about pickup details securely.

Gamification & Anti-Fraud System:
Karma Points and Dynamic Badges (Bronze to Platinum). Includes real-time IP Address fingerprinting and a 7-day rolling Point Cap algorithm to prevent "Sybil Attacks" and point-farming fraud.

Cascading Cleanups (Data Integrity):
Strict SQLAlchemy relationships to ensure that when a resource or user is deleted, all associated chat messages, donation histories, and requests are safely purged.

File Handling: Werkzeug (Secure Filename) & Pillow (PIL)
Handles secure uploading of User ID Documents, NGO Gallery photos, and Resource Impact Proof photos.
''')

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.gemini', 'antigravity', 'brain', '0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2', 'Tech_Stack_Documentation.pdf'))

pdf.output(output_path)
print(f"PDF generated successfully at {output_path}")
