
import yfinance as yf
import pandas as pd

# Define FX pairs
fx_pairs = ["AUDUSD=X", "EURUSD=X", "JPY=X", "GBPUSD=X"]

# Download FX data
fx_data = yf.download(fx_pairs, start="2023-01-01", end="2024-12-31", progress=False)

# Flatten multi-index columns for CSV
fx_data.columns = ['_'.join(col).strip() for col in fx_data.columns.values]

# Save to CSV
fx_data.to_csv("FX_Rates.csv")

print("✅ FX data saved to FX_Rates.csv")
