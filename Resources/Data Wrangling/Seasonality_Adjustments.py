import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned CEC Excel file
file_path = "C:/Users/chris/Downloads/Practice copy.xlsx"
df = pd.read_excel(file_path)

# Standardise and clean key fields
df.columns = df.columns.str.strip()
df['Year'] = df['Year'].astype(int)
df['Month'] = df['Month'].str.strip().str.title()
df['Crop'] = df['Crop'].str.strip().str.title()

# Focus on target crops
target_crops = ['White Maize', 'Yellow Maize', 'Soybeans']
df = df[df['Crop'].isin(target_crops)]

# Create output directory
output_dir = "outputs/visuals"
os.makedirs(output_dir, exist_ok=True)

# Plot long-term trends for each crop and metric
metrics = ['Area (ha)', 'Production (tons)', 'Yield (t/ha)']
for crop in target_crops:
    crop_df = df[df['Crop'] == crop]
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=crop_df, x='Year', y=metric, marker='o')
        plt.title(f'{crop} - {metric} Over Time')
        plt.ylabel(metric)
        plt.xlabel('Year')
        plt.grid(True)
        file_name = f"{crop.replace(' ', '_').lower()}_{metric.split()[0].lower()}_trend.png"
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, file_name))
        plt.close()

# Plot seasonality of forecast estimates by month (if present)
if 'Estimate No.' in df.columns:
    df['Estimate No.'] = df['Estimate No.'].str.strip()
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Month', hue='Estimate No.')
    plt.title("Forecast Frequency by Month")
    plt.xticks(rotation=45)
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "forecast_stage_seasonality.png"))
    plt.close()

print(f"✅ Visuals saved to: {output_dir}")
