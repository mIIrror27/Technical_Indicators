from kiteconnect import KiteConnect
import pandas as pd
import numpy as np
import datetime as dt
import talib

api_key = ""
access_token = ""
with open("access_token.txt") as f:
    access_token = f.read().strip()
    
kite = KiteConnect(api_key = api_key)
kite.set_access_token(access_token)
exchange = "NSE"

token = 1703937
start_date = dt.datetime(2025, 1, 15)
end_date = dt.datetime(2025, 8, 22)

data = kite.historical_data(
    instrument_token=token,
    from_date= start_date,
    to_date = end_date,
    interval="day"
)

df = pd.DataFrame(data)

df["rsi"] = talib.RSI(df["close"], timeperiod= 14)

lookback1 = 5
df["SwingP_High"] = df["close"] == df["close"].rolling(lookback1).max()
df["SwingR_High"] = df["rsi"] == df["rsi"].rolling(lookback1).max()

# Creating Swing condition dataframe
swing = df[(df["SwingP_High"]) & (df["SwingR_High"])].copy()


signal = []
lookback2 = 30
for i in range(1, len(swing)):
    curr = swing.iloc[i]

    # Look at last 'lookback' swing highs before curr
    for j in range(max(0, i - lookback2), i):
        prev = swing.iloc[j]

        if (curr["close"] > prev["close"]) and (curr["rsi"] < prev["rsi"]):
            signal.append({
                "Date": df.loc[curr.name, "date"].strftime("%Y-%m-%d"),
                "Price": round(float(curr["close"]), 2),
                "RSI": round(float(curr["rsi"]), 2),
                "Compared_To": df.loc[prev.name, "date"].strftime("%Y-%m-%d")
            })
            break

for i in signal:

    print(i)

