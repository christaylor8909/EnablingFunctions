import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import os

# -----------------------
# FILE PICKER
# -----------------------
Tk().withdraw()
excel_path = filedialog.askopenfilename(title="Select Accreditation File", filetypes=[("Excel Files", "*.xlsx *.xls")])

if not excel_path:
    raise Exception("❌ No file selected.")

print(f"✅ File selected: {excel_path}")

# -----------------------
# LOAD DATA → Dynamic header finder
# -----------------------
raw_df = pd.read_excel(excel_path, header=None)

# Find header row
header_row = None
for i, row in raw_df.iterrows():
    row_values = row.astype(str).str.lower()
    if "completion percentage" in row_values.values:
        header_row = i
        break

if header_row is None:
    raise Exception("❌ Could not find header row automatically. Please check the file.")

print("✅ Detected header row at:", header_row)

# Load with correct header
df = pd.read_excel(excel_path, header=header_row)

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Detect Completion % column
completion_column = [col for col in df.columns if "completion_percentage" in col][0]

# Convert to numeric
df[completion_column] = pd.to_numeric(df[completion_column], errors='coerce')

# -----------------------
# HISTOGRAM → Completion Percentage Distribution
# -----------------------
plt.figure(figsize=(10, 6))
df[completion_column].dropna().plot(kind="hist", bins=10, color='blue', edgecolor='black')

plt.title("Completion Percentage Distribution")
plt.xlabel("Completion Percentage")
plt.ylabel("Number of Users")
plt.tight_layout()

# Save to PNG
output_folder = os.path.dirname(excel_path)
histogram_path = os.path.join(output_folder, "Completion_Percentage_Distribution.png")
plt.savefig(histogram_path, dpi=300)
print("✅ Saved Histogram to", histogram_path)

plt.show()
