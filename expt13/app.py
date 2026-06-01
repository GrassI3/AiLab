from flask import Flask, render_template, request, jsonify, session
import json
app = Flask(__name__)
app.secret_key = "laptop_diag_secret_2026"
QUESTIONS = [
    {
        "id": "q_main_symptom",
        "text": "What's the main problem you're experiencing?",
        "options": [
            {"value": "wont_start",    "label": "Laptop won't turn on at all"},
            {"value": "slow",          "label": "Laptop is very slow / freezing"},
            {"value": "battery",       "label": "Battery / charging issues"},
            {"value": "display",       "label": "Screen / display issues"},
            {"value": "overheating",   "label": "Laptop overheating / shutting down"},
            {"value": "noise",         "label": "Strange noises (clicking, grinding, beeping)"},
            {"value": "wifi",          "label": "WiFi / network not working"},
            {"value": "keyboard",      "label": "Keyboard / touchpad issues"},
            {"value": "storage",       "label": "Storage / disk errors or slowness"},
            {"value": "bluescreen",    "label": "Blue screen / crash errors (BSOD)"},
        ],
        "always_ask": True,
        "relevance": {} 
    },
    {
        "id": "q_power_led",
        "text": "When you press the power button, do any lights (LED indicators) turn on?",
        "options": [
            {"value": "yes_all",   "label": "Yes – power LED + other lights come on"},
            {"value": "yes_brief", "label": "Briefly flickers then goes dark"},
            {"value": "no",        "label": "No lights at all"},
        ],
        "relevant_to": ["wont_start"],
        "relevance": {"dead_battery": 0.6, "bad_motherboard": 0.4, "power_adapter_fault": 0.5}
    },
    {
        "id": "q_charger_check",
        "text": "Have you tried a different charger or verified your power adapter works?",
        "options": [
            {"value": "yes_works",   "label": "Yes – different charger, still same problem"},
            {"value": "yes_fixed",   "label": "Yes – it works with a different charger"},
            {"value": "no",          "label": "No, haven't tried"},
        ],
        "relevant_to": ["wont_start", "battery"],
        "relevance": {"power_adapter_fault": 0.9, "dead_battery": 0.3}
    },
    {
        "id": "q_beep_codes",
        "text": "Does the laptop emit any beep sounds when you power it on?",
        "options": [
            {"value": "no_beep",       "label": "No beeps – completely silent"},
            {"value": "single_beep",   "label": "One beep then stops"},
            {"value": "multiple_beep", "label": "Multiple / repeating beeps"},
        ],
        "relevant_to": ["wont_start"],
        "relevance": {"ram_fault": 0.8, "bad_motherboard": 0.5}
    },
    {
        "id": "q_dropped",
        "text": "Was the laptop dropped or physically impacted recently?",
        "options": [
            {"value": "yes",       "label": "Yes"},
            {"value": "no",        "label": "No"},
            {"value": "maybe",     "label": "Not sure / minor bumps"},
        ],
        "relevant_to": ["wont_start", "display", "noise", "storage"],
        "relevance": {"hdd_failure": 0.5, "display_damage": 0.7, "bad_motherboard": 0.3}
    },
    {
        "id": "q_battery_behavior",
        "text": "What exactly happens with the battery / charging?",
        "options": [
            {"value": "no_charge",      "label": "Battery doesn't charge at all"},
            {"value": "drains_fast",    "label": "Battery drains unusually fast"},
            {"value": "not_detected",   "label": "Battery not detected by OS"},
            {"value": "charge_to_x",    "label": "Only charges up to a certain percentage"},
        ],
        "relevant_to": ["battery"],
        "relevance": {"dead_battery": 0.7, "battery_calibration": 0.4, "power_adapter_fault": 0.5}
    },
    {
        "id": "q_battery_age",
        "text": "How old is the laptop / battery?",
        "options": [
            {"value": "under1",  "label": "Less than 1 year"},
            {"value": "1to3",    "label": "1–3 years"},
            {"value": "3to5",    "label": "3–5 years"},
            {"value": "over5",   "label": "More than 5 years"},
        ],
        "relevant_to": ["battery", "slow", "overheating"],
        "relevance": {"dead_battery": 0.6, "thermal_paste_needed": 0.4, "hdd_failure": 0.3}
    },
    {
        "id": "q_display_type",
        "text": "What does the display issue look like?",
        "options": [
            {"value": "black_screen",   "label": "Completely black screen"},
            {"value": "flickering",     "label": "Flickering or flashing"},
            {"value": "lines",          "label": "Horizontal / vertical lines on screen"},
            {"value": "dim",            "label": "Screen is very dim"},
            {"value": "colors_off",     "label": "Colors are distorted / washed out"},
            {"value": "partial",        "label": "Part of the screen is dead"},
        ],
        "relevant_to": ["display"],
        "relevance": {"display_damage": 0.6, "gpu_fault": 0.5, "backlight_fault": 0.7, "cable_loose": 0.4}
    },
    {
        "id": "q_external_monitor",
        "text": "Does the laptop work normally when connected to an external monitor?",
        "options": [
            {"value": "yes",         "label": "Yes – external monitor works fine"},
            {"value": "no",          "label": "No – same problem on external monitor"},
            {"value": "not_tried",   "label": "Haven't tried"},
        ],
        "relevant_to": ["display"],
        "relevance": {"display_damage": 0.85, "cable_loose": 0.75, "gpu_fault": 0.8}
    },
    {
        "id": "q_slow_when",
        "text": "When does the slowness occur?",
        "options": [
            {"value": "always",      "label": "Always, even on the desktop"},
            {"value": "heavy_tasks", "label": "Only during heavy tasks (gaming, video, etc.)"},
            {"value": "startup",     "label": "Mainly at startup / boot"},
            {"value": "random",      "label": "Randomly / unpredictably"},
        ],
        "relevant_to": ["slow"],
        "relevance": {"low_ram": 0.5, "hdd_failure": 0.6, "malware": 0.4, "thermal_throttling": 0.5}
    },
    {
        "id": "q_disk_type",
        "text": "Does your laptop have an SSD or HDD?",
        "options": [
            {"value": "ssd",       "label": "SSD (solid state)"},
            {"value": "hdd",       "label": "HDD (hard disk / spinning)"},
            {"value": "unknown",   "label": "Not sure"},
        ],
        "relevant_to": ["slow", "storage", "noise"],
        "relevance": {"hdd_failure": 0.7, "storage_full": 0.3}
    },
    {
        "id": "q_ram",
        "text": "How much RAM does the laptop have?",
        "options": [
            {"value": "4gb_less",  "label": "4 GB or less"},
            {"value": "8gb",       "label": "8 GB"},
            {"value": "16gb_plus", "label": "16 GB or more"},
            {"value": "unknown",   "label": "Not sure"},
        ],
        "relevant_to": ["slow", "bluescreen"],
        "relevance": {"low_ram": 0.7, "ram_fault": 0.3}
    },
    {
        "id": "q_heat_location",
        "text": "Where is the laptop getting hot?",
        "options": [
            {"value": "bottom",  "label": "Mostly the bottom"},
            {"value": "sides",   "label": "Vents on the sides / back"},
            {"value": "keyboard","label": "Keyboard area"},
            {"value": "all_over","label": "Everywhere uniformly"},
        ],
        "relevant_to": ["overheating"],
        "relevance": {"fan_blocked": 0.5, "thermal_paste_needed": 0.4}
    },
    {
        "id": "q_fan_working",
        "text": "Can you hear the fan running inside the laptop?",
        "options": [
            {"value": "yes_normal",  "label": "Yes – sounds normal"},
            {"value": "yes_loud",    "label": "Yes – very loud / always at max speed"},
            {"value": "no",          "label": "No – completely silent even when hot"},
        ],
        "relevant_to": ["overheating", "noise"],
        "relevance": {"fan_failure": 0.8, "fan_blocked": 0.4, "thermal_paste_needed": 0.5}
    },
    {
        "id": "q_heat_surface",
        "text": "What surface do you usually use the laptop on?",
        "options": [
            {"value": "desk",    "label": "Hard desk / flat surface"},
            {"value": "bed",     "label": "Bed, pillow, or lap"},
            {"value": "varies",  "label": "Varies"},
        ],
        "relevant_to": ["overheating"],
        "relevance": {"fan_blocked": 0.7}
    },
    {
        "id": "q_noise_type",
        "text": "What kind of noise is the laptop making?",
        "options": [
            {"value": "clicking",   "label": "Clicking or ticking sound"},
            {"value": "grinding",   "label": "Grinding or scraping"},
            {"value": "beeping",    "label": "Beeping on startup"},
            {"value": "loud_fan",   "label": "Very loud fan whirring"},
            {"value": "buzzing",    "label": "Electrical buzzing"},
        ],
        "relevant_to": ["noise"],
        "relevance": {"hdd_failure": 0.8, "fan_failure": 0.7, "ram_fault": 0.6, "bad_motherboard": 0.4}
    },
    {
        "id": "q_noise_when",
        "text": "When does the noise occur?",
        "options": [
            {"value": "startup",    "label": "Only on startup / boot"},
            {"value": "always",     "label": "Constantly while running"},
            {"value": "tasks",      "label": "During heavy tasks"},
            {"value": "idle",       "label": "Even when idle"},
        ],
        "relevant_to": ["noise"],
        "relevance": {"hdd_failure": 0.5, "fan_failure": 0.4, "ram_fault": 0.5}
    },
    {
        "id": "q_wifi_behavior",
        "text": "What's the WiFi issue exactly?",
        "options": [
            {"value": "not_detected",  "label": "WiFi adapter not detected at all"},
            {"value": "connects_drops","label": "Connects but keeps dropping"},
            {"value": "slow_wifi",     "label": "Connected but very slow"},
            {"value": "no_networks",   "label": "No networks visible"},
        ],
        "relevant_to": ["wifi"],
        "relevance": {"wifi_driver": 0.7, "wifi_hardware": 0.6, "router_issue": 0.5}
    },
    {
        "id": "q_wifi_other_devices",
        "text": "Do other devices connect to the same WiFi fine?",
        "options": [
            {"value": "yes",  "label": "Yes – other devices work fine"},
            {"value": "no",   "label": "No – others are also affected"},
        ],
        "relevant_to": ["wifi"],
        "relevance": {"router_issue": 0.9, "wifi_driver": 0.7, "wifi_hardware": 0.6}
    },
    {
        "id": "q_bsod_frequency",
        "text": "How often do the crashes / blue screens happen?",
        "options": [
            {"value": "once",     "label": "Just happened once"},
            {"value": "often",    "label": "Frequently (multiple times a day)"},
            {"value": "startup",  "label": "Every time on startup"},
            {"value": "random",   "label": "Randomly, no clear pattern"},
        ],
        "relevant_to": ["bluescreen"],
        "relevance": {"ram_fault": 0.5, "driver_issue": 0.6, "hdd_failure": 0.5, "malware": 0.3}
    },
    {
        "id": "q_bsod_error_code",
        "text": "Do you see any error code on the blue screen?",
        "options": [
            {"value": "memory",   "label": "MEMORY_MANAGEMENT or similar"},
            {"value": "irql",     "label": "IRQL_NOT_LESS_OR_EQUAL"},
            {"value": "disk",     "label": "CRITICAL_PROCESS_DIED or disk error"},
            {"value": "other",    "label": "Other error code"},
            {"value": "no",       "label": "Screen disappears too fast / no code seen"},
        ],
        "relevant_to": ["bluescreen"],
        "relevance": {"ram_fault": 0.8, "driver_issue": 0.7, "hdd_failure": 0.7}
    },
    {
        "id": "q_storage_symptom",
        "text": "What's happening with storage?",
        "options": [
            {"value": "full",         "label": "Running out of space"},
            {"value": "files_corrupt","label": "Files getting corrupted or missing"},
            {"value": "slow_read",    "label": "Files take very long to open"},
            {"value": "not_detected", "label": "Drive not detected by system"},
        ],
        "relevant_to": ["storage"],
        "relevance": {"storage_full": 0.9, "hdd_failure": 0.7, "file_system_error": 0.6}
    },
]
DIAGNOSES = {
    "power_adapter_fault": {"label": "Faulty Power Adapter", "description": "Your charger or power adapter may be damaged or incompatible.", "fixes": ["Try a different charger with the same wattage", "Check the charging port for bent pins or debris", "Test with a known working adapter"], "severity": "medium"},
    "dead_battery": {"label": "Dead / Degraded Battery", "description": "The battery has reached end-of-life or has failed.", "fixes": ["Replace the battery (contact manufacturer or a repair shop)", "Check battery health in BIOS or via BatteryInfoView tool", "If under warranty, claim replacement"], "severity": "medium"},
    "battery_calibration": {"label": "Battery Calibration Issue", "description": "The battery meter is inaccurate – common after long storage.", "fixes": ["Fully discharge then fully charge the battery", "Run a battery calibration in BIOS if available", "Use Windows Battery Report: run `powercfg /batteryreport` in CMD"], "severity": "low"},
    "bad_motherboard": {"label": "Motherboard / Hardware Fault", "description": "A component on the motherboard may have failed.", "fixes": ["This requires professional diagnosis", "Check if laptop is under warranty", "Avoid DIY unless experienced — consult a repair center"], "severity": "high"},
    "ram_fault": {"label": "RAM (Memory) Issue", "description": "Your RAM sticks may be faulty, loose, or incompatible.", "fixes": ["Remove and reseat RAM sticks (if accessible)", "Run Windows Memory Diagnostic: search 'mdsched.exe'", "Try using one RAM stick at a time to isolate the faulty one", "Replace faulty RAM module"], "severity": "high"},
    "hdd_failure": {"label": "Hard Drive Failing", "description": "Your HDD/SSD shows signs of failure — back up your data immediately!", "fixes": ["URGENT: Back up all important files NOW", "Run CHKDSK: open CMD as admin → `chkdsk C: /f /r`", "Check S.M.A.R.T. status with CrystalDiskInfo (free tool)", "Replace the drive if errors are found"], "severity": "critical"},
    "display_damage": {"label": "Screen / Display Panel Damage", "description": "The LCD panel itself appears to be physically damaged.", "fixes": ["Use an external monitor as a workaround", "Screen replacement by a repair shop (check cost vs laptop value)", "If recent drop/impact, check warranty coverage"], "severity": "high"},
    "gpu_fault": {"label": "GPU / Graphics Card Issue", "description": "The graphics processor may be overheating or failing.", "fixes": ["Update GPU drivers (Device Manager → Display Adapters)", "Clean laptop vents to improve cooling", "If dedicated GPU: try switching to integrated graphics", "Stress test with GPU-Z or FurMark to confirm"], "severity": "high"},
    "backlight_fault": {"label": "Screen Backlight Failure", "description": "The screen's backlight may have failed — common in older laptops.", "fixes": ["Shine a flashlight at the screen; if you see a faint image, it's the backlight", "Backlight or inverter replacement needed (repair shop)", "Use external monitor if feasible"], "severity": "medium"},
    "cable_loose": {"label": "Loose Display Cable", "description": "The ribbon cable connecting the screen to the motherboard may be loose.", "fixes": ["Open lid fully and partially — if image changes, cable is the culprit", "A technician can reseat the display cable", "Relatively cheap repair if diagnosed correctly"], "severity": "medium"},
    "thermal_throttling": {"label": "Thermal Throttling", "description": "CPU is slowing itself down to prevent overheating.", "fixes": ["Clean the vents and fan with compressed air", "Elevate the laptop for better airflow", "Check Task Manager → Performance tab for CPU temps", "Consider repasting thermal compound"], "severity": "medium"},
    "thermal_paste_needed": {"label": "Degraded Thermal Paste", "description": "The thermal paste between CPU/GPU and heatsink has dried out.", "fixes": ["Reapply high-quality thermal paste (Thermal Grizzly, Arctic MX-4)", "Clean old paste with isopropyl alcohol", "This is a DIY-friendly fix if you're comfortable opening the laptop"], "severity": "medium"},
    "fan_failure": {"label": "Cooling Fan Failure", "description": "The laptop fan isn't working properly — overheating is imminent.", "fixes": ["Replace the fan (model-specific, search your model on iFixit)", "Check BIOS for fan control settings", "Use HWMonitor to check fan RPM"], "severity": "high"},
    "fan_blocked": {"label": "Fan / Vents Blocked", "description": "The cooling vents are blocked by dust or usage on soft surfaces.", "fixes": ["Use compressed air to blow out dust from vents", "Always use on a hard flat surface", "Consider a cooling pad"], "severity": "low"},
    "low_ram": {"label": "Insufficient RAM", "description": "Your system doesn't have enough RAM for current workloads.", "fixes": ["Close background apps and browser tabs", "Upgrade RAM if slots are available", "Add a page file / virtual memory (System → Advanced → Performance)"], "severity": "medium"},
    "malware": {"label": "Malware / Virus Infection", "description": "Malicious software may be consuming resources or causing crashes.", "fixes": ["Run Malwarebytes (free) full scan", "Use Windows Defender Offline Scan", "Check Task Manager for unfamiliar high-CPU processes", "Avoid downloading from untrusted sources"], "severity": "high"},
    "storage_full": {"label": "Storage Almost Full", "description": "Your drive is nearly full, which causes slowdowns and errors.", "fixes": ["Run Disk Cleanup (search in Start Menu)", "Uninstall unused programs", "Move files to external drive or cloud storage", "Check large files with WinDirStat"], "severity": "low"},
    "file_system_error": {"label": "File System Corruption", "description": "The file system has errors due to improper shutdowns or disk issues.", "fixes": ["Run CHKDSK: CMD as admin → `chkdsk C: /f /r` then restart", "Run SFC: `sfc /scannow` in admin CMD", "Check disk health with CrystalDiskInfo"], "severity": "medium"},
    "wifi_driver": {"label": "WiFi Driver Issue", "description": "A corrupted or outdated WiFi driver is causing connectivity problems.", "fixes": ["Device Manager → Network Adapters → Update driver", "Or uninstall driver and let Windows reinstall", "Download latest driver from laptop manufacturer's site"], "severity": "low"},
    "wifi_hardware": {"label": "WiFi Hardware Failure", "description": "The WiFi adapter hardware may be faulty or disabled.", "fixes": ["Check if WiFi is disabled in BIOS", "Try a USB WiFi adapter as workaround", "WiFi card replacement (relatively affordable)"], "severity": "medium"},
    "router_issue": {"label": "Router / Network Issue", "description": "The problem may be with your router or ISP, not the laptop.", "fixes": ["Restart your router (unplug for 30 seconds)", "Try connecting to a different WiFi network", "Contact your ISP if others are also affected"], "severity": "low"},
    "driver_issue": {"label": "Driver Conflict / Outdated Driver", "description": "A device driver is causing system instability.", "fixes": ["Update all drivers via Device Manager", "Use DDU (Display Driver Uninstaller) for GPU driver issues", "Check Windows Event Viewer for specific driver errors", "Roll back a recently updated driver"], "severity": "medium"},
}
SCORING_RULES = {
    ("q_main_symptom", "wont_start"): {"power_adapter_fault": 0.4, "dead_battery": 0.3, "bad_motherboard": 0.2, "ram_fault": 0.1},
    ("q_main_symptom", "slow"): {"low_ram": 0.4, "hdd_failure": 0.3, "malware": 0.3, "thermal_throttling": 0.2, "storage_full": 0.2},
    ("q_main_symptom", "battery"): {"dead_battery": 0.5, "power_adapter_fault": 0.4, "battery_calibration": 0.2},
    ("q_main_symptom", "display"): {"display_damage": 0.4, "gpu_fault": 0.3, "backlight_fault": 0.3, "cable_loose": 0.3},
    ("q_main_symptom", "overheating"): {"fan_failure": 0.4, "fan_blocked": 0.4, "thermal_paste_needed": 0.4, "thermal_throttling": 0.3},
    ("q_main_symptom", "noise"): {"hdd_failure": 0.5, "fan_failure": 0.4, "ram_fault": 0.2},
    ("q_main_symptom", "wifi"): {"wifi_driver": 0.5, "wifi_hardware": 0.4, "router_issue": 0.3},
    ("q_main_symptom", "keyboard"): {},
    ("q_main_symptom", "storage"): {"hdd_failure": 0.4, "storage_full": 0.4, "file_system_error": 0.3},
    ("q_main_symptom", "bluescreen"): {"ram_fault": 0.4, "driver_issue": 0.4, "hdd_failure": 0.3, "malware": 0.2},
    ("q_power_led", "no"): {"power_adapter_fault": 0.5, "dead_battery": 0.4, "bad_motherboard": 0.3},
    ("q_power_led", "yes_brief"): {"dead_battery": 0.4, "bad_motherboard": 0.3},
    ("q_power_led", "yes_all"): {"bad_motherboard": 0.2, "ram_fault": 0.3},
    ("q_charger_check", "yes_fixed"): {"power_adapter_fault": 0.95},
    ("q_charger_check", "yes_works"): {"power_adapter_fault": -0.5, "dead_battery": 0.4, "bad_motherboard": 0.3},
    ("q_beep_codes", "multiple_beep"): {"ram_fault": 0.8, "bad_motherboard": 0.4},
    ("q_beep_codes", "no_beep"): {"bad_motherboard": 0.3},
    ("q_dropped", "yes"): {"hdd_failure": 0.5, "display_damage": 0.6, "bad_motherboard": 0.3},
    ("q_battery_behavior", "no_charge"): {"power_adapter_fault": 0.5, "dead_battery": 0.5},
    ("q_battery_behavior", "drains_fast"): {"dead_battery": 0.6, "battery_calibration": 0.3},
    ("q_battery_behavior", "not_detected"): {"dead_battery": 0.7, "bad_motherboard": 0.2},
    ("q_battery_age", "over5"): {"dead_battery": 0.6},
    ("q_battery_age", "3to5"): {"dead_battery": 0.3},
    ("q_display_type", "black_screen"): {"backlight_fault": 0.6, "gpu_fault": 0.4, "cable_loose": 0.4},
    ("q_display_type", "flickering"): {"cable_loose": 0.7, "gpu_fault": 0.5},
    ("q_display_type", "lines"): {"display_damage": 0.7, "gpu_fault": 0.5},
    ("q_display_type", "dim"): {"backlight_fault": 0.8},
    ("q_external_monitor", "yes"): {"display_damage": 0.8, "cable_loose": 0.8, "backlight_fault": 0.7},
    ("q_external_monitor", "no"): {"gpu_fault": 0.8, "display_damage": -0.3},
    ("q_slow_when", "always"): {"low_ram": 0.5, "malware": 0.4, "hdd_failure": 0.4},
    ("q_slow_when", "startup"): {"hdd_failure": 0.5, "storage_full": 0.3, "malware": 0.3},
    ("q_slow_when", "heavy_tasks"): {"thermal_throttling": 0.6, "low_ram": 0.4},
    ("q_disk_type", "hdd"): {"hdd_failure": 0.4},
    ("q_disk_type", "ssd"): {"hdd_failure": -0.2},
    ("q_ram", "4gb_less"): {"low_ram": 0.7},
    ("q_ram", "8gb"): {"low_ram": 0.3},
    ("q_heat_location", "sides"): {"fan_blocked": 0.5},
    ("q_fan_working", "no"): {"fan_failure": 0.9},
    ("q_fan_working", "yes_loud"): {"fan_blocked": 0.5, "thermal_paste_needed": 0.5},
    ("q_heat_surface", "bed"): {"fan_blocked": 0.7},
    ("q_noise_type", "clicking"): {"hdd_failure": 0.9},
    ("q_noise_type", "grinding"): {"hdd_failure": 0.8, "fan_failure": 0.5},
    ("q_noise_type", "beeping"): {"ram_fault": 0.7, "bad_motherboard": 0.4},
    ("q_noise_type", "loud_fan"): {"fan_blocked": 0.6, "thermal_paste_needed": 0.4},
    ("q_wifi_behavior", "not_detected"): {"wifi_hardware": 0.7, "wifi_driver": 0.6},
    ("q_wifi_behavior", "connects_drops"): {"wifi_driver": 0.6, "router_issue": 0.5},
    ("q_wifi_other_devices", "no"): {"router_issue": 0.9},
    ("q_wifi_other_devices", "yes"): {"router_issue": -0.6, "wifi_driver": 0.5, "wifi_hardware": 0.5},
    ("q_bsod_error_code", "memory"): {"ram_fault": 0.85},
    ("q_bsod_error_code", "irql"): {"driver_issue": 0.8},
    ("q_bsod_error_code", "disk"): {"hdd_failure": 0.8},
    ("q_bsod_frequency", "often"): {"ram_fault": 0.5, "driver_issue": 0.4},
    ("q_bsod_frequency", "startup"): {"hdd_failure": 0.6, "ram_fault": 0.5},
    ("q_storage_symptom", "full"): {"storage_full": 0.9},
    ("q_storage_symptom", "files_corrupt"): {"hdd_failure": 0.8, "file_system_error": 0.6},
    ("q_storage_symptom", "slow_read"): {"hdd_failure": 0.5, "storage_full": 0.3},
    ("q_storage_symptom", "not_detected"): {"hdd_failure": 0.9},
}
SYMPTOM_QUESTION_MAP = {
    "wont_start":    ["q_power_led", "q_charger_check", "q_beep_codes", "q_dropped"],
    "battery":       ["q_battery_behavior", "q_charger_check", "q_battery_age"],
    "display":       ["q_display_type", "q_external_monitor", "q_dropped"],
    "slow":          ["q_slow_when", "q_disk_type", "q_ram", "q_battery_age"],
    "overheating":   ["q_heat_location", "q_fan_working", "q_heat_surface", "q_battery_age"],
    "noise":         ["q_noise_type", "q_noise_when", "q_fan_working", "q_disk_type"],
    "wifi":          ["q_wifi_behavior", "q_wifi_other_devices"],
    "keyboard":      [], 
    "storage":       ["q_storage_symptom", "q_disk_type"],
    "bluescreen":    ["q_bsod_frequency", "q_bsod_error_code", "q_ram", "q_disk_type"],
}
def get_question_by_id(qid):
    return next((q for q in QUESTIONS if q["id"] == qid), None)
