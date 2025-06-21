import yfinance as yf
import pandas as pd

commodities = [
    "GC=F",  # Gold
    "CL=F",  # Crude Oil
    "SI=F",  # Silver
    "HG=F"   # Copper
]

commodity_data = yf.download(commodities, start="2023-01-01", end="2024-12-31", progress=False)
commodity_data.columns = ['_'.join(col).strip() for col in commodity_data.columns.values]
commodity_data.to_csv("Commodities_Data.csv")

print("✅ Commodities data saved to Commodities_Data.csv")

#To run the code use the following powershell inputs
#cd "C:\Users\t0355lp\Documents\GitHub\EnablingFunctions\Financial Automations\Market Data Pull"
#python "Commodities Data Pull.py"
