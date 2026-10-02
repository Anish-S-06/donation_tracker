import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def generate_humanized_flowchart(output_path):
    # High resolution 16:9 canvas (3840 x 2160 equivalent at 300 DPI)
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 105)
    ax.axis('off')

    # Color Palette: Warm, Humanized, Clean & Professional
    c_bg = '#FDFBF9'              # Warm off-white ivory canvas
    c_text_dark = '#1C2826'       # Deep warm charcoal
    c_text_muted = '#556360'      # Soft warm slate
    c_primary = '#D84315'         # Warm terracotta
    c_primary_soft = '#FDF0ED'    # Soft terracotta pastel
    c_secondary = '#2E7D32'       # Forest green
    c_secondary_soft = '#EBF5EE'  # Soft forest green pastel
    c_blue = '#1E6091'            # Muted civic blue
    c_blue_soft = '#EDF4F9'       # Soft civic blue pastel
    c_amber = '#D96B00'           # Warm amber
    c_amber_soft = '#FFF8EE'      # Soft amber pastel
    c_card_bg = '#FFFFFF'         # Crisp white card fill
    c_card_border = '#E0E6E2'     # Subtle border
    c_shadow = '#EFEAE4'          # Gentle shadow

    # Background
    fig.patch.set_facecolor(c_bg)
    ax.set_facecolor(c_bg)

    # -------------------------------------------------------------
    # HEADER SECTION
    # -------------------------------------------------------------
    ax.text(10, 98.5, "M E T H O D O L O G Y   /   S Y S T E M   D E S I G N", 
            fontsize=10.5, fontweight='bold', color=c_primary, fontfamily='sans-serif')
    ax.text(10, 94.2, "Seva Sankalp: Complete Operational Lifecycle Flowchart", 
            fontsize=19, fontweight='bold', color=c_text_dark, fontfamily='sans-serif')
    ax.text(10, 90.8, "A human-centered system design: From identity verification to dignified resource sharing & direct NGO support", 
            fontsize=10.2, color=c_text_muted, fontfamily='sans-serif')

    # Top Right College Crest
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'uploads', 'profile_photos', 'user_4.gif')
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path)
            ax_logo = fig.add_axes([0.84, 0.85, 0.11, 0.11])
            ax_logo.imshow(logo_img)
            ax_logo.axis('off')
        except Exception as e:
            print("Logo load error:", e)

    # Helper: Draw clean card with drop shadow and perfectly spaced title + subtitle
    def draw_card(x, y, w, h, title, subtitle="", badge="", badge_color=c_primary, fill=c_card_bg, border=c_card_border, title_color=c_text_dark):
        # Drop Shadow
        shadow = patches.FancyBboxPatch((x + 0.4, y - 0.45), w, h, boxstyle="round,pad=0.5,rounding_size=0.8", 
                                        ec="none", fc=c_shadow, lw=0, zorder=2)
        ax.add_patch(shadow)

        # Main Box
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=0.8", 
                                     ec=border, fc=fill, lw=1.3, zorder=3)
        ax.add_patch(box)

        # Top Badge Pill
        if badge:
            badge_w = len(badge) * 0.65 + 2.5
            badge_box = patches.FancyBboxPatch((x + 1.2, y + h - 0.8), badge_w, 2.0, boxstyle="round,pad=0.2,rounding_size=0.6",
                                              ec=badge_color, fc=badge_color, lw=0.8, zorder=4)
            ax.add_patch(badge_box)
            ax.text(x + 1.2 + badge_w/2, y + h + 0.2, badge, ha='center', va='center', 
                    fontsize=6.8, fontweight='bold', color='#FFFFFF', zorder=5)

        # Content positioning with generous vertical space
        if subtitle:
            ax.text(x + w/2, y + h * 0.65, title, ha='center', va='center', 
                    fontsize=8.8, fontweight='bold', color=title_color, zorder=5)
            ax.text(x + w/2, y + h * 0.32, subtitle, ha='center', va='center', 
                    fontsize=7.2, color=c_text_muted, zorder=5, linespacing=1.38, multialignment='center')
        else:
            ax.text(x + w/2, y + h * 0.5, title, ha='center', va='center', 
                    fontsize=8.8, fontweight='bold', color=title_color, zorder=5)

    # Helper: Draw smooth connecting arrows
    def draw_arrow(x1, y1, x2, y2, label="", label_pos=0.5, color=c_text_muted, style='->', lw=1.3):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=3, shrinkB=3,
                                    mutation_scale=12, capstyle='round'), zorder=4)
        if label:
            lx = x1 + (x2 - x1) * label_pos
            ly = y1 + (y2 - y1) * label_pos + 1.2
            ax.text(lx, ly, label, ha='center', va='center', fontsize=7.2, fontweight='bold', color=color,
                    bbox=dict(boxstyle="round,pad=0.25", fc=c_bg, ec="none", alpha=0.95), zorder=6)

    # -------------------------------------------------------------
    # PHASE 1: ONBOARDING & TRUST VERIFICATION
    # -------------------------------------------------------------
    band1 = patches.FancyBboxPatch((8, 65.5), 164, 22.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                                   ec='#E4ECE6', fc='#F4F8F5', lw=1, zorder=1)
    ax.add_patch(band1)
    ax.text(11, 85.5, "PHASE 1: CITIZEN & NGO ONBOARDING WITH TRUST VERIFICATION", 
            fontsize=8.8, fontweight='bold', color=c_secondary, zorder=2)

    # Card 1: Registration
    draw_card(12, 67.5, 27, 13.5, "1. Portal Registration", 
              "Citizen (Donor/Recipient)\nor Verified NGO Partner\n(Email OTP + Password)", 
              badge="ENTRY", badge_color=c_secondary)

    draw_arrow(39, 74.25, 47, 74.25)

    # Card 2: Verification Submission
    draw_card(48, 67.5, 29, 13.5, "2. Identity Verification", 
              "Citizens: Aadhaar / PAN / Govt ID\nNGOs: NITI Darpan ID,\nOrg PAN & Auth Letter", 
              badge="KYC / AUDIT", badge_color=c_primary)

    draw_arrow(77, 74.25, 84, 74.25)

    # Decision Diamond 1: Admin Review (Centered at x=90, y=74.25)
    diamond1 = patches.Polygon([[90, 79.5], [97, 74.25], [90, 69.0], [83, 74.25]], closed=True, 
                               ec=c_amber, fc=c_amber_soft, lw=1.5, zorder=4)
    ax.add_patch(diamond1)
    ax.text(90, 75.1, "Admin Review:", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_amber, zorder=5)
    ax.text(90, 73.1, "Docs Valid?", ha='center', va='center', fontsize=7.5, color=c_amber, zorder=5)

    # Rejection Branch (Upward, centered above diamond at x=90)
    draw_arrow(90, 79.5, 90, 81.5, label="NO", label_pos=0.5, color='#C62828')
    draw_card(76, 82.2, 28, 4.6, "Account Pending / Rejected", 
              "User notified via email with review notes", fill='#FFEBEE', border='#FFCDD2', title_color='#C62828')

    # Approval Branch (Rightward)
    draw_arrow(97, 74.25, 107, 74.25, label="YES", label_pos=0.45, color=c_secondary)

    # Card 3: Verified Account
    draw_card(108, 67.5, 30, 13.5, "3. Verified Member Portal", 
              "Verified Badge Granted\nFull Community Features Unlocked\n(Profile, Listings, Requests)", 
              badge="VERIFIED", badge_color=c_secondary, fill=c_secondary_soft, border='#C8E6C9')

    # Connecting Pipe from Phase 1 to Phase 2:
    # Goes out right of Card 3, drops cleanly down outside the content area, then merges to center
    draw_arrow(138, 74.25, 150, 74.25)
    draw_arrow(150, 74.25, 150, 62.5)
    draw_arrow(150, 62.5, 90, 62.5)
    draw_arrow(90, 62.5, 90, 58.5)

    # -------------------------------------------------------------
    # PHASE 2: THREE EMPOWERING COMMUNITY STREAMS
    # -------------------------------------------------------------
    band2 = patches.FancyBboxPatch((8, 27.5), 164, 34.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                                   ec='#EFEBE5', fc='#FAF7F2', lw=1, zorder=1)
    ax.add_patch(band2)
    ax.text(11, 59.8, "PHASE 2: THREE COMMUNITY PATHWAYS (NEIGHBOR-TO-NEIGHBOR & DIRECT NGO GIVING)", 
            fontsize=8.8, fontweight='bold', color=c_primary, zorder=2)

    # Distribution bar across the 3 columns (at y = 56.5)
    draw_arrow(90, 58.5, 30, 58.5)
    draw_arrow(30, 58.5, 30, 53.5)

    draw_arrow(90, 58.5, 90, 53.5)

    draw_arrow(90, 58.5, 150, 58.5)
    draw_arrow(150, 58.5, 150, 53.5)

    # STREAM A: COMMUNITY DONORS (Left Column, x = 14 to 46, center = 30)
    ax.text(30, 52.0, "STREAM A: COMMUNITY DONORS", fontsize=8.2, fontweight='bold', color=c_primary, ha='center', zorder=2)
    draw_card(14, 41.5, 32, 8.8, "A1. List Essential Item", 
              "Clothing, Books, Gadgets, Food\nAdd Photo, Condition, Category", 
              badge="DONATE", badge_color=c_primary)
    draw_arrow(30, 41.5, 30, 38.5)
    draw_card(14, 29.5, 32, 8.8, "A2. Map Pin & EWS Gating", 
              "Set Pickup Location via Map Pin\nOptional: Restrict to Low-Income (EWS)", 
              badge="LOCATION", badge_color=c_primary)

    # STREAM B: RECIPIENTS IN NEED (Center Column, x = 74 to 106, center = 90)
    ax.text(90, 52.0, "STREAM B: RECIPIENTS IN NEED", fontsize=8.2, fontweight='bold', color=c_blue, ha='center', zorder=2)
    draw_card(74, 41.5, 32, 8.8, "B1. Explore Map & Radius", 
              "Browse 4-Col Responsive Catalog\nFilter by Category & 1-50 km Radius", 
              badge="DISCOVER", badge_color=c_blue)
    draw_arrow(90, 41.5, 90, 38.5)
    draw_card(74, 29.5, 32, 8.8, "B2. Anti-Fraud Request Guard", 
              "• Max 3 Concurrent Requests Cap\n• Anti-Flipping Cooldown (180-365d)\n• Past Received Item Proof Check", 
              badge="FAIR USE", badge_color=c_amber, fill=c_amber_soft, border='#FFE0B2')

    # STREAM C: DIRECT NGO GIVING (Right Column, x = 134 to 166, center = 150)
    ax.text(150, 52.0, "STREAM C: VERIFIED GRASSROOT NGOS", fontsize=8.2, fontweight='bold', color=c_secondary, ha='center', zorder=2)
    draw_card(134, 41.5, 32, 8.8, "C1. Browse Verified NGOs", 
              "NITI Darpan Authenticated Causes\nView Mission, Photos & Social Impact", 
              badge="NGO PARTNER", badge_color=c_secondary)
    draw_arrow(150, 41.5, 150, 38.5)
    draw_card(134, 29.5, 32, 8.8, "C2. 100% Direct UPI Giving", 
              "Scan Native UPI QR Code\nZero Platform Cuts or Middlemen\nInstant Transparent Support", 
              badge="DIRECT UPI", badge_color=c_secondary, fill=c_secondary_soft, border='#C8E6C9')

    # -------------------------------------------------------------
    # PHASE 3 & 4: MUTUAL AGREEMENT, SAFE HANDOVER & IMPACT
    # -------------------------------------------------------------
    band3 = patches.FancyBboxPatch((8, 3), 164, 21.5, boxstyle="round,pad=0.6,rounding_size=1.2",
                                   ec='#E2ECE5', fc='#F2F8F4', lw=1, zorder=1)
    ax.add_patch(band3)
    ax.text(11, 22.5, "PHASE 3 & 4: SAFE MUTUAL HANDOVER, PROOF OF IMPACT & GAMIFIED RECOGNITION", 
            fontsize=8.8, fontweight='bold', color=c_secondary, zorder=2)

    # Routing from Stream A & Stream B into Request Review:
    # Routes in neutral space at y = 25.5 (between Band 2 and Band 3), avoiding all text
    draw_arrow(30, 29.5, 30, 25.5)
    draw_arrow(30, 25.5, 41, 25.5)
    
    draw_arrow(90, 29.5, 90, 25.5)
    draw_arrow(90, 25.5, 41, 25.5)
    draw_arrow(41, 25.5, 41, 18.5)

    # Decision Diamond 2: Donor Request Review (Centered at x=41, y=13.5)
    diamond2 = patches.Polygon([[41, 18.5], [49, 13.5], [41, 8.5], [33, 13.5]], closed=True,
                               ec=c_amber, fc=c_amber_soft, lw=1.5, zorder=4)
    ax.add_patch(diamond2)
    ax.text(41, 14.3, "Donor Review:", ha='center', va='center', fontsize=7.6, fontweight='bold', color=c_amber, zorder=5)
    ax.text(41, 12.5, "Accept Request?", ha='center', va='center', fontsize=7.6, color=c_amber, zorder=5)

    # Request Declined Branch (Downward)
    draw_arrow(41, 8.5, 41, 5)
    draw_arrow(41, 5, 49, 5, label="NO", label_pos=0.45, color='#C62828')
    draw_card(50, 3.8, 23, 4.4, "Request Declined", "Item remains active in catalog", 
              fill='#FFEBEE', border='#FFCDD2', title_color='#C62828')

    # Request Accepted Branch (Rightward)
    draw_arrow(49, 13.5, 62, 13.5, label="YES", label_pos=0.45, color=c_secondary)

    # Card 4: In-App Private Chat
    draw_card(63, 6.8, 30, 13.5, "4. In-App Private Chat", 
              "Secure coordination channel\nSafe pickup meeting scheduled\nZero phone number exposure", 
              badge="SAFE HANDOVER", badge_color=c_primary)

    draw_arrow(93, 13.5, 102, 13.5)

    # Card 5: Physical Handover & Impact Proof
    draw_card(103, 6.8, 32, 13.5, "5. Handover & Impact Proof", 
              "Physical item handover confirmed\nBeneficiary uploads receipt photo\nAnti-self-farming IP check logged", 
              badge="VERIFIED USE", badge_color=c_secondary)

    draw_arrow(135, 13.5, 144, 13.5)

    # Card 6: Community Karma Rewards
    draw_card(145, 6.8, 25, 13.5, "6. Community Karma", 
              "Donor receives Karma Points\nWeekly 300 pts fair limit\nBronze/Silver/Gold/Platinum", 
              badge="LEADERBOARD", badge_color=c_primary, fill=c_primary_soft, border='#FFCCBC', title_color=c_primary)

    # Bottom Footer
    ax.text(90, 1.2, "Seva Sankalp • Academic B.Tech Project System Design • 100% Direct Community Impact • Open-Access & Transparent", 
            ha='center', va='center', fontsize=7.8, color='#8E9A96', fontfamily='sans-serif', style='italic')
    ax.text(170, 1.2, "Slide 9", ha='center', va='center', fontsize=9, fontweight='bold', color=c_text_muted, fontfamily='sans-serif')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated clean humanized flowchart: {output_path}")

if __name__ == '__main__':
    out_path = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\scratch\seva_sankalp_system_design_flowchart.png"
    generate_humanized_flowchart(out_path)
