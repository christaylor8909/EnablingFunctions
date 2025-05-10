import pdfplumber
import pandas as pd
import re
import os
from datetime import datetime

# -----------------------
# CONFIGURATION
# -----------------------
pdf_folder = r"C:\Users\t0355lp\.vscode\Python\Automation Files"

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

    # ---------- Dealership split ----------
    dealership_match = re.search(r"Dealership\s+([A-Z0-9]+)\s*-\s*(.*)", full_text)
    if dealership_match:
        extracted_data["Dealership Number"] = dealership_match.group(1).strip()
        extracted_data["Dealership Name"] = dealership_match.group(2).strip()
    else:
        extracted_data["Dealership Number"] = ""
        extracted_data["Dealership Name"] = ""

    # ---------- Other Patterns ----------
    patterns = {
        "Survey Sent Date": r"Survey Sent Date\s+(.*)",
        "Response Date": r"Response Date\s+(.*)",
        "Customer": r"Customer\s+(.*?)\s+Result received",
        "Vehicle Model": r"Vehicle Model\s+(.*)",
        "VIN": r"VIN\s+([A-HJ-NPR-Z0-9]{10,20})",  # VIN fix (no rego)
        "Warranty Start": r"Warranty Start\s+(.*)",
        "Rego": r"Rego\s+(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, full_text)
        extracted_data[key] = match.group(1).strip() if match else ""

    # ---------- Q2 Verbatim ----------
    q2_regex = re.compile(r"Q02\..*?\n", re.IGNORECASE)
    q3_regex = re.compile(r"Q03\.", re.IGNORECASE)

    q2_match = q2_regex.search(full_text)
    if q2_match:
        q2_start = q2_match.end()
        q3_match = q3_regex.search(full_text, q2_start)

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
# Process all PDFs
# -----------------------
data = []

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing {filename}...")
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
