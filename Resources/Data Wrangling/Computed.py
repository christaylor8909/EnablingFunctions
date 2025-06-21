import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
import os

# === GUI: Select Excel file ===
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select your CEC forecast Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)
if not file_path:
    raise FileNotFoundError("❌ No file selected.")

# === Load and clean dataframe ===
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# === Clean 'Month' column ===
month_map = {
    'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
    'Jun': 'June', 'Jul': 'July', 'Aug': 'August', 'Sep': 'September',
    'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
}
df['Month'] = df['Month'].astype(str).str.strip().str.title().replace(month_map)

# === Clean forecast stage from 'Estimate No.' ===
if 'Estimate No.' in df.columns:
    df['Forecast Stage'] = df['Estimate No.'].astype(str).str.strip().str.title()
elif 'Estimate No' in df.columns:
    df['Forecast Stage'] = df['Estimate No'].astype(str).str.strip().str.title()
else:
    raise ValueError(f"❌ 'Estimate No.' column not found. Found: {df.columns.tolist()}")

# === Clean crop column ===
df['Crop'] = df['Crop'].astype(str).str.strip().str.title()

# === Define orderings ===
forecast_order = [
    "1St Forecast", "2Nd Forecast", "3Rd Forecast", "4Th Forecast",
    "5Th Forecast", "6Th Forecast", "7Th Forecast", "8Th Forecast", "Final Forecast"
]
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

df['Forecast Stage'] = pd.Categorical(df['Forecast Stage'], categories=forecast_order, ordered=True)
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# === Target crops ===
target_crops = ['White Maize', 'Yellow Maize', 'Soybeans']
df = df[df['Crop'].isin(target_crops)]

# === Debug output ===
print("\n🔍 Unique Forecast Stages found:")
print(df['Forecast Stage'].dropna().unique())
print("\n📆 Unique Months found:")
print(df['Month'].dropna().unique())

# === Output directory ===
output_dir = os.path.join(os.path.dirname(file_path), "seasonality_exports")
os.makedirs(output_dir, exist_ok=True)

# === Loop through crops, build pivot table and visualise ===
for crop in target_crops:
    crop_df = df[df['Crop'] == crop]
    pivot = crop_df.pivot_table(index='Forecast Stage', columns='Month', aggfunc='size', fill_value=0)
    pivot = pivot[month_order]  # reorder months

    if pivot.sum().sum() == 0:
        print(f"\n⚠️ No data found for {crop}. Skipping heatmap.")
        continue

    # Export to CSV
    csv_path = os.path.join(output_dir, f"{crop.replace(' ', '_').lower()}_seasonality.csv")
    pivot.to_csv(csv_path)
    print(f"✅ Exported seasonality table for {crop} → {csv_path}")

    # Plot heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt='d', cmap='YlGnBu')
    plt.title(f"Forecast Seasonality Heatmap — {crop}")
    plt.xlabel("Month")
    plt.ylabel("Forecast Stage")
    plt.tight_layout()
    plt.show()
