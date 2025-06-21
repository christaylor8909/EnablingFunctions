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
# LOAD DATA → DYNAMIC HEADER FINDER
# -----------------------
raw_df = pd.read_excel(excel_path, header=None)

# Detect header row
header_row = None
for i, row in raw_df.iterrows():
    row_values = row.astype(str).str.lower()
    if "curriculum status" in row_values.values or "user brand" in row_values.values:
        header_row = i
        break

if header_row is None:
    raise Exception("❌ Could not find header row automatically. Please check the file.")

print("✅ Detected header row at:", header_row)

# Load with correct header
df = pd.read_excel(excel_path, header=header_row)

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

print("✅ Cleaned Columns:", df.columns.tolist())

# -----------------------
# AUTO DETECT COLUMN NAMES
# -----------------------
brand_column = [col for col in df.columns if "brand" in col][0]
job_column = [col for col in df.columns if "job" in col][0]
completion_column = [col for col in df.columns if "completion_percentage" in col][0]
status_column = [col for col in df.columns if "curriculum_status" in col][0]

print("✅ Detected Columns → Brand:", brand_column, "| Job:", job_column, "| Completion %:", completion_column, "| Status:", status_column)

# DROP rows with missing brand/job
df = df.dropna(subset=[brand_column, job_column])

# OUTPUT FOLDER
output_folder = os.path.dirname(excel_path)

# -----------------------
# BAR CHART → Completion Status by User Brand
# -----------------------
status_counts = df.groupby([brand_column, status_column]).size().unstack(fill_value=0)

plt.figure(figsize=(12, 7))
status_counts.plot(kind="bar", stacked=True, color=["red", "green"])
plt.title("Completion Status by User Brand")
plt.xlabel("User Brand")
plt.ylabel("Number of Users")
plt.xticks(rotation=45)
plt.legend(title="Curriculum Status")
plt.tight_layout()

bar_chart_path = os.path.join(output_folder, "Completion_Status_by_Brand.png")
plt.savefig(bar_chart_path, dpi=300)
print("✅ Saved Bar Chart to", bar_chart_path)
plt.show()

# -----------------------
# HISTOGRAM → Completion Percentage Distribution
# -----------------------
plt.figure(figsize=(10, 6))
df[completion_column] = pd.to_numeric(df[completion_column], errors='coerce')
df[completion_column].dropna().plot(kind="hist", bins=10, color='blue', edgecolor='black')

plt.title("Completion Percentage Distribution")
plt.xlabel("Completion Percentage")
plt.ylabel("Number of Users")
plt.tight_layout()

histogram_path = os.path.join(output_folder, "Completion_Percentage_Distribution.png")
plt.savefig(histogram_path, dpi=300)
print("✅ Saved Histogram to", histogram_path)
plt.show()

# -----------------------
# PIE CHART → Overall Completion Status
# -----------------------
completed_total = df[df[status_column] == "Completed"].shape[0]
not_completed_total = df[df[status_column] != "Completed"].shape[0]

plt.figure(figsize=(8, 8))
plt.pie([completed_total, not_completed_total], labels=["Completed", "Not Completed"],
        autopct="%1.1f%%", startangle=140, colors=["green", "red"])
plt.title("Overall Completion Status")
plt.tight_layout()

pie_chart_path = os.path.join(output_folder, "Overall_Completion_Pie.png")
plt.savefig(pie_chart_path, dpi=300)
print("✅ Saved Pie Chart to", pie_chart_path)
plt.show()

print("\n✅✅✅ ALL VISUALISATIONS COMPLETED AND SAVED SUCCESSFULLY.")
