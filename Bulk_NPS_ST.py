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

# Always use correct installed tesseract path
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
            if page.extract_text():
                full_text += page.extract_text() + "\n"

    # Extract fields using regex
    extracted_data["Dealership"] = re.search(r"Dealership\s+(.*)", full_text).group(1).strip() if re.search(r"Dealership\s+(.*)", full_text) else ""
    extracted_data["Survey Sent Date"] = re.search(r"Survey Sent Date\s+(.*)", full_text).group(1).strip() if re.search(r"Survey Sent Date\s+(.*)", full_text) else ""
    extracted_data["Response Date"] = re.search(r"Response Date\s+(.*)", full_text).group(1).strip() if re.search(r"Response Date\s+(.*)", full_text) else ""
    extracted_data["Customer"] = re.search(r"Customer\s+(.*?)\s+Result received", full_text).group(1).strip() if re.search(r"Customer\s+(.*?)\s+Result received", full_text) else ""
    extracted_data["Vehicle Model"] = re.search(r"Vehicle Model\s+(.*)", full_text).group(1).strip() if re.search(r"Vehicle Model\s+(.*)", full_text) else ""
    extracted_data["VIN"] = re.search(r"VIN\s+(.*)", full_text).group(1).strip() if re.search(r"VIN\s+(.*)", full_text) else ""
    extracted_data["Warranty Start"] = re.search(r"Warranty Start\s+(.*)", full_text).group(1).strip() if re.search(r"Warranty Start\s+(.*)", full_text) else ""
    extracted_data["Rego"] = re.search(r"Rego\s+(.*)", full_text).group(1).strip() if re.search(r"Rego\s+(.*)", full_text) else ""

    # Extract Q2 Verbatim
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
        extracted_data["Verbatim"] = re.sub(r"\n+", " ", verbatim.strip())
    else:
        extracted_data["Verbatim"] = ""

    # -----------------------
    # OCR + Green color detection for Approval
    # -----------------------
    doc = fitz.open(pdf_path)
    approval = "No"  # default

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT)

        for i, text in enumerate(ocr_data["text"]):
            if text.strip().lower() == "yes":
                left = ocr_data['left'][i]
                top = ocr_data['top'][i]
                check_x = left + 10
                check_y = top + 10

                if check_x < img.width and check_y < img.height:
                    pixel = img.getpixel((check_x, check_y))
                    if pixel[1] > 150 and pixel[0] < 100 and pixel[2] < 100:  # Green
                        approval = "Yes"
                        break

        if approval == "Yes":
            break

    extracted_data["Approval"] = approval

    return extracted_data

# -----------------------
# Process PDFs
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
