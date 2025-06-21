import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog

# Step 1: Select Excel file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select your forecast accuracy Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)
if not file_path:
    raise FileNotFoundError("No file selected.")

# Step 2: Load data
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Step 3: Ensure expected column names
if 'Forecast Stage' in df.columns:
    df.rename(columns={'Forecast Stage': 'Estimate No.'}, inplace=True)

# Check required columns
required_cols = ['Crop', 'Year', 'Estimate No.', '% Error from Final']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise KeyError(f"Missing required columns: {missing}")

# Step 4: Clean and sort forecast stages
forecast_order = ['1st Forecast', '2nd Forecast', '3rd Forecast', '4th Forecast',
                  '5th Forecast', '6th Forecast', '7th Forecast', '8th Forecast']
df = df[df['Estimate No.'].isin(forecast_order)]
df['Estimate No.'] = pd.Categorical(df['Estimate No.'], categories=forecast_order, ordered=True)

# Step 5: Plot per crop
for crop in sorted(df['Crop'].unique()):
    crop_df = df[df['Crop'] == crop]
    n_years = crop_df['Year'].nunique()

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=crop_df,
        x='Estimate No.',
        y='% Error from Final',
        hue='Year',
        marker='o',
        palette=sns.color_palette("Set1", n_colors=n_years)
    )

    plt.axhline(0, linestyle='--', color='gray', linewidth=1)
    plt.title(f"Forecast Accuracy by Stage ({crop})")
    plt.ylabel("% Error from Final")
    plt.xlabel("Forecast Stage")
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
