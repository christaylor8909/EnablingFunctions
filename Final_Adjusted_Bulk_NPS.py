import pdfplumber
import pytesseract
from pytesseract import Output
import pandas as pd
import re
import os
from datetime import datetime
from PIL import Image
import fitz  # PyMuPDF

# -----------------------
# CONFIGURATION
# -----------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\t0355lp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
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

    # ---------- Q3 Approval ----------
    doc = fitz.open(pdf_path)
    approval = "No"

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT)

        yes_location = None
        no_location = None
        tick_location = None

        # Detect Yes/No text locations
        for i, text in enumerate(ocr_data["text"]):
            text_clean = text.strip().lower()
            if text_clean == "yes":
                yes_location = (ocr_data['left'][i], ocr_data['top'][i])
            elif text_clean == "no":
                no_location = (ocr_data['left'][i], ocr_data['top'][i])

        # Detect green tick (search all pixels for green)
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = img.getpixel((x, y))
                if g > 150 and r < 120 and b < 120:
                    tick_location = (x, y)
                    break
            if tick_location:
                break

        # Decide approval based on proximity
        def distance(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

        if tick_location:
            if yes_location and no_location:
                yes_dist = distance(tick_location, yes_location)
                no_dist = distance(tick_location, no_location)

                approval = "Yes" if yes_dist < no_dist else "No"

    extracted_data["Approval"] = approval

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
