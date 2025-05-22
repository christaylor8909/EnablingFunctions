import yfinance as yf
import pandas as pd

symbols = ["AAPL", "MSFT", "AUDUSD=X", "EURUSD=X"]
data = {}

for symbol in symbols:
    df = yf.download(symbol, period="1y", interval="1d")
    df["Symbol"] = symbol
    data[symbol] = df

merged_df = pd.concat(data.values())
merged_df.to_csv("Market_Data_Historical.csv")
print("✅ Market data saved.")