def compute_scores(answers):
    scores = {diag: 0.0 for diag in DIAGNOSES}
    for (qid, val), boosts in SCORING_RULES.items():
        if answers.get(qid) == val:
            for diag, boost in boosts.items():
                if diag in scores:
                    scores[diag] = min(1.0, max(0.0, scores[diag] + boost))
    return scores
def get_next_question_id(answers, asked_ids):
    main = answers.get("q_main_symptom")
    if not main:
        return "q_main_symptom"
    queue = SYMPTOM_QUESTION_MAP.get(main, [])
    for qid in queue:
        if qid not in asked_ids:
            return qid
    return None
def get_all_ranked_diagnoses(scores):
    sorted_diags = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_diags
def format_results(top_diags):
    results = []
    for diag_id, score in top_diags:
        d = DIAGNOSES[diag_id]
        results.append({
            "id": diag_id,
            "label": d["label"],
            "description": d["description"],
            "fixes": d["fixes"],
            "severity": d["severity"],
            "confidence": round(score * 100)
        })
    return results
@app.route("/")
def index():
    session.clear()
    return render_template("index.html")
@app.route("/api/start", methods=["POST"])
def start():
    session["answers"] = {}
    session["asked"] = []
    first_q = get_question_by_id("q_main_symptom")
    return jsonify({"question": first_q})
