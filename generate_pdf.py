import markdown
from fpdf import FPDF, HTMLMixin
import os

class PDF(FPDF, HTMLMixin):
    pass

def generate_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    html_content = markdown.markdown(md_content)
    
    # Add basic HTML boilerplate
    html = f"""
    <font face="Arial" size="12">
    {html_content}
    </font>
    """
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.write_html(html)
    pdf.output(pdf_path)

if __name__ == '__main__':
    md_file = r'C:\Users\SANDAKA ANISH NIHAAL\.gemini\antigravity\brain\0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2\Documentation.md'
    pdf_file = r'C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Donation_Tracker_Documentation.pdf'
    
    try:
        generate_pdf(md_file, pdf_file)
        print(f"Successfully created PDF at {pdf_file}")
    except Exception as e:
        print(f"Error: {e}")
