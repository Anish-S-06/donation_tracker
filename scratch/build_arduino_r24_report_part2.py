import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from build_arduino_r24_report import (
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_body,
    add_bullet,
    add_callout,
    add_code_block,
    add_styled_table
)
from build_arduino_r24_report_part1 import build_document

def add_sections_1_to_6(doc):
    # =========================================================================
    # 1. INTRODUCTION AND PROJECT OVERVIEW
    # =========================================================================
    add_heading_1(doc, "1. Introduction and Project Overview")
    
    add_heading_2(doc, "1.1 The Imperative for Modern Environmental Monitoring")
    add_body(doc, "In an era marked by rapid industrialization, dense urbanization, and increasing climate variability, the continuous observation and real-time assessment of environmental parameters have transitioned from specialized meteorological pursuits into essential public health, occupational safety, and residential well-being priorities. The atmosphere within our immediate living, educational, and working spaces exerts a direct, quantifiable influence on human physiology, cognitive focus, respiratory health, and overall comfort. Parameters such as ambient temperature, relative humidity, and the ambient concentration of noxious gases, volatile chemical compounds, and airborne combustion byproducts govern both acute physical sensations and long-term biological outcomes.")
    add_body(doc, "Historically, environmental data collection relied predominantly on bulky, prohibitively expensive, and centralized laboratory-grade measurement stations operated by municipal agencies or industrial conglomerates. While these flagship installations achieve exceptional analytical precision and comply strictly with federal reference standards, their substantial capital cost, complex maintenance regimens, and physical scarcity create substantial spatial and temporal data voids. A municipal monitoring station positioned five kilometers away from an academic building or indoor laboratory provides virtually no actionable intelligence regarding localized toxic vapor buildup, sudden thermal spikes caused by equipment overheating, or stagnant ventilation pockets within individual architectural enclosures.")
    add_body(doc, "To bridge this fundamental resolution gap, modern instrumentation engineering increasingly embraces decentralized, micro-scale sensor architectures. The emergence of open-source computing platforms, ubiquitous microcontrollers, and mass-manufactured solid-state transducers has catalyzed a democratizing revolution across environmental telemetry. Compact, low-power embedded monitoring stations can now be fabricated and deployed at a minor fraction of traditional costs, enabling hyper-local, continuous tracking of microclimates and internal air masses.")
    add_body(doc, "This project details the systematic conceptualization, virtual simulation, algorithmic development, and physical realization of an autonomous, Arduino-based environmental monitoring station. Specifically engineered to track ambient temperature, relative humidity, and broad-spectrum gaseous responses in real time, the system balances pedagogical transparency with rigorous engineering execution, delivering instantaneous visual feedback through a standardized liquid-crystal interface while logging serial diagnostic telemetry for in-depth data interrogation.")

    add_heading_2(doc, "1.2 Project Architectural Concept and Philosophy")
    add_body(doc, "The core engineering philosophy underpinning this project revolves around modularity, low barrier to deployment, strict operational determinism, and transparent operational boundaries. In contrast to complex Internet-of-Things (IoT) architectures that enforce total reliance on remote cloud servers, continuous Wi-Fi infrastructure, third-party proprietary APIs, and active network connections, this design prioritizes a self-contained, fully autonomous edge-computing paradigm.")
    add_body(doc, "By decoupling core environmental monitoring from network dependencies, the station ensures continuous, fail-safe measurement even in remote field environments, subterranean academic laboratories, electrical enclosures, or network-denied testing facilities. The fundamental workflow is architected around a classical tripartite embedded pipeline comprising sensing, processing, and localized presentation stages:")
    
    add_bullet(doc, "1. Transduction & Sensing Stage", "Solid-state physical and electro-chemical transducers continuously detect thermodynamic variations and chemical adsorption phenomena in the surrounding atmosphere, converting these subtle physical shifts into proportional analog voltages and serialized digital pulse trains.")
    add_bullet(doc, "2. Central Microcontroller Processing Stage", "An ATmega328P microcontroller running customized firmware performs high-frequency sampling, analog-to-digital conversion, voltage normalization, mathematical linearizations, multi-stage non-blocking temporal scheduling, and qualitative threshold categorization.")
    add_bullet(doc, "3. Presentation & Diagnostic Feedback Stage", "An alphanumeric 16x2 Liquid Crystal Display interfaced via a two-wire Inter-Integrated Circuit (I2C) serial backpack renders continuous, human-readable alternating metrics, supplemented concurrently by high-baud-rate serial telemetry transmitted over Universal Asynchronous Receiver-Transmitter (UART) for engineering debugging and computational analysis.")

    add_heading_2(doc, "1.3 Pedagogical Value and Practical Utility")
    add_body(doc, "Beyond its immediate utility as a functioning benchtop instrument, the project serves as an extensive educational blueprint uniting multiple fundamental disciplines across electrical engineering, sensor physics, embedded firmware architecture, and instrumentation metrology. Key pedagogical competencies cultivated throughout the design lifecycle include:")
    add_bullet(doc, "Analog Sensor Interfacing & Quantization", "Mastery of voltage divider networks, source impedance matching, analog reference noise, and 10-bit successive approximation register (SAR) ADC quantization.")
    add_bullet(doc, "Digital Protocol Synchronization", "Hands-on implementation of single-bus proprietary timing protocols (DHT11) alongside multi-master synchronous serial I2C bus protocols utilizing PCF8574 port expanders.")
    add_bullet(doc, "Simulation-to-Hardware Bridge", "Clear delineation between idealized computer simulations conducted within Autodesk Tinkercad Circuits and the messy, nonlinear realities of physical breadboard assembly, characterized by thermal parasitic drifts, contact resistance, and lead inductances.")
    add_bullet(doc, "Metrological Realism & Honest Labelling", "Recognizing the acute engineering distinction between qualitative gas detection and certified, quantitative air quality index (AQI) instrumentation, ensuring students develop professional metrological integrity.")

    add_callout(doc, "Design Philosophy Note", "A dependable embedded instrumentation system prioritizes deterministic local operation before expanding into cloud connectivity. Local display and serial diagnostics ensure that the primary safety and observation functions remain uncompromised by network failures.")

    # =========================================================================
    # 2. PROBLEM STATEMENT, ENGINEERING OBJECTIVES, AND PROJECT SCOPE
    # =========================================================================
    add_heading_1(doc, "2. Problem Statement, Engineering Objectives, and Project Scope")
    
    add_heading_2(doc, "2.1 Problem Formulation")
    add_body(doc, "Educational laboratories, shared workshops, makerspaces, and residential study rooms frequently suffer from subtle, unrecognized environmental deterioration. Fluctuations in ambient temperature and relative humidity directly impair human concentration, foster microbial growth, and compromise delicate electronic prototypes or 3D printing filaments. Concurrently, the accumulation of volatile organic chemicals (VOCs), combustible gases, alcohol fumes, or stagnant carbon dioxide caused by poor ventilation or localized chemical soldering activities presents chronic comfort and health hazards.")
    add_body(doc, "However, contemporary institutions and student developers face a pronounced dilemma when seeking environmental monitoring solutions. Commercial multi-gas air quality monitors are either high-cost proprietary systems with closed firmware, or inexpensive consumer consumer-grade gadgets that present unverified, black-box 'air quality percentages' without disclosing sensor calibration curves, sensor cross-sensitivities, or measurement baselines. Conversely, open-source hobby tutorials frequently overcomplicate early implementations by mandating cloud subscriptions, complex wireless shields, and unstable Wi-Fi libraries before basic sensor physics and local conversion routines are verified.")
    add_body(doc, "Therefore, an urgent academic need exists for an open, robust, low-cost, and meticulously documented environmental monitoring instrument. Such a system must operate reliably on standard 5V power, perform transparent sensor conversions, present immediate physical feedback on a local screen, and maintain honest metrological boundaries that explicitly educate users regarding sensor capabilities and physical constraints.")

    add_heading_2(doc, "2.2 Formal Project Objectives")
    add_body(doc, "To resolve the formulated problem comprehensively, the project pursued seven primary engineering objectives spanning simulation, firmware development, hardware realization, and metrological validation:")
    add_bullet(doc, "1. Virtual Schematic & Algorithmic Validation", "Design and construct an end-to-end interactive circuit simulation within Autodesk Tinkercad Circuits featuring an Arduino Uno R3, an analog TMP36 temperature sensor, a six-terminal heated gas sensor model, and an I2C Liquid Crystal Display.")
    add_bullet(doc, "2. Deterministic Mathematical Conversion", "Develop robust firmware mathematical conversion routines to translate raw ADC quantization counts (0-1023) into precise voltages and calibrated degrees Celsius based on published sensor transfer functions.")
    add_bullet(doc, "3. Dual-Stage Air Quality Response Mapping", "Formulate a multi-tier threshold algorithm that classifies broad-spectrum gas sensor analog voltages into intuitive qualitative states (GOOD, MODERATE, POOR, DANGER) alongside an arbitrary 0-100 demonstration response scale.")
    add_bullet(doc, "4. Physical Hardware Migration Architecture", "Formulate a rigorous component substitution and transition roadmap replacing simulation-exclusive components with real-world physical parts—specifically adopting the digital DHT11 for simultaneous temperature and relative humidity telemetry, and the MQ-135 metal oxide semiconductor breakout board.")
    add_bullet(doc, "5. High-Efficiency Non-Blocking Display Management", "Structure the production firmware using millisecond timestamp scheduling (millis()) rather than processor-halting delay loops, ensuring fluid multi-page LCD presentation and high-responsiveness.")
    add_bullet(doc, "6. System Assembly, Debugging, and Validation", "Fabricate the complete physical breadboard circuit, perform systematic benchtop voltage verification, and record repeatable baseline sensor behavior under varied environmental exposures.")
    add_bullet(doc, "7. Critical Metrological & Safety Profiling", "Document in exhaustive detail the exact physical operating limits, sensor warm-up cycles, thermal drift behaviors, cross-sensitivities, and safety handling requirements associated with internal sensor heating elements.")

    add_heading_2(doc, "2.3 Project Scope and Boundary Constraints")
    add_body(doc, "To maintain rigorous engineering focus and guarantee thorough execution within resource and timeframe allocations, explicit boundaries were established for the project scope:")
    add_body(doc, "**In Scope:** Complete electronic schematic design; Tinkercad simulation logic; breadboard physical implementation; low-level C++ Arduino firmware; I2C LCD backpack communication; UART serial data stream diagnostics; DHT11 single-bus digital decoding; MQ-135 analog voltage acquisition; educational threshold classification logic; and comparative error analysis.")
    add_body(doc, "**Out of Scope:** Long-range wireless telemetry (Wi-Fi, LoRa, Bluetooth, Zigbee); cloud platform integration (ThingSpeak, Adafruit IO, AWS IoT); battery charging management and ultra-low-power sleep states; automated mechanical ventilation actuations (relays, fans, motorized dampers); and certified regulatory Air Quality Index (AQI) compliance.")

    t21_headers = ["Project Domain", "Included In Project Scope", "Explicitly Out of Scope", "Engineering Rationale"]
    t21_widths = [Inches(1.5), Inches(1.7), Inches(1.6), Inches(1.7)]
    t21_rows = [
        ["Microcontroller Platform", "Arduino Uno R3 (ATmega328P 16MHz DIP)", "ESP32, STM32, ARM Cortex-M microcontrollers", "Maximized pedagogical clarity and standardized 5V logic compatibility."],
        ["Thermal Telemetry", "TMP36 (Simulation), DHT11 (Physical)", "PT100 RTD, Thermocouples, Calibrated SHT35", "Provides basic 0-50°C measurement sufficient for room temperature study."],
        ["Gas & Air Sensing", "Tinkercad 6-terminal model, MQ-135 module", "Photoionization Detectors (PID), NDIR CO2 sensors", "Balances affordability (<₹250) with broad-spectrum gas sensitivity."],
        ["Display & Feedback", "16x2 character LCD with PCF8574 I2C backpack", "OLED graphics displays, Nextion HMI touchscreens", "Minimizes wiring complexity down to 4 pins while ensuring readability."],
        ["Network & Connectivity", "UART Serial Monitor over USB A-to-B at 9600 baud", "MQTT, HTTP REST APIs, Cloud dashboards", "Eliminates network latency, router configuration, and cloud downtime."],
        ["Metrological Classification", "Qualitative 4-tier classroom demonstration scale", "Government certified AQI, PM2.5/PM10 metrics", "Prevents false reliance on uncalibrated consumer metal oxide sensors."]
    ]
    add_styled_table(doc, "Table 2.1: Formal Scope Boundary and Deliverable Matrix", t21_headers, t21_rows, t21_widths)

    # =========================================================================
    # 3. THEORETICAL FOUNDATIONS AND TECHNICAL CONCEPTS
    # =========================================================================
    add_heading_1(doc, "3. Theoretical Foundations and Technical Concepts")
    
    add_heading_2(doc, "3.1 Architecture of Embedded Microcontroller Systems")
    add_body(doc, "An embedded system represents an integrated computational assembly of hardware processing silicon, specialized memory hierarchies, peripheral input/output circuitry, and dedicated control software designed to execute an unbroken deterministic sequence of real-time tasks. In stark contrast to general-purpose desktop computing systems that run multi-tasking operating systems with arbitrary scheduling and high power dissipation, embedded microcontroller units (MCUs) are engineered for direct physical interaction with the electrical domain.")
    add_body(doc, "At the core of the Arduino Uno R3 development board resides the Microchip (formerly Atmel) ATmega328P—an 8-bit high-performance AVR enhanced RISC architecture microcontroller. Operating at a crystal-stabilized clock frequency of 16 MHz, the ATmega328P achieves throughputs approaching 16 MIPS (Million Instructions Per Second) by executing powerful single-clock-cycle instructions. The silicon die integrates 32 Kilobytes of in-system self-programmable Flash memory for firmware instruction storage, 2 Kilobytes of static Random Access Memory (SRAM) for runtime dynamic variable allocation, and 1 Kilobyte of Electrically Erasable Programmable Read-Only Memory (EEPROM) for non-volatile parameter retention.")
    add_body(doc, "The functional bridge between the digital logic core and external environmental sensors is provided by the internal peripheral controllers: General Purpose Input/Output (GPIO) registers, hardware timer/counters, a programmable UART serial engine, a Two-Wire Interface (TWI/I2C) hardware module, and an integrated multi-channel Analog-to-Digital Converter.")

    add_heading_2(doc, "3.2 Transducers and Physical Sensing Principles")
    add_body(doc, "In measurement and instrumentation science, a transducer is formally defined as any physical device that transforms an input energy or variable belonging to one physical domain into a corresponding, measurable signal in another domain—almost universally the electrical domain. Environmental transducers encompass two distinct operational subclasses: sensors and actuators. Sensors serve as input transducers, converting thermodynamic, optical, acoustic, or chemical variations into measurable voltages, currents, or impedance changes.")
    add_body(doc, "The physical transducers employed in this monitoring platform represent distinct transducer classifications. The TMP36 temperature sensor utilizes solid-state semiconductor physics, exploiting the temperature-dependent base-emitter junction voltage (Vbe) differential of forward-biased silicon bipolar transistors. In contrast, the MQ-135 chemical sensor relies upon surface adsorption chemistry on polycrystalline metal-oxide semiconductors (specifically Tin Dioxide, SnO2), where gaseous molecules alter electrical conduction through donor electron transfer. Finally, the DHT11 sensor pairs a negative temperature coefficient (NTC) thermistor with a capacitive humidity polymer whose dielectric permittivity fluctuates in direct thermodynamic equilibrium with ambient water vapor molecules.")

    add_heading_2(doc, "3.3 Principles of Analog-to-Digital Conversion (ADC)")
    add_body(doc, "Because physical phenomena such as temperature and chemical concentration manifest as continuous analog variables across infinite voltage spectra, an analog-to-digital converter is required to discretize these signals into finite digital representations that an 8-bit digital processing core can manipulate. The ATmega328P incorporates an internal 10-bit Successive Approximation Register (SAR) ADC connected through an internal analog multiplexer to six external pins (designated A0 through A5).")
    add_body(doc, "**Quantization Resolution:** A 10-bit binary representation subdivides the operational voltage reference spectrum into 2^10 = 1024 discrete quantized voltage increments (steps ranging numerically from 0 to 1023). When utilizing the default reference configuration, the ADC is tied directly to the positive 5.0 V microcontroller system supply rail (Vcc). Consequently, the fundamental step size—known as the Least Significant Bit (LSB) voltage resolution—is mathematically determined as:")
    add_body(doc, "V_LSB = V_ref / (2^10 - 1) = 5.000 V / 1023 ≈ 0.0048876 V (4.888 mV per count)")
    add_body(doc, "To convert an observed integer ADC quantization count (ADC_val) back into its equivalent physical input voltage (V_in), the firmware applies the standard transfer equation:")
    add_body(doc, "V_in = ADC_val * (V_ref / 1023.0)")
    add_body(doc, "**Systemic Error Considerations:** While theoretically straightforward, practical ADC quantization in breadboard environments is susceptible to multiple real-world error sources. Fluctuations in the USB supply voltage (which frequently dips to 4.75 V or surges to 5.20 V depending on computer host load) directly skew V_ref, producing proportional percentage errors in raw voltage calculations. Furthermore, input source impedance exceeding 10 kΩ, thermal noise across breadboard spring contacts, and lack of external ceramic bypass capacitors can cause sample-and-hold capacitor settling errors during rapid multi-channel analog switching.")

    add_heading_2(doc, "3.4 The Inter-Integrated Circuit (I2C) Protocol")
    add_body(doc, "Parallel alphanumeric displays historically required up to 16 physical electrical conductors, demanding at least 6 dedicated microcontroller GPIO pins for basic 4-bit data transfers (Register Select, Enable, and data lines D4-D7). In microcontroller platforms with constrained pin counts, this parallel overhead exhausts available inputs. To solve this dilemma, the instrumentation system utilizes the Inter-Integrated Circuit (I2C) serial bus protocol developed by Philips Semiconductor (now NXP).")
    add_body(doc, "The I2C bus utilizes a synchronous, multi-master, multi-slave, bidirectional serial architecture requiring only two active signal lines alongside common power and ground rails: Serial Data (SDA) and Serial Clock (SCL). Both SDA and SCL are designed with open-drain/open-collector outputs pulled high to the positive supply rail through external pull-up resistors (typically 4.7 kΩ to 10 kΩ). On the Arduino Uno R3, hardware I2C peripheral lines are mapped physically to analog pins A4 (SDA) and A5 (SCL), as well as duplicated on dedicated header pins adjacent to AREF.")
    add_body(doc, "Data transmission proceeds via byte-framed packet transfers governed strictly by the clock signal generated by the master (Arduino). Communication begins with a START condition (SDA pulled LOW while SCL remains HIGH), followed by a 7-bit slave address byte, a Read/Write direction bit, an Acknowledge (ACK/NACK) bit from the peripheral, one or more 8-bit data payload bytes, and a STOP condition (SDA released HIGH while SCL remains HIGH). In this project, an on-board PCF8574 8-bit remote I/O expander chip mounted to the rear of the LCD decodes the I2C serial stream and drives the parallel HD44780 display controller with zero pin waste on the Arduino.")

    add_heading_2(doc, "3.5 Comparative Analysis: Simulation vs. Physical Hardware")
    add_body(doc, "A foundational lesson emphasized throughout this project is that computer-based Electronic Design Automation (EDA) simulations represent highly idealized behavioral abstractions rather than complete physical replicas. While web-based simulation platforms such as Autodesk Tinkercad Circuits provide immense instructional value for verifying schematic routing, testing conditional logic, and debugging display formatting without risk of component burnout, real-world hardware manifests physical complexities that simulations fundamentally omit.")
    add_body(doc, "In simulation, internal resistance in connecting jumper wires is modeled as precisely zero; supply rails never experience ripple or sag; analog sensors exhibit instantaneous thermal equilibrium without response latency; and environmental noise is virtually absent. In physical hardware, ambient thermal gradients, stray parasitic capacitance, mechanical vibration across breadboard contacts, atmospheric humidity variations, and chemical sensor heater warm-up cycles profoundly influence signal stability. Recognizing and designing robust firmware to accommodate these physical phenomena represents a core milestone of real-world instrumentation engineering.")

    add_callout(doc, "Metrological Insight", "Simulation proves functional logic; physical prototyping validates environmental physics. High ADC precision on a computer screen cannot compensate for supply rail fluctuations or uncalibrated sensor cross-sensitivities on a physical breadboard.")

    # =========================================================================
    # 4. SYSTEM ARCHITECTURE AND DETAILED ENGINEERING SPECIFICATIONS
    # =========================================================================
    add_heading_1(doc, "4. System Architecture and Detailed Engineering Specifications")
    
    add_heading_2(doc, "4.1 Comprehensive Functional Requirements")
    add_body(doc, "The primary purpose of an environmental monitoring instrument is to deliver predictable, reliable, and uninterrupted telemetry under nominal operating conditions. To ensure rigorous performance verification during testing, the functional requirements of the system were explicitly codified:")
    add_bullet(doc, "Continuous Dual-Domain Sampling", "The instrument must periodically sample ambient thermal parameters (temperature and humidity) and atmospheric chemical response voltages at deterministic, non-blocking time intervals.")
    add_bullet(doc, "On-Chip Signal Linearization", "The microcontroller firmware must ingest raw 10-bit integer ADC counts, translate them into true floating-point physical voltages, and evaluate mathematical equations to compute accurate temperature in degrees Celsius.")
    add_bullet(doc, "Qualitative Gas Categorization", "The system must map raw analog chemical sensor voltages onto an intuitive demonstration response scale (0 to 100) and assign one of four discrete operational status tiers: GOOD, MODERATE, POOR, or DANGER.")
    add_bullet(doc, "Local Visual Telemetry Presentation", "An integrated 16x2 alphanumeric LCD display must cycle automatically through structured informational screens, displaying temperature, relative humidity, qualitative air status, and response metrics with high legibility.")
    add_bullet(doc, "Asynchronous Engineering Serial Stream", "The microcontroller must output formatted ASCII debug streams over its hardware UART serial port at 9600 baud, enabling benchtop instrumentation logging and real-time computer diagnostics.")

    add_heading_2(doc, "4.2 Rigorous Non-Functional Requirements")
    add_body(doc, "In addition to baseline functional tasks, the physical instrument was engineered to comply with demanding non-functional criteria governing usability, electrical robustness, maintainability, and educational accessibility:")
    add_bullet(doc, "Ultra-Low Fabrication Cost", "Total component acquisition costs for the entire instrument prototype must remain below ₹1,500 ($18 USD), ensuring high replicability across academic institutions and student workshops.")
    add_bullet(doc, "Solderless, Non-Destructive Assembly", "All physical subsystems must interconnect via standard 2.54 mm pitch breadboards and DuPont jumper cables, eliminating required soldering while preserving component integrity for future experiments.")
    add_bullet(doc, "Deterministic Timing & Responsiveness", "Firmware execution must never freeze or enter indefinite blocking states; sensor sampling must execute deterministically every 2000 to 3000 milliseconds using hardware timer counters.")
    add_bullet(doc, "High Legibility & Humanized Interface", "Display layouts must be formatted cleanly with intuitive abbreviated labels, correct SI units, and high contrast, avoiding cluttered technical jargon.")
    add_bullet(doc, "Electrical Supply Integrity", "Total system power dissipation must remain strictly within standard USB 2.0 host current capabilities (500 mA maximum), preventing host port overcurrent shutdowns during sensor heater operation.")

    add_heading_2(doc, "4.3 System Block Diagram and Architectural Layout")
    add_body(doc, "The high-level system architecture follows a clear hierarchical flow separating the physical environment, transduction layer, central processing core, and human machine interface (HMI):")
    add_body(doc, "The **Physical Environment** continuously presents dynamic thermal energy and airborne gas concentrations. These variables encounter the **Transduction Layer**, which comprises either the TMP36/analog gas model in simulation or the DHT11/MQ-135 module in physical hardware.")
    add_body(doc, "The **Central Processing Core** consists of the ATmega328P microcontroller mounted on the Arduino Uno development board. Within this core, hardware peripherals (ADC multiplexer, Timer0, TWI/I2C peripheral, and USART) execute signal conditioning, quantization, non-blocking temporal dispatching, and mathematical state mapping.")
    add_body(doc, "Finally, the **Human Machine Interface Layer** renders the processed intelligence across two distinct feedback channels: the local 16x2 I2C LCD for direct physical user observation and the USB Serial UART diagnostic stream for remote serial terminal logging.")

    add_heading_2(doc, "4.4 Sequential End-to-End Data Flow Pipeline")
    add_body(doc, "The functional lifecycle of every telemetry sample proceeds through an eight-stage execution pipeline within the microcontroller:")
    add_bullet(doc, "1. Temporal Trigger Evaluation", "The main execution loop queries the internal millisecond timer (millis()). If the elapsed duration since the prior acquisition cycle is less than the scheduled interval (3000 ms), the loop yields immediately without blocking CPU cycles.")
    add_bullet(doc, "2. Temperature/Humidity Acquisition", "The microcontroller issues a start pulse to the digital DHT11 sensor and decodes the incoming 40-bit pulse-width-modulated pulse train, extracting integer temperature and humidity values. In simulation, an analog voltage is read from pin A1.")
    add_bullet(doc, "3. ADC Multiplexing & Gas Acquisition", "The internal ADC multiplexer switches to analog channel A0, charges the sample-and-hold capacitor, and initiates a 10-bit conversion cycle, reading the MQ-135 analog voltage.")
    add_bullet(doc, "4. Validation & Error Checking", "The firmware checks the temperature and humidity results against IEEE NaN (Not-a-Number) float conditions. If communication failure is detected, an explicit error state is dispatched to the display.")
    add_bullet(doc, "5. Algorithmic Transformation", "Raw gas ADC values (0-1023) are mapped linearly onto the demonstration scale (0-100) and evaluated against defined conditional boundaries to assign the appropriate qualitative status string.")
    add_bullet(doc, "6. Serial Diagnostic Dispatch", "All instantaneous floating-point values, raw integer ADC counts, scaled response percentages, and assigned status categories are formatted into a human-readable ASCII text block and transmitted over UART.")
    add_bullet(doc, "7. Local Display Update", "The microcontroller transmits byte commands over the I2C bus to the PCF8574 backpack, updating the 16x2 LCD character memory with fresh readings.")
    add_bullet(doc, "8. State Timestamp Refresh", "The last-update timestamp is synchronized to current millis(), preparing the system for the subsequent deterministic measurement cycle.")

    add_callout(doc, "Architecture Highlight", "Implementing non-blocking state scheduling using millis() instead of delay() ensures that the microcontroller remains responsive to serial commands, button interrupts, or secondary timing routines without sacrificing display stability.")

    # =========================================================================
    # 5. HARDWARE COMPONENT ANALYSIS AND MODULE SPECIFICATIONS
    # =========================================================================
    add_heading_1(doc, "5. Hardware Component Analysis and Module Specifications")
    
    add_heading_2(doc, "5.1 Central Processing Unit: Arduino Uno R3")
    add_body(doc, "The central computing engine selected for this project is the Arduino Uno R3 development board, built around the Microchip ATmega328P 8-bit AVR microcontroller. The board operates at a standard system clock frequency of 16 MHz supplied by an on-board ceramic resonator, delivering predictable instruction execution timing. Operating at an industry-standard 5.0 V logic level, the Uno provides seamless electrical compatibility with standard sensors and displays without requiring bidirectional logic level shifting circuits.")
    add_body(doc, "The board features 14 digital input/output pins (of which 6 provide hardware 8-bit Pulse Width Modulation output), 6 analog inputs mapped directly to the internal 10-bit ADC multiplexer, an on-board 5V low-dropout voltage regulator (NCP1117ST50), and a dedicated secondary ATmega16U2 microcontroller functioning as a high-speed USB-to-serial converter. The board can be powered directly via a standard USB A-to-B cable from a host computer or through an external DC barrel jack accepting an unregulated 7 to 12 V input. Its rugged design, socketed DIP microcontroller IC, and resilient polyfuse overcurrent protection make it the premier choice for educational electronics prototyping.")

    add_heading_2(doc, "5.2 Alphanumeric Display: 16x2 Character LCD with I2C Backpack")
    add_body(doc, "Visual feedback is delivered through a standard 16-character by 2-row alphanumeric Liquid Crystal Display built upon the industry-standard Hitachi HD44780 dot-matrix LCD controller. In its native configuration, an HD44780 requires a minimum of 6 GPIO connections in 4-bit mode alongside separate power, contrast, and backlight wiring—a total of 16 electrical pins that rapidly overwhelm introductory microcontrollers.")
    add_body(doc, "To overcome this wiring complexity, the display module is paired with a pre-soldered I2C backpack board based on the NXP PCF8574 remote 8-bit I/O expander. The PCF8574 interfaces with the Arduino over the standard two-wire I2C bus (SDA and SCL), receiving byte commands and converting them into parallel nibbles that drive the HD44780 controller. The backpack incorporates a precision multi-turn trimmer potentiometer for adjusting display contrast, an onboard jumper for enabling or disabling the LED backlight, and solderable address jumpers (A0, A1, A2) allowing the default 7-bit slave address to be configured between 0x27 and 0x3F. This elegant subsystem reduces the total electrical interface between the display and microcontroller to four wires: VCC, GND, SDA, and SCL.")

    add_heading_2(doc, "5.3 Prototyping Infrastructure and Interconnects")
    add_body(doc, "Reliable prototyping requires high-quality electrical interconnects and robust mechanical mounting. The physical circuit is constructed upon an 830-tie-point solderless breadboard featuring two continuous power distribution rails along each perimeter and 126 five-point terminal strips spanning the center divider. The internal spring contacts are fabricated from phosphor bronze with nickel plating, designed to accommodate standard 22-26 AWG solid core wire leads.")
    add_body(doc, "Interconnections between the Arduino Uno headers, breadboard bus strips, and sensor pin headers are completed using color-coded multi-strand copper DuPont jumper cables (male-to-male and male-to-female). Adhering to strict electrical conventions, black and blue cables are reserved exclusively for Ground (GND), red and orange cables for 5.0 V positive supply (VCC), yellow cables for analog signals (A0, A1), and green/white cables for digital and I2C buses (D2, SDA, SCL). This disciplined color coding prevents catastrophic wiring errors during assembly and troubleshooting.")

    t51_headers = ["Subsystem / Component", "Key Technical Parameter", "Specified Value", "Functional Significance"]
    t51_widths = [Inches(1.5), Inches(1.6), Inches(1.7), Inches(1.7)]
    t51_rows = [
        ["Arduino Uno R3", "Microcontroller Core", "Microchip ATmega328P (8-bit AVR RISC)", "Executes main firmware control loop."],
        ["Arduino Uno R3", "Clock Frequency / Flash", "16.0 MHz / 32 KB Flash Memory", "Guarantees deterministic execution and timing."],
        ["Arduino Uno R3", "Operating Voltage & I/O", "5.0 V DC Logic / 20 mA max per I/O pin", "Matches sensor voltage rails without level shifters."],
        ["16x2 LCD Display", "Display Format & Font", "16 characters x 2 rows (5x8 dot matrix)", "Presents clean, two-line text metrics."],
        ["I2C LCD Backpack", "Interface IC / Default Addr", "PCF8574T (I2C to 8-bit parallel) / 0x27 or 0x3F", "Reduces display wiring down to two communication wires."],
        ["Solderless Breadboard", "Tie-Point Distribution", "830 tie-points (630 terminal + 200 power rail)", "Enables modular, non-destructive circuit prototyping."],
        ["DuPont Interconnects", "Conductor Specifications", "24 AWG multi-strand copper, 2.54 mm pitch", "Ensures low-resistance electrical connections."]
    ]
    add_styled_table(doc, "Table 5.1: Technical Specifications of Core Hardware Modules", t51_headers, t51_rows, t51_widths)

    # =========================================================================
    # 6. TRANSDUCER PHYSICS AND ENVIRONMENTAL SENSOR PRINCIPLES
    # =========================================================================
    add_heading_1(doc, "6. Transducer Physics and Environmental Sensor Principles")
    
    add_heading_2(doc, "6.1 Analog Thermal Transducer: TMP36 Precision Sensor")
    add_body(doc, "The TMP36 is a low-voltage, precision centigrade temperature sensor fabricated by Analog Devices. The device operates on the fundamental physical principle of the silicon bandgap temperature sensor, exploiting the predictable thermodynamic relationship governing the base-emitter voltage difference (ΔVbe) between two identical bipolar transistors operating at differing collector current densities. This differential voltage is inherently proportional to absolute temperature in Kelvin (PTAT - Proportional to Absolute Temperature).")
    add_body(doc, "Internal signal conditioning circuitry linearizes and amplifies this core thermal voltage, producing an analog output that is directly proportional to temperature in degrees Celsius. Crucially, the TMP36 incorporates an intentional 500 mV (0.50 V) DC offset at 0°C. This deliberate offset allows the sensor to measure negative temperatures down to -40°C without requiring a negative dual-rail power supply. The output voltage scaling factor is exactly 10.0 mV/°C. Consequently, the mathematical transfer function converting measured output voltage (V_out) into temperature (T_C) is expressed as:")
    add_body(doc, "T_C = (V_out - 0.500 V) * 100 °C/V")
    add_body(doc, "For example, when the sensor is exposed to a nominal room temperature of 25.0°C, the output pin produces an electrical potential of: V_out = 0.500 V + (25.0 * 0.010 V) = 0.750 V. The sensor operates over a broad supply voltage span of 2.7 V to 5.5 V, consumes less than 50 µA of quiescent current, and exhibits low self-heating (less than 0.1°C in still air), making it an exceptional thermal reference in simulation and introductory physical laboratories.")

    add_heading_2(doc, "6.2 Digital Environmental Transducer: DHT11 Temperature & Relative Humidity Sensor")
    add_body(doc, "The DHT11 is an integrated composite environmental sensor module manufactured by Aosong Electronics, capable of delivering calibrated digital output for both temperature and relative humidity. The module incorporates two distinct physical transducers paired with an internal 8-bit OTP (One-Time Programmable) microcontroller that performs analog acquisition, factory calibration coefficient mapping, and digital serial encoding.")
    add_body(doc, "Relative humidity measurement is performed via a resistive-capacitive humidity sensing component. The transducer features a moisture-sensitive hygroscopic dielectric polymer layer sandwiched between two permeable gold electrodes. As atmospheric humidity shifts, water vapor molecules enter thermodynamic equilibrium with the polymer film, altering its dielectric constant and electrical impedance. Simultaneously, temperature is measured via an integrated Negative Temperature Coefficient (NTC) ceramic thermistor whose electrical resistance decreases non-linearly with increasing thermal energy.")
    add_body(doc, "The onboard microcontroller continuously measures these elements, looks up factory calibration coefficients stored in internal OTP memory, and converts the readings into a single-bus digital data stream. The communication protocol utilizes a custom single-wire bidirectional serial bus. The master microcontroller (Arduino) initiates communication by pulling the shared data line LOW for at least 18 milliseconds, followed by a 20-40 microsecond HIGH pull-up. The DHT11 responds with an 80 microsecond LOW acknowledgement, followed by 40 consecutive data bits: 16 bits of humidity data (integer and decimal), 16 bits of temperature data (integer and decimal), and an 8-bit checksum byte that guarantees communication integrity.")

    add_heading_2(doc, "6.3 Chemiresistive Metal-Oxide Gas Transducer: MQ-135 Sensor")
    add_body(doc, "The MQ-135 is a broad-spectrum chemiresistive gas sensor belonging to the widely utilized MQ family manufactured by Zhengzhou Winsen Electronics. The core sensing element consists of a micro-machined ceramic tube (Al2O3) coated with a thin polycrystalline layer of Tin Dioxide (SnO2), enclosing an internal Nickel-Chromium (Ni-Cr) resistance heating coil. The sensor operates on the fundamental physical chemistry of high-temperature gas adsorption and surface redox reactions.")
    add_body(doc, "When the internal heater coil is energized with a continuous 5.0 V DC supply, the SnO2 sensing layer is heated to its optimal operating temperature of approximately 300°C to 400°C. In clean ambient air, atmospheric oxygen molecules adsorb onto the crystalline surfaces of the Tin Dioxide particles, capturing conduction-band donor electrons to form negatively charged chemisorbed oxygen ions (O- and O2-). This electron trapping creates a significant potential energy barrier between adjacent crystal grains, resulting in high baseline electrical resistance (R0).")
    add_body(doc, "When the heated sensor encounters reducing gases or target volatile pollutants—such as carbon dioxide (CO2), ammonia (NH3), benzene (C6H6), alcohol vapors, or smoke—these gaseous molecules undergo oxidation reactions with the chemisorbed surface oxygen ions. This redox reaction releases the trapped donor electrons back into the SnO2 conduction band, dramatically reducing the inter-granular potential barrier and causing the bulk electrical resistance of the sensing layer (Rs) to drop substantially.")
    add_body(doc, "The physical breakout module integrates a precision load resistor (RL, typically 10 kΩ to 47 kΩ) in series with the variable sensor element (Rs), forming a classic voltage divider network. As target gas concentrations rise and Rs falls, the voltage drop across the load resistor (V_RL) increases proportionally according to the voltage divider equation: V_RL = Vcc * [RL / (Rs + RL)]. This analog voltage is exposed on the AO pin and routed directly to the Arduino ADC.")

    add_heading_2(doc, "6.4 Chemiresistive Dynamics, Calibration Imperatives, and Honest Metrology")
    add_body(doc, "While metal-oxide semiconductor (MOS) sensors provide exceptional sensitivity at minimal cost, professional engineering demands a thorough understanding of their physical constraints and metrological realities:")
    add_bullet(doc, "Mandatory Thermal Preheating (Burn-In)", "Metal-oxide sensors require an initial burn-in stabilization period of 24 to 48 hours of continuous heater operation to burn off manufacturing chemical residues. Furthermore, whenever powered on from a cold state, the sensor requires a warm-up stabilization phase of 2 to 5 minutes before electrical resistance reaches dynamic equilibrium.")
    add_bullet(doc, "Atmospheric Cross-Sensitivity", "The MQ-135 lacks chemical selectivity. It responds concurrently to ammonia, carbon dioxide, ethanol, acetone, carbon monoxide, and cigarette smoke. A sudden spike in sensor voltage may indicate alcohol vapors from an antiseptic wipe rather than hazardous air pollution.")
    add_bullet(doc, "Environmental Dependency (Temperature & Humidity Skew)", "The rate of surface gas adsorption is strongly influenced by ambient temperature and relative humidity. High humidity causes water vapor molecules to compete with oxygen for adsorption sites, artificially depressing sensor resistance. True scientific accuracy requires mathematical temperature/humidity compensation curves derived from manufacturer datasheets.")
    add_bullet(doc, "Honest Metrological Labelling", "In student and hobbyist projects, raw MQ-135 ADC values are frequently mislabeled as 'Air Pollution Percentage' or 'Certified Air Quality Index (AQI)'. This practice is scientifically invalid. Formal AQI is a federally standardized metric governed by complex multi-pollutant epidemiological formulas measuring PM2.5, PM10, O3, NO2, SO2, and CO over multi-hour running averages. In this project, the gas response is strictly and honestly classified as an arbitrary 'Classroom Demonstration Response Scale (0-100)'. This transparent terminology maintains absolute scientific and academic integrity.")

    t61_headers = ["Specification / Parameter", "TMP36 Analog Temperature", "DHT11 Digital Temp/Humidity", "MQ-135 Chemiresistive Gas"]
    t61_widths = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.7)]
    t61_rows = [
        ["Primary Transduction Principle", "Silicon bandgap Vbe differential", "NTC thermistor + capacitive polymer", "SnO2 metal-oxide surface adsorption"],
        ["Target Measurement Domain", "Ambient Temperature", "Temperature and Relative Humidity", "NH3, NOx, Alcohol, Benzene, CO2, Smoke"],
        ["Measurement Operational Range", "-40°C to +125°C", "0°C to 50°C / 20% to 90% RH", "10 ppm to 1000 ppm (approximate range)"],
        ["Measurement Accuracy / Tolerance", "±1.0°C at 25°C (±2.0°C full span)", "±2.0°C / ±5.0% Relative Humidity", "Uncalibrated qualitative response (relative)"],
        ["Output Interface Type", "Linear analog voltage (10 mV/°C)", "Single-bus custom digital protocol", "Analog voltage (AO) + Digital threshold (DO)"],
        ["Operating Voltage Rail", "2.7 V to 5.5 V DC", "3.0 V to 5.5 V DC", "5.0 V DC ±0.1 V (Heater requirement)"],
        ["Active Power / Current Draw", "< 50 µA quiescent current", "0.5 mA to 2.5 mA active sampling", "Approximately 150 mA to 180 mA (Heater)"],
        ["Response Time / Stabilization", "Immediate (< 1 second in moving air)", "6 to 10 seconds (thermal mass)", "Warm-up: 2-5 min; Burn-in: 24-48 hrs"]
    ]
    add_styled_table(doc, "Table 6.1: Comprehensive Comparative Sensor Specifications", t61_headers, t61_rows, t61_widths)

    print("Sections 1 to 6 added.")
    return doc

print("Sections 1-6 module ready.")
