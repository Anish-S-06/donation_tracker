import re

with open(r'scratch/temp_test_30.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update toc_rows
old_toc = '''    toc_rows = [
        ["Front Matter", "Certificate, Student Declaration, Acknowledgements, Technical Abstract", "Pages 1 – 3"],
        ["1", "Introduction and Project Overview: Industrial Context, Edge Philosophy, and Educational Value", "Pages 5 – 6"],
        ["2", "Problem Statement, Engineering Objectives, and Formal Scope Boundaries", "Pages 6 – 7"],
        ["3", "Theoretical Foundations: Embedded MCUs, Transducers, ADC Quantization, and I2C Buses", "Pages 8 – 9"],
        ["4", "System Architecture, Functional/Non-Functional Specs, Block Diagrams, and Data Pipelines", "Pages 10 – 11"],
        ["5", "Hardware Component Analysis: ATmega328P Core, HD44780 LCD, and Breadboard Interconnects", "Pages 11 – 12"],
        ["6", "Transducer Physics: TMP36 Silicon Bandgap, DHT11 Hygrometry, and MQ-135 SnO2 Chemiresistance", "Pages 13 – 15"],
        ["7", "Virtual Prototyping & EDA Simulation Workflow in Autodesk Tinkercad Circuits", "Pages 15 – 16"],
        ["8", "Comprehensive Circuit Schematic, Master Pin Interconnections, and Grounding Architecture", "Pages 17 – 18"],
        ["9", "Firmware Architecture, Cooperative State Scheduling, Conversion Algorithms, and Fault Traps", "Pages 19 – 20"],
        ["10", "Complete Virtual Firmware Implementation (Annotated Tinkercad C++ Source Code)", "Pages 21 – 22"],
        ["11", "Physical Hardware Implementation, Bill of Materials, Benchtop Assembly, and Power Budget", "Pages 22 – 24"],
        ["12", "Production Physical Firmware Implementation, Toolchain Setup, and Dual-Line Visualization", "Pages 24 – 26"],
        ["13", "Experimental Testing, Multi-Stage Calibration Protocols, and Empirical Benchtop Test Logs", "Pages 26 – 27"],
        ["14", "Results Discussion, Sensor Limitations, Cross-Sensitivity Analysis, and Laboratory Safety", "Pages 27 – 28"],
        ["15", "Engineering Component Specification, Project Timeline Schedule, and Future Roadmap", "Pages 28 – 29"],
        ["16", "Comprehensive Project Conclusions, Architectural Syntheses, and Final Reflections", "Pages 29 – 30"],
        ["17", "Technical Glossary, Formal References, Standards, and Verification Checklist", "Pages 30 – 31"]
    ]'''

new_toc = '''    toc_rows = [
        ["Front Matter", "Certificate, Student Declaration, Acknowledgements, Technical Abstract", "Pages 1 – 6"],
        ["1", "Introduction and Project Overview: Industrial Context, Edge Philosophy, and Educational Value", "Page 7"],
        ["2", "Problem Statement, Engineering Objectives, and Formal Scope Boundaries", "Pages 8 – 9"],
        ["3", "Theoretical Foundations: Embedded MCUs, Transducers, ADC Quantization, and I2C Buses", "Page 10"],
        ["4", "System Architecture, Functional/Non-Functional Specs, Block Diagrams, and Data Pipelines", "Page 11"],
        ["5", "Hardware Component Analysis: ATmega328P Core, HD44780 LCD, and Breadboard Interconnects", "Page 12"],
        ["6", "Transducer Physics: TMP36 Silicon Bandgap, DHT11 Hygrometry, and MQ-135 SnO2 Chemiresistance", "Pages 13 – 14"],
        ["7", "Virtual Prototyping & EDA Simulation Workflow in Autodesk Tinkercad Circuits", "Page 15"],
        ["8", "Comprehensive Circuit Schematic, Master Pin Interconnections, and Grounding Architecture", "Page 16"],
        ["9", "Firmware Architecture, Cooperative State Scheduling, Conversion Algorithms, and Fault Traps", "Page 17"],
        ["10", "Complete Virtual Firmware Implementation (Annotated Tinkercad C++ Source Code)", "Pages 18 – 19"],
        ["11", "Physical Hardware Implementation, Bill of Materials, Benchtop Assembly, and Power Budget", "Page 20"],
        ["12", "Production Physical Firmware Implementation, Toolchain Setup, and Dual-Line Visualization", "Pages 21 – 22"],
        ["13", "Experimental Testing, Multi-Stage Calibration Protocols, and Empirical Benchtop Test Logs", "Page 23"],
        ["14", "Results Discussion, Sensor Limitations, Cross-Sensitivity Analysis, and Laboratory Safety", "Page 24"],
        ["15", "Engineering Component Specification, Project Timeline Schedule, and Future Roadmap", "Pages 25 – 26"],
        ["16", "Comprehensive Project Conclusions, Architectural Syntheses, and Final Reflections", "Page 27"],
        ["17", "Technical Glossary, Formal References, Standards, and Verification Checklist", "Pages 28 – 30"]
    ]'''

assert old_toc in code, "old_toc not found in code!"
code = code.replace(old_toc, new_toc)

with open(r'scratch/build_compact_30_page_report.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_compact_30_page_report.py successfully updated with final layout and page numbers!")
