import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

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

def add_sections_7_to_12(doc):
    # =========================================================================
    # 7. VIRTUAL PROTOTYPING AND SIMULATION WORKFLOW IN AUTODESK TINKERCAD
    # =========================================================================
    add_heading_1(doc, "7. Virtual Prototyping and Simulation Workflow in Autodesk Tinkercad")
    
    add_heading_2(doc, "7.1 Role and Value of Electronic Design Automation (EDA) Simulation")
    add_body(doc, "Before investing physical resources, cutting wires, or powering delicate silicon components, modern electronic engineering relies heavily upon Electronic Design Automation (EDA) and virtual prototyping platforms. Autodesk Tinkercad Circuits provides an intuitive yet robust browser-based SPICE-assisted circuit simulation environment capable of modeling mixed-signal analog and digital systems.")
    add_body(doc, "In the context of academic instrumentation projects, virtual simulation eliminates the fear of component destruction caused by accidental reverse polarity connections or direct VCC-to-GND dead shorts. Furthermore, Tinkercad enables students to iterate rapidly through firmware algorithmic changes, observe immediate visual feedback on virtual displays, and test conditional threshold branching across synthesized environmental extremes that would be difficult or dangerous to recreate physically on a laboratory bench.")

    add_heading_2(doc, "7.2 Analysis of Virtual Simulation Component Models")
    add_body(doc, "Executing a valid simulation requires a thorough understanding of the behavioral models provided within the Tinkercad component library:")
    add_bullet(doc, "Virtual Microcontroller", "The Tinkercad Arduino Uno R3 model simulates the ATmega328P instruction set and peripherals, supporting code compilation via an embedded AVR-GCC toolchain. It provides full virtual serial monitor capabilities and digital/analog pin routing.")
    add_bullet(doc, "Virtual Temperature Transducer", "The TMP36 model in Tinkercad provides an interactive slider allowing the user to dial simulated ambient temperatures smoothly from -40°C up to +125°C. The virtual output pin produces an exact analog voltage matching the official Analog Devices transfer formula.")
    add_bullet(doc, "Virtual Six-Terminal Gas Sensor Model", "Tinkercad does not feature an integrated, pre-packaged MQ-135 four-pin breakout module. Instead, it provides a raw six-terminal gas sensor component representing the bare internal sensing capsule. This model features two heater pins (H1, H2) and two pairs of sensing electrodes (A1, A2 and B1, B2). To simulate a functional gas sensing circuit, the heater must be tied across 5V and GND, one electrode pair tied to 5V, and the opposing pair connected to an analog input and pulled down to ground via a virtual 10 kΩ load resistor. During simulation, an interactive smoke cloud icon allows the developer to vary gas proximity.")
    add_bullet(doc, "Virtual Alphanumeric LCD", "Tinkercad includes a 16x2 character LCD component with an integrated PCF8574 I2C adapter backpack, responding to standard I2C bus transactions.")

    add_heading_2(doc, "7.3 Step-by-Step Simulation Construction Workflow")
    add_body(doc, "The construction of the virtual monitoring instrument within Tinkercad Circuits followed a systematic, four-phase procedural workflow:")
    add_bullet(doc, "Phase 1: Component Instantiation & Placement", "A blank circuit workspace was initialized, and an Arduino Uno R3, half-size breadboard, TMP36 temperature sensor, six-terminal gas sensor element, 10 kΩ resistor, and 16x2 I2C LCD were placed into the workspace.")
    add_bullet(doc, "Phase 2: Power and Ground Bus Distribution", "5.0 V power and Ground leads were routed from the Arduino headers to the primary top and bottom breadboard distribution rails. Decoupling jumper lines were established across rails.")
    add_bullet(doc, "Phase 3: Sensor and Peripheral Wiring", "The TMP36 power pins were wired to 5V and GND, with the center analog wiper routed directly to Arduino analog pin A1. The six-terminal gas sensor was configured with H1 and A1 connected to the 5V rail, H2 connected to GND, and B1 routed to Arduino analog pin A0 while simultaneously connecting to GND through the 10 kΩ load resistor. The I2C LCD power leads were tied to the 5V rails, and its SDA and SCL terminals were routed to Arduino pins A4 and A5 respectively.")
    add_bullet(doc, "Phase 4: Code Implementation & Verification", "C++ code utilizing the Adafruit_LiquidCrystal library was entered into the text editor. The simulation was started, and slider controls were systematically exercised to verify ADC response, serial streaming, and LCD screen switching.")

    add_heading_2(doc, "7.4 Metrological Scope: What Virtual Simulation Proves and What It Omits")
    add_body(doc, "A rigorous engineering report must clearly distinguish between simulated validation and physical proof. Virtual simulation successfully proves: C++ code syntax correctness, arithmetic conversion logic, conditional threshold branching, non-blocking temporal flow, I2C bus communication mechanics, and serial output formatting.")
    add_body(doc, "Conversely, virtual simulation fundamentally omits: physical component manufacturing tolerances, breadboard contact degradation, power supply ripple, wire capacitance, ambient thermal dissipation, the 24-hour MQ-135 chemical burn-in requirement, gas cross-sensitivity, and the real-world digital single-bus handshaking protocol required by physical DHT11 sensors. These real-world phenomena can only be validated through physical benchtop hardware testing.")

    add_callout(doc, "Simulation Verification Rule", "Always treat simulation as proof of software logic and basic circuit topology, never as final validation of sensor calibration or physical reliability.")

    # =========================================================================
    # 8. COMPREHENSIVE CIRCUIT SCHEMATIC AND WIRING ARCHITECTURE
    # =========================================================================
    add_heading_1(doc, "8. Comprehensive Circuit Schematic and Wiring Architecture")
    
    add_heading_2(doc, "8.1 Simulation Interconnection Architecture")
    add_body(doc, "The virtual circuit implementation inside Autodesk Tinkercad Circuits reflects a foundational mixed-signal instrumentation design. Because simulation platforms utilize idealized component primitives, specific wiring topologies must be carefully structured to ensure accurate electrical propagation.")
    add_body(doc, "In the Tinkercad environment, the primary analog temperature channel is monitored via the TMP36 sensor connected to analog channel A1. The gas sensing circuit utilizes the raw six-terminal gas capsule model. Terminal H1 (heater power) and Terminal A1 (sensing electrode power) are tied together to the 5.0 V positive bus. Terminal H2 (heater return) is connected directly to circuit Ground. Terminal B1 (sensing output) connects to the measurement node, which is wired simultaneously to Arduino analog input A0 and to one terminal of a 10 kΩ 0.25 W carbon film load resistor. The remaining terminal of the load resistor connects to Ground, forming the complete voltage divider network.")
    add_body(doc, "The alphanumeric I2C LCD backpack is wired directly across the system power bus (VCC and GND), with its serial data line (SDA) connected to analog pin A4 and its serial clock line (SCL) connected to analog pin A5. This complete interconnection scheme utilizes only two analog input pins for sensing and two dual-function analog pins for I2C communication, leaving digital pins D0 through D13 entirely unencumbered.")

    add_heading_2(doc, "8.2 Physical Hardware Interconnection Architecture")
    add_body(doc, "Transitioning the project from virtual simulation to a tangible physical breadboard assembly introduces significant, practical improvements in sensor capability and circuit topology. In the physical build, the analog TMP36 is replaced by the digital DHT11 composite sensor module, enabling simultaneous observation of both ambient temperature and atmospheric relative humidity.")
    add_body(doc, "The DHT11 module requires three active electrical connections: VCC (connected to Arduino 5.0 V), GND (connected to common Ground), and DATA. The DATA pin is routed to Arduino digital pin D2. If utilizing a bare 4-pin DHT11 sensor rather than a pre-mounted 3-pin breakout board, a 4.7 kΩ to 10 kΩ pull-up resistor must be inserted between the DATA line and the 5.0 V rail to maintain high bus idle levels.")
    add_body(doc, "The gas detection channel in the physical implementation utilizes a commercial 4-pin MQ-135 breakout board. Unlike the raw six-terminal simulation model, the commercial MQ-135 module integrates an onboard LM393 comparator, internal load resistor, and power filtering circuitry. The module exposes four pins: VCC, GND, AO (Analog Output), and DO (Digital Threshold Output). The module's VCC is connected to the 5.0 V rail, GND is tied to common Ground, and AO is routed to Arduino analog input A0. The digital output pin (DO) is left unconnected in this build, as continuous multi-level analog tracking is handled entirely within firmware.")
    add_body(doc, "The physical I2C LCD display connects identically to the simulation topology: VCC to 5.0 V, GND to common Ground, SDA to Arduino pin A4, and SCL to Arduino pin A5.")

    add_heading_2(doc, "8.3 Grounding Integrity, Power Bus Decoupling, and Assembly Rules")
    add_body(doc, "Maintaining absolute signal integrity across mixed-signal microcontroller circuits requires disciplined adherence to grounding and decoupling principles. In an instrumentation circuit combining high-current resistive heating coils (MQ-135 heater drawing ~160 mA) with sensitive micro-volt analog sensing and high-speed digital switching lines, ground loops and supply rail noise represent severe hazards.")
    add_body(doc, "To prevent erratic readings and ADC quantization jitter, all subsystems—the Arduino Uno, DHT11 sensor, MQ-135 module, and I2C LCD—must share a single, unbroken Common Ground reference. Establishing a common ground ensures that all voltage measurements possess an identical 0.0 V zero-potential reference point across the entire breadboard.")
    add_body(doc, "Furthermore, during initial physical assembly, a 100 µF electrolytic decoupling capacitor should be placed across the main breadboard 5V and GND power rails to absorb transient current surges caused by the MQ-135 heater, supplemented by a 0.1 µF ceramic capacitor placed adjacent to the sensor power pins to filter high-frequency digital switching noise.")

    t81_headers = ["Component Pin / Terminal", "Module / Subsystem", "Arduino Connection", "Signal Type & Operational Function"]
    t81_widths = [Inches(1.6), Inches(1.5), Inches(1.6), Inches(1.8)]
    t81_rows = [
        ["VCC / Pin 1 (+Vs)", "TMP36 (Simulation)", "5.0 V Breadboard Rail", "Power supply input (2.7 V to 5.5 V DC)."],
        ["Vout / Pin 2 (Center)", "TMP36 (Simulation)", "Analog Pin A1", "Linear analog thermal voltage (10 mV/°C)."],
        ["GND / Pin 3 (Right)", "TMP36 (Simulation)", "Common Ground Rail", "Zero-volt reference return."],
        ["VCC / Pin 1 (+)", "DHT11 (Physical)", "5.0 V Breadboard Rail", "Positive power supply input (3.0 V to 5.5 V DC)."],
        ["DATA / Pin 2 (Out)", "DHT11 (Physical)", "Digital Pin D2", "Single-bus bidirectional PWM serial pulse stream."],
        ["GND / Pin 3 (-)", "DHT11 (Physical)", "Common Ground Rail", "Zero-volt reference return."],
        ["VCC / Pin 1 (Power)", "MQ-135 Module", "5.0 V Breadboard Rail", "Heater and internal comparator supply (5.0 V DC)."],
        ["GND / Pin 2 (Ground)", "MQ-135 Module", "Common Ground Rail", "Zero-volt reference return for heater and signal."],
        ["AO / Pin 3 (Analog)", "MQ-135 Module", "Analog Pin A0", "Variable analog voltage from internal divider."],
        ["DO / Pin 4 (Digital)", "MQ-135 Module", "Not Connected (NC)", "Onboard LM393 comparator threshold output."],
        ["VCC / Pin 1", "I2C LCD Backpack", "5.0 V Breadboard Rail", "Logic and backlight power (5.0 V DC)."],
        ["GND / Pin 2", "I2C LCD Backpack", "Common Ground Rail", "Zero-volt reference return."],
        ["SDA / Pin 3", "I2C LCD Backpack", "Analog Pin A4 (SDA)", "Two-wire serial data bidirectional bus line."],
        ["SCL / Pin 4", "I2C LCD Backpack", "Analog Pin A5 (SCL)", "Two-wire serial clock synchronization bus line."]
    ]
    add_styled_table(doc, "Table 8.1: Complete End-to-End Pin Interconnection Matrix", t81_headers, t81_rows, t81_widths)

    # =========================================================================
    # 9. FIRMWARE ARCHITECTURE, ALGORITHMIC DESIGN, AND FLOW CONTROL
    # =========================================================================
    add_heading_1(doc, "9. Firmware Architecture, Algorithmic Design, and Flow Control")
    
    add_heading_2(doc, "9.1 Structural Execution Philosophy and Timing Architecture")
    add_body(doc, "Embedded firmware architecture fundamentally dictates the reliability, responsiveness, and long-term stability of an instrumentation device. In traditional beginner-level Arduino code, developers rely heavily upon the blocking delay() function to pace program execution and control LCD refresh rates. However, invoking delay(3000) completely halts the ATmega328P processor core for three seconds, suspending serial communications, preventing real-time error handling, and making responsive multi-tasking impossible.")
    add_body(doc, "To overcome these critical limitations, the firmware for this environmental monitoring system is structured around a non-blocking cooperative state scheduler utilizing the microcontroller's hardware Timer0 millisecond counter (millis()). The main loop executes continuously at full clock speed, querying whether the elapsed time since the prior operational cycle has surpassed a preconfigured threshold (const unsigned long updateInterval = 3000 ms). This ensures that background tasks, serial buffer monitoring, and error watchdogs operate with zero latency while sensor sampling and screen refreshes occur deterministically.")

    add_heading_2(doc, "9.2 Mathematical Quantization, Normalization, and Mapping Algorithms")
    add_body(doc, "Raw digital data acquired from embedded transducers requires multi-stage mathematical transformation before it can be presented meaningfully to human operators:")
    add_bullet(doc, "Stage 1: Analog Quantization to True Voltage", "When analog channels are sampled via analogRead(), the 10-bit ADC yields an integer count ranging from 0 to 1023. The firmware normalizes this count into true floating-point voltage using the formula: float voltage = (float)adcCount * (5.0 / 1023.0).")
    add_bullet(doc, "Stage 2: Thermal Linearization (TMP36)", "For analog temperature conversion, the 0.50 V offset is subtracted and the result multiplied by 100: float temperature = (voltage - 0.50) * 100.0.")
    add_bullet(doc, "Stage 3: Chemical Sensor Mapping", "The raw gas ADC value (0-1023) is translated onto a normalized demonstration response scale (0-100) using the integer scaling function: int responseScale = map(gasRaw, 0, 1023, 0, 100); followed by mathematical bounding: responseScale = constrain(responseScale, 0, 100); to guarantee array index safety and prevent overflow bugs.")

    add_heading_2(doc, "9.3 Multi-Tier Qualitative Threshold Categorization Logic")
    add_body(doc, "Because raw metal-oxide sensor outputs reflect broad-spectrum relative resistance changes rather than calibrated chemical concentrations, presenting unvarnished numbers to non-technical users creates confusion. The firmware implements a 4-tier qualitative categorization algorithm that translates numerical response metrics into clear, human-understandable environmental states:")
    add_bullet(doc, "Tier 1 (Response Scale 0 to 29)", "Categorized as 'GOOD'. Represents normal, clean ambient baseline conditions with minimal detected reducing gases or volatile airborne contaminants.")
    add_bullet(doc, "Tier 2 (Response Scale 30 to 59)", "Categorized as 'MODERATE'. Reflects slight atmospheric variations, elevated human occupancy, minor stagnation in room air, or trace volatile compounds.")
    add_bullet(doc, "Tier 3 (Response Scale 60 to 79)", "Categorized as 'POOR'. Indicates noticeable accumulation of organic vapors, cooking fumes, stagnant respiratory CO2, or soldering smoke requiring active ventilation.")
    add_bullet(doc, "Tier 4 (Response Scale 80 to 100)", "Categorized as 'DANGER'. Signifies heavy localized chemical fumes, combustible gas leakage, or intense smoke saturation demanding immediate room evacuation.")
    add_body(doc, "These boundaries represent pedagogical demonstration thresholds designed to demonstrate conditional state-machine logic in classroom laboratories, explicitly distinguishing them from federally mandated regulatory air quality standards.")

    add_heading_2(doc, "9.4 Robust Error Trapping, Sensor Validation, and Fault Recovery")
    add_body(doc, "A hallmark of professional-grade firmware is graceful error handling. When interfacing digital transducers such as the DHT11, communication timeouts, loose breadboard jumpers, or electrical noise can corrupt the 40-bit data stream, causing library functions to return IEEE NaN (Not-a-Number) floating-point flags.")
    add_body(doc, "Rather than crashing or printing unreadable garbage characters to the LCD, the firmware actively traps these conditions using the isnan(temperature) || isnan(humidity) macro. If a communication fault is detected, the firmware suppresses downstream arithmetic, outputs an explicit diagnostic warning ('DHT11 read error') to the display, logs the fault over the UART serial stream, and executes an immediate loop return, waiting for the subsequent sampling interval to attempt self-recovery.")

    t91_headers = ["Demonstration Scale (0-100)", "Raw ADC Range (0-1023)", "Assigned Status Label", "Environmental Interpretation & Pedagogical Action"]
    t91_widths = [Inches(1.5), Inches(1.5), Inches(1.5), Inches(2.0)]
    t91_rows = [
        ["0 to 29", "0 to 306 ADC counts", "GOOD", "Clean ambient baseline; normal room air ventilation."],
        ["30 to 59", "307 to 613 ADC counts", "MODERATE", "Slight presence of VOCs or stagnant air; observe trends."],
        ["60 to 79", "614 to 818 ADC counts", "POOR", "Elevated vapor or smoke detected; active ventilation advised."],
        ["80 to 100", "819 to 1023 ADC counts", "DANGER", "Severe gas concentration; alert occupants and ventilate space."]
    ]
    add_styled_table(doc, "Table 9.1: Multi-Tier Qualitative Gas Response Classification Matrix", t91_headers, t91_rows, t91_widths)

    # =========================================================================
    # 10. COMPLETE VIRTUAL FIRMWARE IMPLEMENTATION (TINKERCAD ENVIRONMENT)
    # =========================================================================
    add_heading_1(doc, "10. Complete Virtual Firmware Implementation (Tinkercad Environment)")
    
    add_heading_2(doc, "10.1 Tinkercad Software Environment and Adafruit LiquidCrystal Library")
    add_body(doc, "The Autodesk Tinkercad Circuits platform utilizes an embedded AVR-GCC compiler and provides a pre-installed, specialized LCD library: Adafruit_LiquidCrystal.h. Unlike physical PCF8574 libraries that initialize via an explicit 7-bit hexadecimal I2C slave address (such as 0x27 or 0x3F), the Tinkercad Adafruit library utilizes an integer constructor argument (typically lcd(0)) to designate the virtual I2C expander instance.")
    add_body(doc, "Understanding this library abstraction is essential for students and engineers working across simulation and physical hardware. The code presented below represents the complete, verified, and syntax-checked source code for the Tinkercad simulation, featuring comprehensive comments, robust variable definitions, and clean modular structure.")

    add_heading_2(doc, "10.2 Complete Commented Simulation C++ Source Code")
    add_body(doc, "The complete simulation source code is structured as follows:")

    sim_code = """/*
 * ============================================================================
 * Project: Arduino-Based Environmental Monitoring System (Virtual Simulation)
 * Platform: Autodesk Tinkercad Circuits (Arduino Uno R3)
 * Sensors: TMP36 (Analog Temperature on A1), 6-Terminal Gas Sensor (A0)
 * Display: 16x2 Character LCD with I2C Backpack (Adafruit_LiquidCrystal)
 * Description: Samples temperature and gas response, performs mathematical
 *              conversions, categorizes gas status, and alternates display.
 * ============================================================================
 */

#include <Adafruit_LiquidCrystal.h>

// Pin Definitions
#define GAS_PIN   A0    // Analog input pin for gas sensing element
#define TEMP_PIN  A1    // Analog input pin for TMP36 temperature sensor

// Initialize I2C LCD using Tinkercad Adafruit library (instance address 0)
Adafruit_LiquidCrystal lcd(0);

void setup() {
  // Initialize hardware serial communication for diagnostic monitoring
  Serial.begin(9600);
  
  // Initialize alphanumeric LCD: 16 columns by 2 rows
  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.clear();
  
  // Render introductory welcome banner
  lcd.setCursor(0, 0);
  lcd.print("Environmental");
  lcd.setCursor(0, 1);
  lcd.print("Monitoring");
  delay(2000);
  lcd.clear();
  
  Serial.println("==================================================");
  Serial.println("   Tinkercad Environmental Monitor Initialized   ");
  Serial.println("==================================================");
}

void loop() {
  // --------------------------------------------------------------------------
  // 1. Temperature Sensor Acquisition & Conversion (TMP36)
  // --------------------------------------------------------------------------
  int tempReading = analogRead(TEMP_PIN);
  float voltage = tempReading * (5.0 / 1023.0);
  // Transfer Function: (Vout - 0.500 V) * 100 deg C/V
  float temperature = (voltage - 0.500) * 100.0;
  
  // --------------------------------------------------------------------------
  // 2. Gas Sensor Acquisition & Qualitative Mapping
  // --------------------------------------------------------------------------
  int gasValue = analogRead(GAS_PIN);
  int responseScale = map(gasValue, 0, 1023, 0, 100);
  responseScale = constrain(responseScale, 0, 100);
  
  // Qualitative Multi-Tier Status Classification
  String airQuality;
  if (responseScale < 30) {
    airQuality = "GOOD";
  } else if (responseScale < 60) {
    airQuality = "MODERATE";
  } else if (responseScale < 80) {
    airQuality = "POOR";
  } else {
    airQuality = "DANGER";
  }
  
  // --------------------------------------------------------------------------
  // 3. Serial Diagnostic Telemetry Dispatch
  // --------------------------------------------------------------------------
  Serial.println("----------------------------------------");
  Serial.print("Temperature (°C)   : "); Serial.println(temperature, 2);
  Serial.print("TMP36 Voltage (V)  : "); Serial.println(voltage, 3);
  Serial.print("Gas Raw ADC Value  : "); Serial.println(gasValue);
  Serial.print("Demonstration Scale: "); Serial.print(responseScale); Serial.println("/100");
  Serial.print("Classroom Status   : "); Serial.println(airQuality);
  
  // --------------------------------------------------------------------------
  // 4. Sequential Screen Presentation on 16x2 LCD
  // --------------------------------------------------------------------------
  // Screen 1: Temperature Observation
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temperature:");
  lcd.setCursor(0, 1);
  lcd.print(temperature, 1);
  lcd.print(" C");
  delay(3000);
  
  // Screen 2: Qualitative Air Quality Status
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Air Quality:");
  lcd.setCursor(0, 1);
  lcd.print(airQuality);
  delay(3000);
  
  // Screen 3: Scaled Gas Response Metric
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Gas Response:");
  lcd.setCursor(0, 1);
  lcd.print(responseScale);
  lcd.print("/100");
  delay(3000);
}"""
    add_code_block(doc, sim_code)

    add_heading_2(doc, "10.3 In-Depth Line-by-Line Code Review and Operational Analysis")
    add_body(doc, "A rigorous technical examination of the simulation code reveals multiple deliberate architectural considerations:")
    add_bullet(doc, "Explicit Macro Constants", "#define GAS_PIN A0 and #define TEMP_PIN A1 improve firmware maintainability and eliminate magic numbers, allowing rapid pin remapping without modifying internal operational logic.")
    add_bullet(doc, "Floating-Point Normalization", "Casting the ADC integer to floating-point via (5.0 / 1023.0) guarantees that the compiler generates high-precision floating-point arithmetic instructions rather than truncating division to integer zero.")
    add_bullet(doc, "Boundary Safety with constrain()", "Applying constrain(responseScale, 0, 100) protects against unexpected math anomalies or ADC overflow, ensuring values strictly obey display buffer limits.")
    add_bullet(doc, "Modular LCD Screen Cycling", "Splitting information across three successive screens prevents display line overcrowding and ensures all parameters remain readable at standard classroom distances.")

    add_callout(doc, "Code Portability Caution", "Notice that the Tinkercad code uses Adafruit_LiquidCrystal lcd(0). This library is specific to Tinkercad's virtual environment. In physical hardware, the PCF8574 backpack requires LiquidCrystal_I2C lcd(0x27, 16, 2) or lcd(0x3F, 16, 2).")

    # =========================================================================
    # 11. PHYSICAL HARDWARE IMPLEMENTATION AND ASSEMBLY ROADMAP
    # =========================================================================
    add_heading_1(doc, "11. Physical Hardware Implementation and Assembly Roadmap")
    
    add_heading_2(doc, "11.1 Bill of Materials and Procurement Specifications")
    add_body(doc, "Transitioning the project to tangible hardware requires sourcing commercial-grade components meeting exact electrical and mechanical specifications. The complete physical bill of materials encompasses:")
    add_bullet(doc, "Arduino Uno R3 Development Board", "ATmega328P DIP edition preferred for socketed serviceability, accompanied by a 1.0 m shielded USB A-to-B cable.")
    add_bullet(doc, "DHT11 Composite Sensor Breakout Module", "3-pin edition featuring onboard 4.7 kΩ pull-up resistor and decoupling capacitor.")
    add_bullet(doc, "MQ-135 Air Quality Gas Sensor Breakout Board", "4-pin edition featuring integrated LM393 comparator and trimmer potentiometer.")
    add_bullet(doc, "16x2 Character Alphanumeric LCD", "Pre-soldered PCF8574 I2C adapter backpack.")
    add_bullet(doc, "Prototyping Platform", "830-point solderless breadboard and a 40-piece ribbon pack of 20 cm male-to-male and male-to-female DuPont jumper cables.")

    add_heading_2(doc, "11.2 Step-by-Step Benchtop Assembly Workflow")
    add_body(doc, "To guarantee circuit integrity and prevent electrostatic discharge (ESD) or wiring damage, physical benchtop assembly must follow a strict, eight-step procedural sequence:")
    add_bullet(doc, "Step 1: Power Disconnection & Anti-Static Precautions", "Ensure the Arduino Uno is completely disconnected from computer USB ports or external DC power adapters before inserting any wires into the breadboard.")
    add_bullet(doc, "Step 2: Main Power and Ground Bus Distribution", "Connect the Arduino Uno 5V header pin to the top red (+) breadboard bus rail using a red jumper. Connect the Arduino GND pin to the top blue (-) bus rail using a black jumper. Bridge the top and bottom power rails using color-coded jumpers.")
    add_bullet(doc, "Step 3: I2C Display Interconnection", "Mount the 16x2 LCD display securely. Route VCC and GND from the I2C backpack to the breadboard power rails. Connect the backpack SDA terminal to Arduino analog pin A4 and SCL to analog pin A5.")
    add_bullet(doc, "Step 4: Initial Display & Bus Validation", "Plug the USB cable into the Arduino and upload a minimal I2C scanner sketch to verify that the backpack responds at expected address 0x27 or 0x3F. Adjust the blue contrast potentiometer on the backpack until solid test characters are visible.")
    add_bullet(doc, "Step 5: DHT11 Sensor Wiring", "Disconnect USB power. Insert the DHT11 module. Connect VCC to 5V, GND to Ground, and route the DATA pin to Arduino digital pin D2.")
    add_bullet(doc, "Step 6: MQ-135 Gas Sensor Wiring", "Connect the MQ-135 module VCC to the 5V power rail, GND to Ground, and connect the AO (analog output) pin to Arduino analog input A0. Leave the DO pin unconnected.")
    add_bullet(doc, "Step 7: Pre-Flight Visual Inspection", "Review all connections against the master wiring diagram, checking specifically for reversed VCC/GND leads, shorted jumper pins, or loose breadboard grips.")
    add_bullet(doc, "Step 8: Power-Up and Initial Sensor Burn-In", "Reconnect USB power. Observe the power LED indicators on the Arduino, MQ-135, and LCD backpack. Allow the MQ-135 sensor heater to warm up for at least 5 minutes before logging data.")

    add_heading_2(doc, "11.3 Electrical Power Distribution, Heater Current Dissipation, and Thermal Management")
    add_body(doc, "A critical physical consideration in multi-sensor embedded design is total electrical current consumption. While standard digital sensors like the DHT11 consume less than 2.5 mA during active measurements, the MQ-135 utilizes an internal resistive heating element (31 Ω ±3 Ω) that consumes approximately 150 mA to 180 mA of continuous current at 5.0 V DC.")
    add_body(doc, "When combined with the Arduino microcontroller core (~50 mA) and the 16x2 LCD LED backlight (~30 mA), the complete physical instrument draws approximately 240 mA to 270 mA. While well within the 500 mA current limit of standard USB 2.0 computer ports, powering the circuit from unpowered USB hubs or undersized 9V alkaline batteries through the onboard 5V regulator can cause regulator thermal overload and voltage brownouts. A dedicated 5V 1A regulated USB power source or USB 3.0 port is strongly recommended for continuous benchtop operation.")

    t111_headers = ["Component Name", "Manufacturer / Package", "Quantity", "Supply Voltage", "Nominal Current Draw", "Interface Protocol"]
    t111_widths = [Inches(1.3), Inches(1.3), Inches(0.6), Inches(1.1), Inches(1.1), Inches(1.1)]
    t111_rows = [
        ["Arduino Uno R3", "Microchip ATmega328P DIP", "1", "5.0 V DC (USB/7-12V)", "45 mA - 55 mA", "UART / SPI / I2C / GPIO"],
        ["DHT11 Sensor Module", "Aosong 3-pin Breakout", "1", "3.3 V - 5.0 V DC", "0.5 mA - 2.5 mA", "Custom Single-Bus Digital"],
        ["MQ-135 Gas Sensor", "Winsen 4-pin Breakout", "1", "5.0 V DC ±0.1 V", "150 mA - 180 mA", "Linear Analog Voltage (AO)"],
        ["16x2 LCD + PCF8574", "Hitachi HD44780 + I2C", "1", "5.0 V DC", "25 mA - 35 mA (Backlight)", "Two-Wire Serial I2C Bus"],
        ["Solderless Breadboard", "830-point ABS Plastic", "1", "N/A (Passive)", "0 mA", "Direct Mechanical Spring"],
        ["DuPont Jumper Wires", "Multi-strand Copper 24AWG", "1 set (20 pcs)", "N/A (Passive)", "0 mA", "2.54 mm Pitch Headers"]
    ]
    add_styled_table(doc, "Table 11.1: Physical Prototype Bill of Materials (BOM) & Electrical Parameters", t111_headers, t111_rows, t111_widths)

    # =========================================================================
    # 12. PRODUCTION PHYSICAL FIRMWARE AND SOFTWARE TOOLCHAIN SETUP
    # =========================================================================
    add_heading_1(doc, "12. Production Physical Firmware and Software Toolchain Setup")
    
    add_heading_2(doc, "12.1 Software Development Environment and Toolchain Configuration")
    add_body(doc, "Developing production-ready firmware for the physical Arduino platform requires configuring the official Arduino Integrated Development Environment (IDE v2.x or modern command-line Arduino CLI). The development environment provides an integrated code editor, an automated AVR-GCC cross-compiler toolchain, and an in-system programmer (avrdude) that flashes compiled binary hex files to the ATmega328P via the Optiboot bootloader.")
    add_body(doc, "To interface the physical sensor hardware, two third-party open-source libraries must be installed via the Arduino IDE Library Manager:")
    add_bullet(doc, "1. Adafruit DHT Sensor Library", "Provides high-level object-oriented classes to decode the proprietary 40-bit single-bus digital pulse stream from the DHT11 sensor, incorporating integrated CRC parity checking and microsecond pulse-width timing. Requires the foundational Adafruit Unified Sensor library as an underlying dependency.")
    add_bullet(doc, "2. LiquidCrystal_I2C Library", "Facilitates high-speed I2C communication with PCF8574-based display backpacks, replacing low-level Wire.h byte transactions with intuitive print(), setCursor(), and clear() commands.")
    add_body(doc, "Before uploading the production sketch, an I2C scanner sketch should always be executed to verify the exact 7-bit bus address of the physical LCD backpack. While 0x27 is the standard address for PCF8574T chips, backpacks utilizing the PCF8574AT silicon variant operate at address 0x3F. Mismatching this address is the single most common cause of blank LCD screens in student laboratories.")

    add_heading_2(doc, "12.2 Production Physical C++ Source Code Implementation")
    add_body(doc, "The complete, production-grade Arduino C++ source code for the physical monitoring station is provided below. It features non-blocking timestamp scheduling, explicit hardware pin macros, robust error trapping, serial diagnostic telemetry, and clean two-line LCD formatting:")

    phys_code = """/*
 * ============================================================================
 * Project: Arduino-Based Environmental Monitoring System (Physical Build)
 * Platform: Physical Arduino Uno R3 (ATmega328P @ 16 MHz)
 * Sensors: DHT11 (Digital Temp/Humidity on D2), MQ-135 Gas Sensor (AO on A0)
 * Display: 16x2 Character LCD via PCF8574 I2C Backpack (Address 0x27 / 0x3F)
 * Architecture: Non-blocking cooperative state scheduling via millis()
 * Description: Reads digital temperature/humidity and analog gas response,
 *              performs error trapping, executes qualitative threshold
 *              categorization, streams serial telemetry, and updates LCD.
 * ============================================================================
 */

#include <Wire.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>

// Hardware Pin Assignments
#define DHTPIN       2       // Digital input pin connected to DHT11 DATA line
#define DHTTYPE      DHT11   // Transducer type identifier (DHT11 or DHT22)
#define MQ135_PIN    A0      // Analog input pin connected to MQ-135 AO terminal

// Instantiation of Peripheral Objects
DHT dht(DHTPIN, DHTTYPE);

// Configure I2C LCD: Common address is 0x27; modify to 0x3F if backpack uses PCF8574AT
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Non-Blocking Timing Scheduler Variables
unsigned long lastUpdate = 0;
const unsigned long updateInterval = 3000; // Deterministic refresh interval: 3.0 seconds

void setup() {
  // Initialize Universal Asynchronous Receiver-Transmitter (UART) serial bus
  Serial.begin(9600);
  
  // Initialize DHT11 digital environmental transducer
  dht.begin();
  
  // Initialize I2C alphanumeric LCD display
  lcd.init();
  lcd.backlight();
  lcd.clear();
  
  // Present introductory system splash screen
  lcd.setCursor(0, 0);
  lcd.print("Environmental");
  lcd.setCursor(0, 1);
  lcd.print("Monitoring Sys");
  delay(2000); // Brief initial banner hold
  lcd.clear();
  
  Serial.println("==================================================");
  Serial.println(" Physical Environmental Monitoring Station Ready  ");
  Serial.println(" System Core: ATmega328P @ 16 MHz | Logic: 5.0 V  ");
  Serial.println(" Sensors: DHT11 (Pin D2) | MQ-135 (Pin A0)        ");
  Serial.println(" Telemetry Interval: 3000 ms                      ");
  Serial.println("==================================================");
}

void loop() {
  // --------------------------------------------------------------------------
  // 1. Non-Blocking Execution Guard
  // --------------------------------------------------------------------------
  if (millis() - lastUpdate < updateInterval) {
    return; // Yield control immediately; preserve CPU responsiveness
  }
  lastUpdate = millis(); // Refresh operational execution timestamp
  
  // --------------------------------------------------------------------------
  // 2. Multi-Channel Environmental Transducer Acquisition
  // --------------------------------------------------------------------------
  float temperature = dht.readTemperature(); // Ambient temperature in degrees Celsius
  float humidity    = dht.readHumidity();    // Relative atmospheric humidity in %
  int gasRaw        = analogRead(MQ135_PIN); // 10-bit integer ADC quantization (0-1023)
  
  // --------------------------------------------------------------------------
  // 3. Robust Error Trapping & Communication Validation
  // --------------------------------------------------------------------------
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("[ERROR] Failed to read from DHT11 sensor! Check cabling/pull-up.");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("DHT11 Sensor Err");
    lcd.setCursor(0, 1);
    lcd.print("Check Cabling...");
    return; // Abort cycle gracefully; retry at subsequent scheduling window
  }
  
  // --------------------------------------------------------------------------
  // 4. Mathematical Mapping & Qualitative Status Classification
  // --------------------------------------------------------------------------
  // Linear demonstration scale mapping (0 to 100)
  int responseScale = map(gasRaw, 0, 1023, 0, 100);
  responseScale = constrain(responseScale, 0, 100);
  
  // Multi-tier qualitative threshold categorization
  const char* status;
  if (responseScale < 30) {
    status = "GOOD";
  } else if (responseScale < 60) {
    status = "MODERATE";
  } else if (responseScale < 80) {
    status = "POOR";
  } else {
    status = "DANGER";
  }
  
  // --------------------------------------------------------------------------
  // 5. Serial Diagnostic Telemetry Dispatch (9600 Baud)
  // --------------------------------------------------------------------------
  Serial.println("----------------------------------------");
  Serial.print("Timestamp (ms)    : "); Serial.println(millis());
  Serial.print("Temperature (°C)  : "); Serial.println(temperature, 1);
  Serial.print("Humidity (%)      : "); Serial.println(humidity, 1);
  Serial.print("MQ-135 Raw ADC    : "); Serial.println(gasRaw);
  Serial.print("Demonstration /100: "); Serial.println(responseScale);
  Serial.print("Qualitative Status: "); Serial.println(status);
  
  // --------------------------------------------------------------------------
  // 6. Alphanumeric LCD Telemetry Rendering (16x2 Matrix)
  // --------------------------------------------------------------------------
  lcd.clear();
  // Row 0: Dual thermal parameters
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temperature, 1);
  lcd.print("C H:");
  lcd.print(humidity, 0);
  lcd.print("%");
  
  // Row 1: Air response status and numerical scale
  lcd.setCursor(0, 1);
  lcd.print("Air:");
  lcd.print(status);
  lcd.print(" (");
  lcd.print(responseScale);
  lcd.print(")");
}"""
    add_code_block(doc, phys_code)

    add_heading_2(doc, "12.3 Line-by-Line Technical Code Analysis and Architectural Benefits")
    add_body(doc, "An in-depth technical analysis highlights several key firmware innovations:")
    add_bullet(doc, "Millisecond Scheduling vs. CPU Blocking", "The if (millis() - lastUpdate < updateInterval) pattern decouples sensor sampling from microcontroller clock cycles. The processor executes millions of background checks without entering power-draining or communication-halting delay loops.")
    add_bullet(doc, "Simultaneous Dual-Line Visualization", "Unlike the simulation firmware which required three consecutive screens due to TMP36 single-variable display, the physical firmware compacts four critical environmental metrics onto a single screen: Temperature (T:24.5C), Relative Humidity (H:58%), Air Status (Air:GOOD), and Scaled Value ((18)). This delivers an exceptionally clean, readable, and human-friendly interface.")
    add_bullet(doc, "Fault Trapping Resilience", "The isnan() guard prevents mathematical calculation errors from propagating to the display, preserving visual professionalism even during momentary sensor disconnection.")

    add_callout(doc, "Deployment Best Practice", "When deploying the physical monitor in a permanent installation, verify the I2C backpack contrast potentiometer with a small precision screwdriver until character pixels are crisp against the blue or green backlight.")

    print("Sections 7 to 12 added.")
    return doc

print("Sections 7-12 module ready.")
