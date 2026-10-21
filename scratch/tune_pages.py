import os
import re

with open(r'scratch/build_compact_30_page_report.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'add_heading_1' in line:
        print(f"Line {i+1}: {line.strip()}")
