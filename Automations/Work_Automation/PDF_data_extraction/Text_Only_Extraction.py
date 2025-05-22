import pdfplumber
import pandas as pd
import re
import os
from datetime import datetime

# -----------------------
# CONFIGURATION (Auto path detection)
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_folder = os.path.normpath(os.path.join(BASE_DIR, "..", "Service_Thankyou_Repo"))

print(f"📂 Reading PDFs from: {pdf_folder}")

if not os.path.exists(pdf_folder):
    raise FileNotFoundError(f"❌ Folder not found: {pdf_folder}")

# -----------------------
# Extraction function
# -----------------------
def extract_data(pdf_path):
    extracted_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    # Dealership Number and Name
    dealership_match = re.search(r"Dealership\s+([A-Z0-9]+)\s*-\s*(.*?)\n", full_text)
    extracted_data["Dealership Number"] = dealership_match.group(1).strip() if dealership_match else ""
    extracted_data["Dealership Name"] = dealership_match.group(2).strip() if dealership_match else ""

    # Clean Survey Sent Date (avoid picking up extra "Response Date")
    sent_match = re.search(r"Survey Sent Date\s+([0-9]{1,2} \w+ 20[0-9]{2})", full_text)
    extracted_data["Survey Sent Date"] = sent_match.group(1).strip() if sent_match else ""

    # Other fields
    patterns = {
        "Response Date": r"Response Date\s+([0-9]{1,2} \w+ 20[0-9]{2})",
        "Customer": r"Customer\s+(.*?)\s+Result received",
        "Vehicle Model": r"Vehicle Model\s+(.*)",
        "VIN": r"VIN\s+([A-HJ-NPR-Z0-9]{10,20})",
        "Warranty Start": r"Warranty Start\s+(.*)",
        "Rego": r"Rego\s+(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, full_text)
        extracted_data[key] = match.group(1).strip() if match else ""

    # Q2 Verbatim
    q2_match = re.search(r"Q02\..*?\n", full_text, re.IGNORECASE)
    q3_match = re.search(r"Q03\.", full_text, re.IGNORECASE)
    if q2_match:
        q2_start = q2_match.end()
        if q3_match:
            verbatim = full_text[q2_start:q3_match.start()]
        else:
            verbatim = full_text[q2_start:]
        verbatim = re.sub(r"\n+", " ", verbatim).strip()
        extracted_data["Verbatim"] = verbatim
    else:
        extracted_data["Verbatim"] = ""

    return extracted_data

# -----------------------
# Process PDFs
# -----------------------
data = []
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"🔍 Processing {filename}...")
        record = extract_data(pdf_path)
        record["PDF File"] = filename
        data.append(record)

# -----------------------
# Export to Excel
# -----------------------
df = pd.DataFrame(data)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_excel = os.path.join(pdf_folder, f"All_Service_Data_{timestamp}.xlsx")
df.to_excel(output_excel, index=False)

print(f"\n✅ Done! Saved to {output_excel}")
