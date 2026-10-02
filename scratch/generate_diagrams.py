import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color palette - clean grayscale/monochrome with subtle contrasts
    bg_box = '#FFFFFF'
    border_color = '#000000'
    header_fill = '#EFEFEF'
    box_fill = '#F9F9F9'
    accent_box = '#F0F0F0'

    # Title Banner
    ax.text(50, 96, "Seva Sankalp: System Infrastructure & Operational Flow", 
            ha='center', va='center', fontsize=14, fontweight='bold', fontfamily='serif')

    # 1. CLIENT TIER
    rect_client = patches.FancyBboxPatch((5, 78), 90, 14, boxstyle="round,pad=1", 
                                         ec=border_color, fc=header_fill, lw=1.5)
    ax.add_patch(rect_client)
    ax.text(50, 89, "CLIENT PRESENTATION TIER (Web & Mobile Browsers)", 
            ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')
    
    clients = [
        ("Community Donors\n(List Items, Map Picker)", 18),
        ("Grassroots Recipients\n(Search, Radius, Request)", 40),
        ("Statutory NGOs\n(Darpan ID, UPI QR)", 62),
        ("System Administrator\n(Document Approvals)", 82)
    ]
    for text, x in clients:
        box = patches.FancyBboxPatch((x-9, 79.5), 18, 7, boxstyle="round,pad=0.5", 
                                     ec=border_color, fc=bg_box, lw=1)
        ax.add_patch(box)
        ax.text(x, 83, text, ha='center', va='center', fontsize=8.5, fontfamily='serif')

    # Arrow Down
    ax.annotate('', xy=(50, 71), xytext=(50, 78),
                arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=7))
    ax.text(52, 74.5, "HTTPS Requests / Responsive Bootstrap 5 UI", fontsize=8.5, fontfamily='serif', style='italic')

    # 2. BACKEND MVC TIER (Flask WSGI)
    rect_backend = patches.FancyBboxPatch((5, 26), 90, 45, boxstyle="round,pad=1", 
                                          ec=border_color, fc=box_fill, lw=1.5)
    ax.add_patch(rect_backend)
    ax.text(50, 68, "APPLICATION LOGIC TIER (Flask WSGI & Modular Blueprints)", 
            ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')

    modules = [
        ("Authentication & RBAC (`auth_bp`)\n- Email OTP Verification via SMTP\n- Bcrypt Password Security\n- NITI Darpan & PAN Ingestion", 25, 54),
        ("Geospatial Discovery (`search_bp`)\n- Backend Haversine Distance Engine\n- OpenStreetMap & Leaflet.js Mapping\n- Real-Time Radius Filtering (1-50 km)", 75, 54),
        ("Anti-Fraud Integrity (`request_bp`)\n- 12-Month Cooldown for Electronics\n- 6-Month Cooldown for Appliances\n- Maximum 3 Concurrent Requests Cap", 25, 38),
        ("Privacy & Trust Ledger (`profile_bp`)\n- Admin-Only EWS Income Verification\n- IP Collision Check at Handover\n- Rolling 300 Karma Points Weekly Limit", 75, 38)
    ]

    for title_text, cx, cy in modules:
        box = patches.FancyBboxPatch((cx-21, cy-6), 42, 12, boxstyle="round,pad=0.5", 
                                     ec=border_color, fc=bg_box, lw=1)
        ax.add_patch(box)
        ax.text(cx, cy, title_text, ha='center', va='center', fontsize=8.5, fontfamily='serif')

    # Arrow Down
    ax.annotate('', xy=(50, 19), xytext=(50, 26),
                arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=7))
    ax.text(52, 22.5, "SQLAlchemy ORM Transactions / File System I/O", fontsize=8.5, fontfamily='serif', style='italic')

    # 3. DATA PERSISTENCE TIER
    rect_data = patches.FancyBboxPatch((5, 5), 90, 14, boxstyle="round,pad=1", 
                                       ec=border_color, fc=header_fill, lw=1.5)
    ax.add_patch(rect_data)
    ax.text(50, 16, "DATA PERSISTENCE & AUDIT TIER", 
            ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')

    db_boxes = [
        ("Relational Database (SQLAlchemy)\n`User`, `Resource`, `Request`, `DonationHistory`", 27),
        ("Anti-Fraud & Audit Ledgers\n`PointsTransaction`, `UPIDonationClick`, `Message`", 73)
    ]
    for text, x in db_boxes:
        box = patches.FancyBboxPatch((x-20, 6.5), 40, 7, boxstyle="round,pad=0.5", 
                                     ec=border_color, fc=bg_box, lw=1)
        ax.add_patch(box)
        ax.text(x, 10, text, ha='center', va='center', fontsize=8.5, fontfamily='serif')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

def create_flowchart_diagram(output_path):
    fig, ax = plt.subplots(figsize=(9, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    border_color = '#000000'
    bg_box = '#FFFFFF'
    accent_box = '#F5F5F5'

    ax.text(50, 97, "Seva Sankalp: Request Validation & Anti-Fraud Flowchart", 
            ha='center', va='center', fontsize=13, fontweight='bold', fontfamily='serif')

    # Step 1: Start
    box1 = patches.FancyBboxPatch((25, 89), 50, 5, boxstyle="round,pad=0.5", ec=border_color, fc=accent_box, lw=1.5)
    ax.add_patch(box1)
    ax.text(50, 91.5, "Beneficiary Submits Resource Request", ha='center', va='center', fontsize=9.5, fontweight='bold', fontfamily='serif')

    # Arrow 1
    ax.annotate('', xy=(50, 84), xytext=(50, 89), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))

    # Step 2: Decision 1 (Account Approved)
    diamond1 = patches.Polygon([[50, 84], [72, 78], [50, 72], [28, 78]], closed=True, ec=border_color, fc=bg_box, lw=1.5)
    ax.add_patch(diamond1)
    ax.text(50, 78, "Is Beneficiary\nAccount Approved?", ha='center', va='center', fontsize=8.5, fontfamily='serif')

    # Reject 1 (Right)
    ax.annotate('', xy=(85, 78), xytext=(72, 78), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(75, 79.5, "NO", fontsize=8, fontweight='bold', fontfamily='serif')
    box_rej1 = patches.FancyBboxPatch((80, 75.5), 18, 5, boxstyle="square,pad=0.2", ec=border_color, fc='#EAEAEA', lw=1)
    ax.add_patch(box_rej1)
    ax.text(89, 78, "Block: ID Approval\nRequired by Admin", ha='center', va='center', fontsize=7.5, fontfamily='serif')

    # Arrow Down (YES)
    ax.annotate('', xy=(50, 67), xytext=(50, 72), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(52, 69.5, "YES", fontsize=8, fontweight='bold', fontfamily='serif')

    # Step 3: Decision 2 (Outstanding Impact Proof)
    diamond2 = patches.Polygon([[50, 67], [72, 61], [50, 55], [28, 61]], closed=True, ec=border_color, fc=bg_box, lw=1.5)
    ax.add_patch(diamond2)
    ax.text(50, 61, "Pending Proof for\nPast Received Item?", ha='center', va='center', fontsize=8.5, fontfamily='serif')

    # Reject 2 (Right)
    ax.annotate('', xy=(85, 61), xytext=(72, 61), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(75, 62.5, "YES", fontsize=8, fontweight='bold', fontfamily='serif')
    box_rej2 = patches.FancyBboxPatch((80, 58.5), 18, 5, boxstyle="square,pad=0.2", ec=border_color, fc='#EAEAEA', lw=1)
    ax.add_patch(box_rej2)
    ax.text(89, 61, "Block: Must Upload\nPast Impact Proof", ha='center', va='center', fontsize=7.5, fontfamily='serif')

    # Arrow Down (NO)
    ax.annotate('', xy=(50, 50), xytext=(50, 55), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(52, 52.5, "NO", fontsize=8, fontweight='bold', fontfamily='serif')

    # Step 4: Decision 3 (Low Income Gating)
    diamond3 = patches.Polygon([[50, 50], [72, 44], [50, 38], [28, 44]], closed=True, ec=border_color, fc=bg_box, lw=1.5)
    ax.add_patch(diamond3)
    ax.text(50, 44, "High-Value Item?\n(Low-Income Gated)", ha='center', va='center', fontsize=8.5, fontfamily='serif')

    # Branch Right for Low Income Check
    ax.annotate('', xy=(85, 44), xytext=(72, 44), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(74, 45.5, "YES", fontsize=8, fontweight='bold', fontfamily='serif')
    box_e1 = patches.FancyBboxPatch((80, 41.5), 18, 5, boxstyle="square,pad=0.2", ec=border_color, fc='#EAEAEA', lw=1)
    ax.add_patch(box_e1)
    ax.text(89, 44, "Check Admin-Verified\nIncome Certificate", ha='center', va='center', fontsize=7.5, fontfamily='serif')

    # Arrow Down (NO or Passed)
    ax.annotate('', xy=(50, 33), xytext=(50, 38), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(52, 35.5, "NO / PASS", fontsize=7.5, fontweight='bold', fontfamily='serif')

    # Step 5: Decision 4 (Anti-Flipping Cooldown)
    diamond4 = patches.Polygon([[50, 33], [72, 27], [50, 21], [28, 27]], closed=True, ec=border_color, fc=bg_box, lw=1.5)
    ax.add_patch(diamond4)
    ax.text(50, 27, "Cooldown Lock Active?\n(Electronics: 365d\nHousehold: 180d)", ha='center', va='center', fontsize=8, fontfamily='serif')

    # Reject 3 (Right)
    ax.annotate('', xy=(85, 27), xytext=(72, 27), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(74, 28.5, "YES", fontsize=8, fontweight='bold', fontfamily='serif')
    box_rej3 = patches.FancyBboxPatch((80, 24.5), 18, 5, boxstyle="square,pad=0.2", ec=border_color, fc='#EAEAEA', lw=1)
    ax.add_patch(box_rej3)
    ax.text(89, 27, "Block: Anti-Flipping\nCooldown Active", ha='center', va='center', fontsize=7.5, fontfamily='serif')

    # Arrow Down (NO)
    ax.annotate('', xy=(50, 16), xytext=(50, 21), arrowprops=dict(facecolor='black', width=1.2, headwidth=6))
    ax.text(52, 18.5, "NO", fontsize=8, fontweight='bold', fontfamily='serif')

    # Step 6: Success
    box_success = patches.FancyBboxPatch((20, 8), 60, 8, boxstyle="round,pad=0.5", ec=border_color, fc=accent_box, lw=1.5)
    ax.add_patch(box_success)
    ax.text(50, 12, "Request Approved & Created\n- Donor Notified via In-App Alert & Email\n- In-App Chat Opened for Secure Physical Handover\n- IP Tracking Applied at Handover to Stop Self-Farming", 
            ha='center', va='center', fontsize=8.5, fontfamily='serif')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    create_architecture_diagram(r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\scratch\figure_4_1_architecture.png")
    create_flowchart_diagram(r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\scratch\figure_4_2_flowchart.png")
