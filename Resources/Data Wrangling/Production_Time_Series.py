import pandas as pd
import matplotlib.pyplot as plt

# Load your cleaned data
file_path = "C:/Users/chris/Downloads/Practice copy.xlsx"  # Update if needed
df = pd.read_excel(file_path)

# Clean up
df.columns = df.columns.str.strip()
df['Year'] = df['Year'].astype(int)
df['Crop'] = df['Crop'].str.strip().str.title()
df['Estimate No.'] = df['Estimate No.'].str.strip()

# Filter only final forecasts and target crops
target_crops = ['White Maize', 'Yellow Maize', 'Soybeans']
final_df = df[(df['Estimate No.'] == 'Final Forecast') & (df['Crop'].isin(target_crops))]

# Pivot table for plotting
pivot_df = final_df.pivot(index='Year', columns='Crop', values='Production (tons)')

# Plot
plt.figure(figsize=(10, 6))
for crop in target_crops:
    if crop in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[crop], label=crop, marker='o')

plt.title('Final Production Over Time (White Maize, Yellow Maize, Soybeans)')
plt.xlabel('Year')
plt.ylabel('Production (tons)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
