import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# --------------------
# LOAD FILE
# --------------------
Tk().withdraw()
excel_path = filedialog.askopenfilename(title="Select Accreditation File", filetypes=[("Excel Files", "*.xlsx *.xls")])

if not excel_path:
    raise Exception("❌ No file selected.")

print(f"✅ File selected: {excel_path}")

# Load Excel, skip first 2 metadata rows
df = pd.read_excel(excel_path, header=2)

# Clean columns
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

print(f"✅ Columns loaded: {list(df.columns)}")

# --------------------
# Validate required columns
# --------------------
required_columns = ["oic_name", "curriculum_status"]
for col in required_columns:
    if col not in df.columns:
        raise Exception(f"❌ ERROR: Required column '{col}' not found in Excel file!")

# --------------------
# Get available dealerships (clean them)
# --------------------
df["oic_name_clean"] = df["oic_name"].astype(str).str.strip().str.lower()
unique_dealers = sorted(df["oic_name_clean"].dropna().unique())
print("\nAvailable Dealerships:")
for dealer in unique_dealers:
    print("-", dealer.title())

dealer_input = input("\nEnter dealership name exactly as shown above: ").strip().lower()

if dealer_input not in unique_dealers:
    raise Exception("❌ ERROR: Dealership not found. Please enter exactly as shown.")

# --------------------
# Filter for selected dealership
# --------------------
dealer_df = df[df["oic_name_clean"] == dealer_input]

if dealer_df.empty:
    raise Exception("❌ ERROR: No training data found for this dealership!")

print(f"✅ Found {dealer_df.shape[0]} training records for '{dealer_input.title()}'")

# --------------------
# Clean Curriculum Status and classify
# --------------------
dealer_df["curriculum_status"] = dealer_df["curriculum_status"].astype(str).str.strip().str.lower()

# Classify as Completed or Not Completed
dealer_df["completion_group"] = dealer_df["curriculum_status"].apply(
    lambda x: "Completed" if "complete" in x and "not" not in x else "Not Completed"
)

# --------------------
# Calculate summary
# --------------------
completion_summary = dealer_df["completion_group"].value_counts()
print("\n✅ COMPLETION SUMMARY:")
print(completion_summary)

# --------------------
# PLOT
# --------------------
plt.figure(figsize=(8, 6))
colors = ['green' if status == "Completed" else 'red' for status in completion_summary.index]

plt.bar(completion_summary.index, completion_summary.values, color=colors)
plt.title(f"Training Completion - {dealer_input.title()}")
plt.xlabel("Status")
plt.ylabel("Number of Trainings")
plt.tight_layout()
plt.show()
