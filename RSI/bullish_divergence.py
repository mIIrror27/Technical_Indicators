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
start_date = dt.datetime(2021, 1, 15)
end_date = dt.datetime(2025, 8, 22)

data = kite.historical_data(
    instrument_token=token,
    from_date= start_date,
    to_date = end_date,
    interval="day"
)

df = pd.DataFrame(data)

df["rsi"] = talib.RSI(df["close"], timeperiod= 14)

# Calculating local minima
df["SwingP_Low"] = (df["close"] <  df["close"].shift(1)) & (df["close"] < df["close"].shift(-1))
df["SwingR_Low"] = (df["rsi"] <  df["rsi"].shift(1)) & (df["rsi"] < df["rsi"].shift(-1))

# Creating Swing condition dataframe
swing = df[(df["SwingP_Low"]) & (df["SwingR_Low"])].copy()


signal = []
lookback = 30

for i in range(1, len(swing)):
    curr = swing.iloc[i]

    for j in range(max(0, i - lookback), i):
        prev = swing.iloc[j]

        if (curr["close"] < prev["close"]) and (curr["rsi"] > prev["rsi"]):
            signal.append({
                "Date": df.loc[curr.name, "date"].strftime("%Y-%m-%d"),
                "Price": round(float(curr["close"]), 2),
                "RSI": round(float(curr["rsi"]), 2),
                "Compared_To": df.loc[prev.name, "date"].strftime("%Y-%m-%d")
            })
            break

for s in signal:
    print(s)