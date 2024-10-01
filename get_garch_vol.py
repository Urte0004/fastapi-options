from arch import arch_model as am
import datetime as dt
def get_garch_vol(df, tenx):
    if tenx:
        df["Close"] = df["Close"]*10
    
    rolling_window_length = 4
    df["returns"] = df["Close"].pct_change().dropna()
    series = 1000*df["returns"].to_numpy()[-rolling_window_length:]
    model = am(series, mean="ARX",vol="Garch", p=rolling_window_length,q=rolling_window_length)
    fitted = model.fit()
    fore = fitted.forecast(align="origin")
    variance_df = fore.variance
    vol_val = variance_df.iloc[0,0]
    vol = (vol_val/100)**.5
    return vol



    


