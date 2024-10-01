import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
def price_option(S, K, vol, rfr, time_to_exp):
    d_1 = (np.log(S/K) + (rfr+.5*(vol**2))*time_to_exp)/(vol*(time_to_exp**.5))
    d_2 = d_1 - vol*(time_to_exp**.5)
    Value = S*norm(d_1)-K*np.exp(-rfr*time_to_exp)*norm(d_2)

