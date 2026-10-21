import os
import shutil
import pypdf
from docx2pdf import convert

# Let's inspect which sections can have page_break=True
# Currently break=True on: 1, 3, 5, 7, 9, 11, 13, 15, 17 (9 breaks)
# If we add page_break=True to:
# 2, 4, 6, 8, 10, 12, 14, 16
# Let's see how many pages we get if ALL of them have page_break=True

def test_config(breaks_to_enable):
    with open(r'scratch/build_compact_30_page_report.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # modify the heading calls
    for sec_num in breaks_to_enable:
        old_pattern = f'add_heading_1(doc, "{sec_num}.'
        # find where it is
        idx = content.find(old_pattern)
        if idx != -1:
            end_idx = content.find(')', idx)
            line = content[idx:end_idx+1]
            if 'page_break=True' not in line:
                new_line = line[:-1] + ', page_break=True)'
                content = content[:idx] + new_line + content[end_idx+1:]

    test_script = r'scratch/temp_test_build.py'
    with open(test_script, 'w', encoding='utf-8') as f:
        f.write(content)

    import subprocess
    res = subprocess.run(['python', test_script], capture_output=True, text=True)
    print("STDOUT:", res.stdout[-300:] if res.stdout else "")
    print("STDERR:", res.stderr[-300:] if res.stderr else "")

if __name__ == '__main__':
    # Test adding breaks to 2, 4, 6, 8, 10, 12, 14, 16
    test_config([2, 4, 6, 8, 10, 12, 14, 16])
