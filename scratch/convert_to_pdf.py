import os
import shutil
from docx2pdf import convert

docx_path = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Seva_Sankalp_Complete_Project_Report.docx"
pdf_path = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker\Seva_Sankalp_Complete_Project_Report.pdf"
brain_pdf_path = r"C:\Users\SANDAKA ANISH NIHAAL\.gemini\antigravity\brain\0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2\Seva_Sankalp_Complete_Project_Report.pdf"

print(f"Converting {docx_path} to PDF...")
convert(docx_path, pdf_path)

if os.path.exists(pdf_path):
    print(f"Successfully generated PDF: {pdf_path}")
    shutil.copy2(pdf_path, brain_pdf_path)
    print(f"Successfully copied to brain artifacts: {brain_pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
else:
    print("PDF conversion failed.")
