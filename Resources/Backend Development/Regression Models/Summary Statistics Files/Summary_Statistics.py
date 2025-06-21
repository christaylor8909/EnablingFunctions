import pandas as pd

# Load data
file_path = "InterviewSummaryData.xlsx"
df = pd.read_excel(file_path, sheet_name=0, skiprows=3)

# Clean column names
df.columns = df.columns.str.strip()

# Convert all columns with numeric data to numeric type (ignore errors)
df_numeric = df.apply(pd.to_numeric, errors='coerce')

# Calculate summary statistics
summary_stats = pd.DataFrame({
    "Mean": df_numeric.mean(),
    "Median": df_numeric.median(),
    "Std Dev": df_numeric.std(),
    "Min": df_numeric.min(),
    "Max": df_numeric.max(),
    "Count (Non-missing)": df_numeric.count()
})

# Remove rows where everything is NaN (i.e. non-numeric columns)
summary_stats = summary_stats.dropna(how='all')

# Save to new Excel file
output_path = "InterviewSummaryData_Summary.xlsx"
summary_stats.to_excel(output_path)

print(f"✅ Summary statistics saved to {output_path}")
