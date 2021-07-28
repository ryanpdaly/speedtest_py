# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 19:11:15 2020

@author: ryand
"""

import pandas as pd
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt

def read_csv():
    filename = 'C:\Python\Speedtest\speedtest_data.csv'
    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date'])
    df.rename(columns={'Ping (ms)':'Ping',
                       'Download (Mbps)':'Download',
                       'Upload (Mbps)':'Upload'}, inplace=True)
    return df

def calc_avg(df, days=30000):
    '''Rather hackish solution to defaulting to an alltime average.
        A better solution may be to use optional arguments and logic to
        eliminate our start_date criteria if days is null
    '''
    start_date = dt.datetime.now() - dt.timedelta(days)
    df = df[(df['Date'] >= start_date)]
    result = df.mean(axis=0)
    return result
    
def calc_weekday(df_orig):
    df = df_orig.copy(deep=True)
    df['Weekday']=df['Date'].dt.weekday
    df = df.groupby('Weekday').mean()
    
    #df.plot(kind='bar', x=df.index, y='Ping')
    return df

def calc_time(df_orig):
    df = df_orig.copy(deep=True)
    df['Date'] = df['Date'].apply(lambda x: dt.datetime(x.year, x.month, x.day, x.hour,
                                            30*round((float(x.minute) + float(x.second)/60)/30)))
    
    df['Time'] = df['Date'].dt.time
    df = df.drop(columns=['Date'])
    df = df.groupby('Time').mean()
    return df

def plot_all(df):
    ax = plt.gca()
    
    df.plot(kind='line', x='Date', y='Download', color='red', ax=ax)
    df.plot(kind='line', x='Date', y='Upload', color='blue', ax=ax)
    
    plt.show()

data = read_csv()

avg_alltime = calc_avg(data)
avg_30day = calc_avg(data, 30)
avg_7day = calc_avg(data, 7)
avg_1day = calc_avg(data, 1)
avg_weekday = calc_weekday(data)
avg_time = calc_time(data)

plot_all(data)