import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Step 1: Select file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select your cleaned CEC Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if file_path:
    # Step 2: Load and clean
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)
    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].str.strip().str.title()
    df['Estimate No.'] = df['Estimate No.'].str.strip()
    df['Crop'] = df['Crop'].str.strip().str.title()
    if 'Yield (t/ha)' in df.columns:
        df['Yield (t/ha)'] = df['Yield (t/ha)'].round(2)

    # Step 3: Filter for Final Forecasts only
    final_df = df[df['Estimate No.'] == 'Final Forecast']

    # Step 4: Pivot the table to Year x Crop
    pivot = final_df.pivot(index='Year', columns='Crop', values='Yield (t/ha)')

    # Step 5: Plot
    plt.figure(figsize=(10, 6))
    for crop in ['White Maize', 'Yellow Maize', 'Soybeans']:
        if crop in pivot.columns:
            plt.plot(pivot.index, pivot[crop], marker='o', label=crop)

    plt.title("📈 Final Yield Over Time (White Maize, Yellow Maize, Soybeans)")
    plt.xlabel("Year")
    plt.ylabel("Yield (t/ha)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("No file selected.")
