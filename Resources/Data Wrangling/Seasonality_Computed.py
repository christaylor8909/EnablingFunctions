import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
import os

# File picker
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select your CEC cleaned Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)
if not file_path:
    raise FileNotFoundError("No file selected.")

# Load data
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Clean Month
month_map = {
    'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
    'Jun': 'June', 'Jul': 'July', 'Aug': 'August', 'Sep': 'September',
    'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
}
df['Month'] = df['Month'].astype(str).str.strip().str.title().replace(month_map)

# Filter production only
df['Crop'] = df['Crop'].astype(str).str.strip().str.title()
df = df[df['Crop'].isin(['White Maize', 'Yellow Maize', 'Soybeans'])]

month_order = ['February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']
df = df[df['Month'].isin(month_order)]
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Drop missing production rows
df = df.dropna(subset=['Production (tons)'])

# Create median line (for trend)
median_df = (
    df.groupby(['Crop', 'Month'])['Production (tons)']
    .median()
    .reset_index()
    .rename(columns={'Production (tons)': 'Median'})
)

# Merge back for trend line
df = df.merge(median_df, on=['Crop', 'Month'])

# Plot: one row per crop
g = sns.FacetGrid(df, row="Crop", sharey=False, height=4, aspect=2)
g.map_dataframe(sns.boxplot, x='Month', y='Production (tons)', order=month_order, color='skyblue')
g.map_dataframe(sns.lineplot, x='Month', y='Median', color='black', marker='o', linewidth=2)

# Title and layout
g.set_titles(row_template="{row_name}")
g.set_axis_labels("Month", "Total Production (tons)")
for ax in g.axes.flat:
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.show()
