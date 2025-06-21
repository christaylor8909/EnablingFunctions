import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ✅ Corrected file path
file_path = "C:/Users/chris/Desktop/GitHub/EnablingFunctions/forecast_accuracy_all_crops.xlsx"
df = pd.read_excel(file_path)

# Filter for White Maize only
df = df[df['Crop'] == 'White Maize']

# Ensure correct forecast stage order
forecast_order = ["1st Forecast", "2nd Forecast", "3rd Forecast",
                  "4th Forecast", "5th Forecast", "6th Forecast",
                  "7th Forecast", "8th Forecast"]
df['Forecast Stage'] = pd.Categorical(df['Forecast Stage'], categories=forecast_order, ordered=True)

# Plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='Forecast Stage', y='% Error from Final', hue='Year', marker='o')
plt.title('Forecast Accuracy by Stage (White Maize)')
plt.ylabel('% Error from Final')
plt.xlabel('Forecast Stage')
plt.axhline(0, color='gray', linestyle='--')
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/visuals/forecast_accuracy_over_time.png")
plt.close()

print("✅ Forecast accuracy visual saved to: outputs/visuals/forecast_accuracy_over_time.png")
