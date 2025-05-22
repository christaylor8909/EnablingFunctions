import backtrader as bt
import yfinance as yf
from datetime import datetime

# Step 1: Download stock data
df = yf.download("AAPL", start="2022-01-01", end="2023-01-01", group_by='ticker')
df.dropna(inplace=True)

# ✅ Flatten multi-index columns
df.columns = df.columns.droplevel(0)

print("Type of df:", type(df))
print(df.head())

# Step 2: Load into Backtrader
data = bt.feeds.PandasData(dataname=df)

# Step 3: Strategy
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=10)
        sma2 = bt.ind.SMA(period=30)
        self.signal_add(bt.SIGNAL_LONG, sma1 > sma2)
        self.signal_add(bt.SIGNAL_SHORT, sma1 < sma2)

# Step 4: Backtest
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)
cerebro.run()
cerebro.plot()
