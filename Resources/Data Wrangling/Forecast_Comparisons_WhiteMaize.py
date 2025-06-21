import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Step 1: GUI file selector
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select your cleaned CEC Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if file_path:
    # Step 2: Load + clean
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)

    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].str.strip().str.title()
    df['Estimate No.'] = df['Estimate No.'].str.strip()
    df['Crop'] = df['Crop'].str.strip().str.title()
    df['Production (tons)'] = pd.to_numeric(df['Production (tons)'], errors='coerce')

    # Step 3: Filter out Prelim and define ordered categories
    estimate_order = ["1st Forecast", "2nd Forecast", "3rd Forecast",
                      "4th Forecast", "5th Forecast", "6th Forecast",
                      "7th Forecast", "8th Forecast", "Final Forecast"]
    df = df[df["Estimate No."].isin(estimate_order)]
    df['Estimate No.'] = pd.Categorical(df['Estimate No.'], categories=estimate_order, ordered=True)

    # Step 4: Filter White Maize
    crop_to_plot = "White Maize"
    crop_df = df[df['Crop'] == crop_to_plot]

    # Step 5: Pivot table: Forecast Stage × Year
    pivot = crop_df.pivot(index="Estimate No.", columns="Year", values="Production (tons)")
    pivot = pivot.dropna(how='all')
    pivot.index = pivot.index.astype(str)

    # Step 6: Plot
    plt.figure(figsize=(12, 6))
    for year in pivot.columns:
        if pivot[year].notna().sum() > 1:
            plt.plot(pivot.index, pivot[year], marker='o', label=str(year))

    plt.title(f"{crop_to_plot} — Forecast Convergence (1st → Final Forecast)")
    plt.xlabel("Forecast Stage")
    plt.ylabel("Production (tons)")
    plt.xticks(rotation=45)
    plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print("❌ No file selected.")
