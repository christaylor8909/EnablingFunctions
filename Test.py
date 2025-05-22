import yfinance as yf

# Download stock data
data = yf.download("AAPL", start="2022-01-01", end="2024-12-31")

# Create strategy and backtester objects
strategy = MovingAverageStrategy()
tester = Backtester(strategy, data)

# Run the backtest
tester.run()


class Strategy:
    def generate_signals(self, data):
        raise NotImplementedError

class MovingAverageStrategy(Strategy):
    def generate_signals(self, data):
        data["SMA50"] = data["Close"].rolling(50).mean()
        data["SMA200"] = data["Close"].rolling(200).mean()
        data["Signal"] = 0
        data.loc[data["SMA50"] > data["SMA200"], "Signal"] = 1
        data.loc[data["SMA50"] < data["SMA200"], "Signal"] = -1
        return data

class Backtester:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def run(self):
        df = self.strategy.generate_signals(self.data)
        df["Strategy Return"] = df["Signal"].shift(1) * df["Close"].pct_change()
        total_return = (df["Strategy Return"] + 1).prod() - 1
        print(f"Total return: {total_return:.2%}")
