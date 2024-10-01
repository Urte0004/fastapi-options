import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import exp

#equity parameters
num_steps = 252
T = 1 #years
volatility = .1
rfr = .05
S_0 = 100
K = 100

#tree parameters


def generate_S_tree(S_0, up, down, num_steps):
    tree = [[S_0]]
    for i in range(1,num_steps):
        layer = []
        for j in range(i):
            layer.append(tree[i-1][j]*up)
            if j == i-1:
                layer.append(tree[i-1][j]*down)
        tree.append(layer)
    return tree

def generate_V_trees(S_0, K, volatility, rfr, num_steps, T):
    dt = T/num_steps
    up = exp(volatility*(dt**.5))
    down = 1/up
    prob_up = (exp(rfr*dt)-down)/(up-down)
    S_tree = generate_S_tree(S_0, up, down, num_steps)
    ending_V_payoff = [max(0,i-K) for i in S_tree[-1]]
    E_V_tree = [ending_V_payoff]
    A_V_tree = [ending_V_payoff]
    #constructed last layer^

    for i in range(1,num_steps):
        new_E_V_layer = []
        new_A_V_layer = []
        S_layer = S_tree[num_steps-i-1]
        E_V_layer = E_V_tree[i-1]   #should be last layer
        A_V_layer = A_V_tree[i-1]
        for j in range(1,num_steps-i+1):
            payoff_A = (A_V_layer[j-1]*prob_up+A_V_layer[j]*(1-prob_up))/exp(rfr*dt)
            payoff_E = (E_V_layer[j-1]*prob_up+E_V_layer[j]*(1-prob_up))/exp(rfr*dt)
            #if i == 240:
                #print(S_layer[j-1]-K,payoff_A, payoff_E)
            exercise_value = S_layer[j-1]-K
            new_A_V_layer.append(max(payoff_A, exercise_value))
            new_E_V_layer.append(payoff_E)
            
        A_V_tree.append(new_A_V_layer)
        E_V_tree.append(new_E_V_layer)
    #reverse both
    A_V_tree, E_V_tree = A_V_tree[::-1], E_V_tree[::-1]
    return A_V_tree, E_V_tree, S_tree
        

#delta
#small change in initial S, corresponding change in V at t=0? decrease num_steps by 1 maybe?
def gen_delta(bottom_of_range, K, volatility, rfr, num_steps, T, increment, top_of_range): #S_0 is bottom of range.
    deltas = []
    for i in range(int((top_of_range-bottom_of_range)/increment)):
        print(bottom_of_range+(i*increment))
        American_tree, _, S_tree = generate_V_trees(bottom_of_range+(i*increment), K, volatility, rfr, num_steps, T)
        
        deltas.append((American_tree[1][0]-American_tree[1][1])/(S_tree[1][0]-S_tree[1][1]))
    return deltas
deltas = gen_delta(80,100,volatility,rfr,num_steps,T,.05,120)
print(deltas)
plt.plot(deltas)
plt.show()