import os
import subprocess
import pypdf

# Let's read build_compact_30_page_report.py
with open(r'scratch/build_compact_30_page_report.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Enable page breaks for all 17 sections
for sec_num in [2, 4, 6, 8, 10, 12, 14, 16]:
    old_str = f'add_heading_1(doc, "{sec_num}.'
    idx = code.find(old_str)
    if idx != -1:
        end_idx = code.find(')', idx)
        line = code[idx:end_idx+1]
        if 'page_break=True' not in line:
            new_line = line[:-1] + ', page_break=True)'
            code = code[:idx] + new_line + code[end_idx+1:]

# Now let's try option A: add page break before ABSTRACT
# Let's find ABSTRACT
code_a = code.replace('r = p.add_run("ABSTRACT")', 'doc.add_page_break()\n    p = doc.add_paragraph()\n    r = p.add_run("ABSTRACT")', 1)

# And option B: also add page break before STUDENT DECLARATION
code_b = code_a.replace('r = p.add_run("STUDENT DECLARATION")', 'doc.add_page_break()\n    p = doc.add_paragraph()\n    r = p.add_run("STUDENT DECLARATION")', 1)

# Write code_b to test script and run
with open(r'scratch/temp_test_30.py', 'w', encoding='utf-8') as f:
    f.write(code_b)

print("Running temp_test_30.py...")
res = subprocess.run(['python', r'scratch/temp_test_30.py'], capture_output=True, text=True)
print(res.stdout[-200:] if res.stdout else "")

reader = pypdf.PdfReader('Arduino_Environmental_Monitoring_System_Project_Report.pdf')
print("FINAL PAGE COUNT WITH B:", len(reader.pages))
