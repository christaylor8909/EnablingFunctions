import os
import re
import pandas as pd
import pdfplumber
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
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Dealership Number and Name
    dealership_match = re.search(r"Dealership\s+([A-Z0-9]+)\s*-\s*(.*?)(?:\s+\(Staff|\n)", full_text)
    extracted_data["Dealership Number"] = dealership_match.group(1).strip() if dealership_match else ""
    extracted_data["Dealership Name"] = dealership_match.group(2).strip() if dealership_match else ""

    # Standard patterns
    patterns = {
        "Survey Sent Date": r"Survey Sent Date\s+([0-9]{1,2} \w+ 20[0-9]{2})",
        "Response Date": r"Response Date\s+([0-9]{1,2} \w+ 20[0-9]{2})",
        "Customer": r"Customer\s+(.*)",
        "Vehicle Model": r"Vehicle Model\s+(.*)",
        "VIN": r"VIN\s+([A-HJ-NPR-Z0-9]{10,20})",
        "Warranty Start": r"Warranty Start\s+(.*)",
        "Rego": r"Rego\s+(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, full_text)
        extracted_data[key] = match.group(1).strip() if match else ""

    # Q2 Verbatim
    q2_match = re.search(r"Q02\..*?\n(.*?)(?=\nQ03\.|\nQ03)", full_text, re.DOTALL | re.IGNORECASE)
    extracted_data["Verbatim"] = re.sub(r"\n+", " ", q2_match.group(1)).strip() if q2_match else ""

    # Q3 Follow-up Consent
    if "Q03." in full_text:
        if re.search(r"Q03\..*?✔\s*Yes", full_text, re.IGNORECASE | re.DOTALL):
            extracted_data["Follow-up Consent"] = "Yes"
        elif re.search(r"Q03\..*?✘\s*No", full_text, re.IGNORECASE | re.DOTALL):
            extracted_data["Follow-up Consent"] = "No"
        else:
            extracted_data["Follow-up Consent"] = "Unclear"
    else:
        extracted_data["Follow-up Consent"] = ""

    # Save full PDF path
    extracted_data["PDF Path"] = pdf_path
    return extracted_data

# -----------------------
# Process all PDFs
# -----------------------
data = []
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        full_path = os.path.join(pdf_folder, filename)
        print(f"🔍 Processing: {filename}")
        record = extract_data(full_path)
        data.append(record)

# -----------------------
# Export to Excel
# -----------------------
df = pd.DataFrame(data)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output_excel = os.path.join(pdf_folder, f"All_Service_Data_{timestamp}.xlsx")
df.to_excel(output_excel, index=False)

print(f"\n✅ Done! Saved to {output_excel}")
