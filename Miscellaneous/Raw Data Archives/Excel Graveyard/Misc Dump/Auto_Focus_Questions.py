import os
from PIL import Image, ImageEnhance
import pytesseract
import pandas as pd

# Paths
folder = r"C:\Users\t0355lp\.vscode\Python\NPS Report Automations"
output_excel = os.path.join(folder, "focus_summary_auto.xlsx")
image_extensions = [".png", ".jpg", ".jpeg"]

# OCR helper
def ocr_text(image_crop):
    img = image_crop.convert("L")
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = img.point(lambda p: p > 160 and 255)
    text = pytesseract.image_to_string(img, config="--psm 6")
    return [line.strip() for line in text.split("\n") if line.strip()]

# Load Excel or create
if os.path.exists(output_excel):
    df_master = pd.read_excel(output_excel)
else:
    df_master = pd.DataFrame()

# Process images
for file in os.listdir(folder):
    if any(file.lower().endswith(ext) for ext in image_extensions):
        path = os.path.join(folder, file)
        base_name = os.path.splitext(file)[0]

        img = Image.open(path)
        width, height = img.size

        # Crop left (labels) and right (scores)
        left_box = (0, 0, width * 0.6, height)
        right_box = (width * 0.6, 0, width, height)

        labels_img = img.crop(left_box)
        scores_img = img.crop(right_box)

        labels = ocr_text(labels_img)
        scores = ocr_text(scores_img)

        # Match if lengths align
        if len(labels) != len(scores):
            print(f"⚠️ Mismatch in {file}: {len(labels)} labels vs {len(scores)} scores")
            continue

        try:
            scores_float = [float(s) for s in scores]
        except ValueError:
            print(f"⚠️ Failed to convert some scores in {file}.")
            continue

        df_temp = pd.DataFrame({
            "National Summary - Focus": labels,
            base_name: scores_float
        })

        # Merge into master
        if df_master.empty:
            df_master = df_temp
        else:
            df_master = pd.merge(df_master, df_temp, on="National Summary - Focus", how="outer")

# Save
try:
    df_master.to_excel(output_excel, index=False)
    print(f"✅ Excel updated: {output_excel}")
except PermissionError:
    print(f"❌ File is open. Close {output_excel} and run again.")