@app.route("/api/answer", methods=["POST"])
def answer():
    data = request.json
    qid = data["question_id"]
    val = data["answer"]
    answers = session.get("answers", {})
    asked = session.get("asked", [])
    answers[qid] = val
    if qid not in asked:
        asked.append(qid)
    session["answers"] = answers
    session["asked"] = asked
    scores = compute_scores(answers)
    ranked_diags = get_all_ranked_diagnoses(scores)
    next_qid = get_next_question_id(answers, asked)
    is_decisive = False
    if len(ranked_diags) > 1:
        top_score = ranked_diags[0][1]
        runner_up_score = ranked_diags[1][1]
        if top_score >= 0.85 and (top_score - runner_up_score >= 0.30):
            is_decisive = True
    elif len(ranked_diags) == 1 and ranked_diags[0][1] > 0:
        is_decisive = True
    if is_decisive or next_qid is None:
        decisive_result = ranked_diags[:1] 
        return jsonify({"done": True, "diagnoses": format_results(decisive_result)})
    next_q = get_question_by_id(next_qid)
    asked_count = len(asked)
    total_expected = 1 + len(SYMPTOM_QUESTION_MAP.get(answers.get("q_main_symptom",""), []))
    return jsonify({
        "done": False,
        "question": next_q,
        "progress": {"asked": asked_count, "total": total_expected}
    })
if __name__ == "__main__":
    app.run(debug=True)