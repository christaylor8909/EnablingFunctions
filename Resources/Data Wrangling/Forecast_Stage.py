import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === Load your forecast accuracy file ===
file_path = "C:/Users/chris/Desktop/GitHub/EnablingFunctions/forecast_accuracy_all_crops.xlsx"
df = pd.read_excel(file_path)

# === Clean and prepare ===
df.columns = df.columns.str.strip()
df['Forecast Stage'] = df['Forecast Stage'].str.strip()
df['Crop'] = df['Crop'].str.title()

# === PART 1: Seasonality Summary ===
print("\n📊 Frequency of each forecast stage by crop:\n")
seasonality_summary = df.groupby(['Crop', 'Forecast Stage']).size().unstack(fill_value=0)
print(seasonality_summary)

# === PART 2: Forecast Error Stability (1st–3rd Forecasts) ===
early_stages = ["1st Forecast", "2nd Forecast", "3rd Forecast"]
early_df = df[df['Forecast Stage'].isin(early_stages)]

# Average absolute error by crop and year
print("\n📈 Average absolute % error (1st–3rd forecasts) vs final:\n")
yearly_error = early_df.groupby(['Crop', 'Year'])['% Error from Final'].apply(lambda x: round(x.abs().mean(), 2)).reset_index()
yearly_error.columns = ['Crop', 'Year', 'Avg Abs Error (1st–3rd)']

# Flag stability
yearly_error['Stability'] = yearly_error['Avg Abs Error (1st–3rd)'].apply(lambda x: 'Stable' if x < 3 else 'Volatile')
print(yearly_error.to_string(index=False))

# Optional: Visualise in a plot window
plt.figure(figsize=(10, 6))
sns.barplot(data=yearly_error, x='Year', y='Avg Abs Error (1st–3rd)', hue='Crop')
plt.axhline(3, color='red', linestyle='--', label='Volatility Threshold (3%)')
plt.title("Early Forecast Error by Year (1st–3rd vs Final)")
plt.ylabel("Avg % Error (Abs)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
