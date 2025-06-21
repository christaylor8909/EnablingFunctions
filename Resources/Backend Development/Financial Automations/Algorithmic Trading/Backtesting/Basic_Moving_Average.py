#Buy Signal: When SMA50 crosses above SMA200 → interpreted as a bullish trend starting.
#Sell Signal: When SMA50 crosses below SMA200 → interpreted as bearish, so you exit or short.

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

ticker = "AAPL"
df = yf.download(ticker, start="2022-01-01", end="2024-12-31", auto_adjust=False)

# OPTIONAL: Flatten multi-index columns (if needed)
if isinstance(df.columns[0], tuple):
    df.columns = [col[0] for col in df.columns]

# Calculate moving averages
df["SMA50"] = df["Close"].rolling(window=50).mean()
df["SMA200"] = df["Close"].rolling(window=200).mean()

# Generate signal
df["Signal"] = 0
df.loc[df["SMA50"] > df["SMA200"], "Signal"] = 1
df.loc[df["SMA50"] < df["SMA200"], "Signal"] = -1

# Strategy return
df["Strategy Return"] = df["Signal"].shift(1) * df["Close"].pct_change()

# Plot
df[["Close", "SMA50", "SMA200"]].plot(figsize=(12, 6), title="Moving Average Crossover Strategy")
plt.grid(True)
plt.show()

# Print total return
print(f"✅ Total Strategy Return: {(df['Strategy Return'] + 1).prod() - 1:.2%}")
