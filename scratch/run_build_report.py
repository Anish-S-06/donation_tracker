import os
import sys
import shutil

# Add current scratch path to sys.path
scratch_dir = os.path.dirname(os.path.abspath(__file__))
if scratch_dir not in sys.path:
    sys.path.insert(0, scratch_dir)

from build_arduino_r24_report_part1 import build_document
from build_arduino_r24_report_part2 import add_sections_1_to_6
from build_arduino_r24_report_part3 import add_sections_7_to_12
from build_arduino_r24_report_part4 import add_sections_13_to_17

def main():
    print("Initializing document...")
    doc = build_document()
    
    print("Appending Sections 1 to 6...")
    doc = add_sections_1_to_6(doc)
    
    print("Appending Sections 7 to 12...")
    doc = add_sections_7_to_12(doc)
    
    print("Appending Sections 13 to 17...")
    doc = add_sections_13_to_17(doc)
    
    # Destination Paths
    proj_dir = r"C:\Users\SANDAKA ANISH NIHAAL\donation_tracker"
    artifact_dir = r"C:\Users\SANDAKA ANISH NIHAAL\.gemini\antigravity\brain\0c0befe5-ef6a-4fa5-bcf3-701edc32bbd2"
    
    docx_filename = "Arduino_Environmental_Monitoring_System_Project_Report.docx"
    pdf_filename = "Arduino_Environmental_Monitoring_System_Project_Report.pdf"
    
    out_docx_proj = os.path.join(proj_dir, docx_filename)
    out_docx_artifact = os.path.join(artifact_dir, docx_filename)
    
    out_pdf_proj = os.path.join(proj_dir, pdf_filename)
    out_pdf_artifact = os.path.join(artifact_dir, pdf_filename)
    
    print(f"Saving DOCX to: {out_docx_proj}")
    doc.save(out_docx_proj)
    
    print(f"Copying DOCX to artifacts: {out_docx_artifact}")
    shutil.copyfile(out_docx_proj, out_docx_artifact)
    
    print("Converting DOCX to PDF...")
    pdf_created = False
    try:
        from docx2pdf import convert
        convert(out_docx_proj, out_pdf_proj)
        shutil.copyfile(out_pdf_proj, out_pdf_artifact)
        print("PDF conversion with docx2pdf succeeded!")
        pdf_created = True
    except Exception as e:
        print(f"docx2pdf conversion note: {e}, attempting win32com...")
        try:
            import win32com.client
            word = win32com.client.DispatchEx("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
            in_file = os.path.abspath(out_docx_proj)
            out_file = os.path.abspath(out_pdf_proj)
            doc_com = word.Documents.Open(in_file)
            doc_com.SaveAs(out_file, FileFormat=17) # 17 = wdFormatPDF
            doc_com.Close()
            word.Quit()
            shutil.copyfile(out_pdf_proj, out_pdf_artifact)
            print("PDF conversion with win32com succeeded!")
            pdf_created = True
        except Exception as e2:
            print(f"win32com conversion note: {e2}")

    print("\n=======================================================")
    print("SUCCESS: Document generation complete!")
    print(f"Word Document (.docx): {out_docx_proj}")
    if pdf_created:
        print(f"PDF Document (.pdf): {out_pdf_proj}")
    print("=======================================================")

if __name__ == "__main__":
    main()
