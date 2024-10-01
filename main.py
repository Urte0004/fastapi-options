from typing import Union
import numpy as np
from scipy.stats import norm
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from blackscholes_inputs import get_inputs
import datetime as dt
import yfinance as yf
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_block": item.block, "item_id": item_id}


#helper
#needs garch estimate
def price_option(S, K, vol, D, rfr,time_to_exp):
    d_1 = (np.log(S/K) + (rfr-D+.5*(vol**2))*time_to_exp)/(vol*(time_to_exp**.5))
    d_2 = d_1 - vol*(time_to_exp**.5)
    Value = S*np.exp(-D*time_to_exp)*norm.cdf(d_1)-K*np.exp(-rfr*time_to_exp)*norm.cdf(d_2)
    return Value, d_1, d_2

@app.get("/ticker/")
def ticker_comprehensive(ticker: str = "SPY", interval: str = "1m") -> list:
    df = yf.download(f"{ticker}", interval=f"{interval}", period="max")
    if len(df) == 0:
        return "either ticker or interval not valid"
    return [df["Close"].to_dict(), df.index[-1]]

@app.get("/options/")
def option_comprehensive(ticker:str="SPY", D:float=1, interval:str="1d",K:float=500,exp_date:dt.datetime=(dt.datetime.now()+dt.timedelta(7))):
    #get bs inputs
    S, time_to_exp, vol, rfr = get_inputs(ticker, interval,exp_date)
    response = get_greeks(S,K,vol,D,rfr,time_to_exp)
    return response



def get_greeks(S: float, K: float, vol: float, D: float, rfr: float, time_to_exp: float):
    val, d_1, d_2 = price_option(S,K,vol,D,rfr,time_to_exp)
    delta = np.exp(-D*time_to_exp)*norm.cdf(d_1)
    gamma = np.exp(-D*time_to_exp)*norm.pdf(d_1)/(vol*S*time_to_exp**.5)
    #theta formula less pretty, will adjust ttexp by small nudge, .0001

    theta = (price_option(S,K,vol,D,rfr,time_to_exp-.00001)[0]-val)/.01
    vega = S*(time_to_exp**.5)*np.exp(-D*time_to_exp)*norm.pdf(d_1)
    rho = K*time_to_exp*np.exp(-rfr*time_to_exp)*norm.pdf(d_2)
    print(delta, gamma, theta, vega, rho)
    return val, pd.DataFrame({"delta":delta, "gamma":gamma, "theta":theta, "vega":vega, "rho":rho}, index=[1])