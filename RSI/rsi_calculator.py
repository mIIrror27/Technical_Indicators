from kiteconnect import KiteConnect
import pandas as pd
import numpy as np
import datetime as dt

api_key = ""
access_token = ""
with open("access_token.txt") as f:
    access_token = f.read().strip()
    
kite = KiteConnect(api_key = api_key)
kite.set_access_token(access_token)
exchange = "NSE"

token = 1703937
start_date = dt.datetime(2025, 6, 11)
end_date = dt.datetime(2025, 8, 14)

data = kite.historical_data(
    instrument_token=token,
    from_date= start_date,
    to_date = end_date,
    interval="day"
)

df = pd.DataFrame(data)

# Step 1: Calculate daily changes
df["diff"] = df["close"].diff()

# Step 2: Gains and losses
df["gain"] = np.where(df["diff"] > 0, df["diff"], 0)
df["loss"] = np.where(df["diff"] < 0, -df["diff"], 0)

# Step 3: Initialize period
period = 14

#Simple average mean
df.loc[period, "avg_gain"] = df["gain"].iloc[1:period+1].mean()
df.loc[period, "avg_loss"] = df["loss"].iloc[1:period+1].mean()

for i in range(period+1,len(df)):
    df.loc[i, "avg_gain"]  = (df.loc[i-1, "avg_loss"] * (period-1) + df.loc[i, "gain"])/period
    df.loc[i, "avg_loss"]  = (df.loc[i-1, "avg_loss"] * (period-1) + df.loc[i, "loss"])/period
    

# Step 5: RS and RSI
df["rs_0"] = df["avg_gain"] / df["avg_loss"]
df["rsi_0"] = 100 - (100 / (1 + df["rs_0"]))

print(df[["date", "close", "rsi_0"]].tail(8))