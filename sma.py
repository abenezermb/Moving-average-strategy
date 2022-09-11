import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import numpy as np


class SMA:
    STOCK = 'TSLA'
    def get_stock_price(self):
        start = datetime.datetime(2021, 2, 1) 
        end = datetime.datetime(2022, 2, 1) # extract the closing price data
        price_df = web.DataReader([self.STOCK], 'yahoo', start = start, end = end)['Close']
        price_df.columns = {'Close Price'}
        return price_df
    
    def visualize_price_df(self,df):
        # visualize the data
        df['Close Price'].plot(figsize = (15, 8))
        plt.grid()
        plt.ylabel("Price in Dollars")
        plt.show()    
    
    def get_short_simple_moving_average(self,df):
        return df['Close Price'].rolling(window = 20, min_periods = 1).mean()
    
    def get_long_simple_moving_average(self,df):
        return df['Close Price'].rolling(window = 50, min_periods = 1).mean()
    
    def generate_crossover_signals(self,df):
        # sets one when short is above long and zero when short is below zero
        df['Signal'] = 0.0
        df['Signal'] = np.where(df['20_SMA'] > df['50_SMA'], 1.0, 0.0)
        return df
    
    def calculate_crossover_direction(self,df):
        df['Position'] = df['Signal'].diff()
        return df
    
    def visualize_crossover(self,df):
        # Now let's visualize this using a plot to make it more clear
        plt.figure(figsize = (20,10))
        # plot close price, short-term and long-term moving averages 
        df['Close Price'].plot(color = 'k', label= 'Close Price') 
        df['20_SMA'].plot(color = 'b',label = '20-day SMA')
        df['50_SMA'].plot(color = 'g', label = '50-day SMA')

        # plot ‘buy’ signals
        plt.plot(df[df['Position'] == 1].index, 
                df['20_SMA'][df['Position'] == 1], 
                '^', markersize = 15, color = 'g', label = 'buy')# plot ‘sell’ signals
        plt.plot(df[df['Position'] == -1].index, 
                df['20_SMA'][df['Position'] == -1], 
                'v', markersize = 15, color = 'r', label = 'sell')
        plt.ylabel('Price in Dollar', fontsize = 15 )
        plt.xlabel('Date', fontsize = 15 )
        plt.title('TESLA', fontsize = 20)
        plt.legend()
        plt.grid()
        plt.show()
        
    def start(self):
        df = self.get_stock_price()
        df['20_SMA'] = self.get_short_simple_moving_average(df)
        df['50_SMA'] = self.get_long_simple_moving_average(df)
         
        df = self.generate_crossover_signals(df)
        df = self.calculate_crossover_direction(df)
        self.visualize_crossover(df)

# Now that we have 20 days and 50 days SMAs, next we see how to strategize
# this information to generate trade signals

# Simple moving average crossover strategy and exponential moving average
# crossover strategy
"""
A moving average crossover occurs when plotting, the two moving averages
each based on different time periods tend to cross. The indicator uses
two(or more) moving average. We could have a short time period(faster moving)
and long timer period(slow moving) SMA.
Short timer period = 5,10,20 days
Long time period = 50, 100, 200 day
"""

# Generating trade signals from crossovers
"""
1. When the short term moving average crosses above the long term moving
average, this indicates a BUY SIGNAL.
2. When the short term moving average crosses below the long term moving
average, this indicates a SELL SIGNAL.
"""

# From the 'signal' values, the position orders can be generated to 
# represent trading signals. Crossover happens when the faster moving
# and slow moving average cross, in other words the 'signal' changes from
# 0 to 1(or 1 to 0). So, to incorporate this information, create a new column
# 'Position' which nothing but a day-to-day difference of the 'signal' column.


"""
1. when position = 1, it implies that signal has changed from 0 to 1
meaning a short-term(faster) moving average has crossed above the long-term
(slower) moving average, thereby triggering a buy call.
2. When position = -1, it implies that the signal has changed from 1 to 0
meaning a short-term(faster) moving average has crossed below the long-term
(slower) moving average, thereby triggering a sell call.
"""



