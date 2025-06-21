import yfinance as yf
import pandas as pd
import schedule
import time

ticker = "AAPL"
lookback = 200  # Max SMA window

def run_strategy():
    df = yf.download(ticker, period="6mo", interval="15m")  # near real-time intraday data
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()

    if df["SMA50"].iloc[-1] > df["SMA200"].iloc[-1]:
        signal = "BUY"
    elif df["SMA50"].iloc[-1] < df["SMA200"].iloc[-1]:
        signal = "SELL"
    else:
        signal = "HOLD"

    print(f"[{df.index[-1]}] Signal: {signal} | Price: {df['Close'].iloc[-1]:.2f}")

# Schedule to run every 15 minutes
schedule.every(15).minutes.do(run_strategy)

print("🚀 Starting Forward Test for AAPL...")
while True:
    schedule.run_pending()
    time.sleep(1)
