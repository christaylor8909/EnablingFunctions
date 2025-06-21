import pandas as pd
import tkinter as tk
from tkinter import filedialog

# GUI to select Excel file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select your cleaned CEC Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if file_path:
    # Load & clean
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    df.dropna(how='all', inplace=True)

    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].str.strip().str.title()
    df['Estimate No.'] = df['Estimate No.'].str.strip()
    df['Crop'] = df['Crop'].str.strip().str.title()
    df['Production (tons)'] = pd.to_numeric(df['Production (tons)'], errors='coerce')

    # Only keep needed forecast stages
    forecast_stages = ["1st Forecast", "2nd Forecast", "3rd Forecast",
                       "4th Forecast", "5th Forecast", "6th Forecast",
                       "7th Forecast", "8th Forecast", "Final Forecast"]

    df = df[df["Estimate No."].isin(forecast_stages)]
    df['Estimate No.'] = pd.Categorical(df['Estimate No.'], categories=forecast_stages, ordered=True)

    # Create comparison table
    result_rows = []

    for crop in df['Crop'].unique():
        for year in sorted(df['Year'].unique()):
            crop_year_df = df[(df['Crop'] == crop) & (df['Year'] == year)]
            final_row = crop_year_df[crop_year_df['Estimate No.'] == 'Final Forecast']
            if final_row.empty:
                continue
            final_value = final_row['Production (tons)'].values[0]

            for stage in forecast_stages[:-1]:  # skip Final itself
                row = crop_year_df[crop_year_df['Estimate No.'] == stage]
                if not row.empty and pd.notna(row['Production (tons)'].values[0]):
                    est = row['Production (tons)'].values[0]
                    error = 100 * (est - final_value) / final_value
                    result_rows.append({
                        "Crop": crop,
                        "Year": year,
                        "Forecast Stage": stage,
                        "Forecast (tons)": est,
                        "Final (tons)": final_value,
                        "% Error from Final": round(error, 2)
                    })

    # Final DataFrame
    accuracy_df = pd.DataFrame(result_rows)
    pd.set_option('display.max_rows', 100)
    print("\nForecast Accuracy Table:\n")
    print(accuracy_df)

    # Optionally save to CSV
    accuracy_df.to_csv("forecast_accuracy_by_crop.csv", index=False)
    print("\nSaved to 'forecast_accuracy_by_crop.csv'.")

else:
    print("No file selected.")

