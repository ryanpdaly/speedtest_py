# -*- coding: utf-8 -*-
"""
Created on Sat May 23 22:08:03 2020

@author: ryand
"""

import speedtest as st
import pandas as pd
import datetime

def run_test():
    #Run our internet speeds test
    s = st.Speedtest()
    s.get_best_server()
    
    #Convert results to Mbps, ms, round to 2 decimals
    down = round(s.download()/1e6, 2)
    up = round(s.upload()/1e6, 2)
    ping = round(s.results.ping, 0)
    
    results= 'Ping: {} ms \nDownload: {} Mbps \nUpload: {} Mbps'
    #print(results.format(ping, down, up))
    return(ping, down, up)

def update_csv(results):
    now = datetime.datetime.now()
    
    filename = r"C:\Python\Speedtest\speedtest_data.csv"
    
    #Attempt to load CSV to update
    try:
        csv_data = pd.read_csv(filename, index_col='Date')
    except:
        csv_data = pd.DataFrame(
            list(),
            columns=['Ping (ms)', 'Download (Mbps)', 'Upload (Mbps)'])
        
    #Create a one-row Dataframe for the new test results
    df_results = pd.DataFrame(
        [[results[0], results[1], results[2]]],
        columns=['Ping (ms)', 'Download (Mbps)', 'Upload (Mbps)'],
        index=[now])
    
    #Append the DataFrame with results to our data from CSV file
    df_updated = csv_data.append(df_results, sort=False)
    df_updated.to_csv(filename, index_label='Date')
    
    #print('Check the CSV')
        
test_results = run_test()
update_csv(test_results)
