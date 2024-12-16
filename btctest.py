import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams

rcParams['figure.autolayout'] = True

fig = plt.figure(figsize=(12, 7))
ax = [fig.add_subplot(2, 3, i+1, projection='3d') for i in range(6)]

def calculate_rsi(close):
    H = close[1:] - close[:-1]
    up = sum([i for i in H if i >= 0])
    dn = sum([abs(i) for i in H if i < 0])
    return 100 - 100/(1 + up/dn)

def TradingStrategy(close, entry_rsi, exit_rsi, window=30, fee=0.004):
    N = len(close)
    profit = 0
    entry = 0
    side = 0

    for i in range(window, N):

        if side == 1:
            H = close[i-window:i]
            rsi = calculate_rsi(H)
            delta = (close[i] - entry)/entry
            if rsi > exit_rsi:
                profit += (delta - fee)
                side = 0
            

        if side == 0:
            H = close[i-window:i]
            rsi = calculate_rsi(H)
            if rsi < entry_rsi:
                entry = close[i]
                side = 1

    return profit
    

files = ['BTC60','BTC300','BTC900','BTC3600','BTC21600','BTC86400']
intervals = ['1Min','5Min','15Min','1Hr','6Hr','1Day']

rsi_entry = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
rsi_exit = [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]

x, y = np.meshgrid(rsi_entry, rsi_exit)

data = {file:pd.read_csv(f'{file}.csv')[::-1]['Close'].values for file in files}

for index, file in enumerate(files):
    z = []
    for entry_rsi in rsi_entry:
        tz = []
        for exit_rsi in rsi_exit:
            profit = TradingStrategy(data[file], entry_rsi, exit_rsi)
            tz.append(profit)
        z.append(tz)
    z = np.array(z)
    ax[index].set_title("Time Interval: " + intervals[index])
    ax[index].plot_surface(x, y, z, color='red' if np.mean(z) < 0 else 'limegreen', edgecolor='black', linewidth=0.8)
    ax[index].set_xlabel("Entry RSI")
    ax[index].set_ylabel("Exit RSI")

plt.show()





            
