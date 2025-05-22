import yfinance as yf
import pandas as pd

# Define bond yield tickers
bonds = ["^IRX", "^FVX", "^TNX", "^TYX"]  # 13wk, 5yr, 10yr, 30yr

# Download bond yield data
bond_data = yf.download(bonds, start="2023-01-01", end="2024-12-31", progress=False)

# Flatten multi-index columns for CSV
bond_data.columns = ['_'.join(col).strip() for col in bond_data.columns.values]

# Save to CSV
bond_data.to_csv("US_Treasury_Yields.csv")

print("✅ Bond data saved to US_Treasury_Yields.csv")
