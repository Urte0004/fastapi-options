import yfinance as yf
from get_garch_vol import get_garch_vol
import pandas as pd
import numpy as np
import datetime as dt
import os
import pytz

def get_inputs(ticker:str, interval:float, exp_date:dt.datetime):
    if "1m" == interval:

        df = yf.download(ticker, interval=interval, period="5d")
    elif interval == "5m":
        df = yf.download(ticker, interval=interval, period="5d")
    elif interval == "30m":
        df = yf.download(ticker, interval=interval, period="50d")
    elif interval == "4h":
        df = yf.download(ticker, interval=interval, period="50d")
    else:
        df = yf.download(ticker, interval=interval)
    S = df["Close"].to_numpy()[-1]
    last_dt = df.index[-1]
    exp_date = exp_date.astimezone(tz=pytz.timezone("UTC"))
    last_dt = last_dt.tz_localize("EST").astimezone(tz=pytz.timezone("UTC"))

    second_delta = (exp_date - last_dt).total_seconds()
    anual_tte = second_delta/(60*60*24*365)
    rfr = 4.51
    if interval == ("1m" or "5m" or "30m"):

        vol = get_garch_vol(df, True)
    else:
        vol = get_garch_vol(df, False)
    return S, anual_tte,vol, rfr