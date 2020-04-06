#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kyle Strokes
SL: Aleah Crawford
11/12/19
ISTA 131 Hw7


This program reads in a csv file that contains the extent of sea ice.
There were some missing dates in the data, clean_data() replaces dates
with no data with the average of the date before and after. If multiple days
are missing then the average of the date a year before and after is assigned.
After the data is cleaned. A new dataframe is made indexed by year and each
column is in the format 'MMDD'. This data from the cleaned series is moved to
the dataframe. A series that includes ice extent from the year 2019 is extracted
from the original series. The last two items are then written into csv files
and placed in the same directory. File names are 'data_79_18.csv' and 
'data_2019.csv'
"""

import pandas as pd
from datetime import datetime
import numpy as np


'''
This function takes the data from a csv file about sea ice extent
It uses the year, month, day, and sea ice measure columns
The date from year, month, day is parsed into a datetime object
Some dates are missing and filled in with pandas daterange method.
It returns a series indexed by a complete datetime objects and 
values are the sea ice extent
'''
def get_data():
    file_str = "N_seaice_extent_daily_v3.0.csv"
    df = pd.read_csv(file_str, skiprows=1, usecols=[0,1,2,3],
                     parse_dates={'Date':[0,1,2]})
    v = df.iloc[:,1]
    v.index = df.iloc[:,0].values  
    full = pd.date_range(start='1978-10-26', end='2019-10-17')
    new = v.reindex(index=full)
    return new

'''
This function replaces dates with no data with the average of the date 
before and after. If multiple days are missing then the average of the
date a year before and after is assigned. It only edits the exsisting series
so nothing is returned 
'''
def clean_data(series):
    for i in range(len(series.isna())):
        if (series.isna().iloc[i]) and not(series.isna().iloc[i-1]) and not(series.isna().iloc[i-1]):
                series.iloc[i] = (series.iloc[i-1]+series.iloc[i+1]) / 2
    for i in range(len(series.isna())):
        if (series.isna().iloc[i]):
            now = series.index[i]
            year_before = now.year - 1
            before = datetime(year_before,now.month,now.day)
            year_after = now.year + 1
            after = datetime(year_after,now.month,now.day)
            avg = (series.loc[before] + series.loc[after]) / 2
            series.iloc[i] = avg
     
'''
This function creates a list of all the days of a non leap year in
'MMDD' format. A helper function is called to do this. The said list
is then returned
'''
def get_column_labels():
    days = []
    for month in range(1,12):
        num = datetime(1987,month+1,1) - datetime(1987,month,1) 
        for day in range(1,num.days+1):
            days.append(needs_zero(month)+needs_zero(day))
    for n in range(1,32):
        days.append(str(12)+needs_zero(n))
    return days

'''
A helper function to assign a zero in front of single digit numbers
and returns the string
'''   
def needs_zero(n):
    if n>=10:
        return str(n)
    return '0'+str(n)

'''
This function moves the data from the clean original series to a new datafram
indexed by year and columns in 'MMDD' format from get_column_labels(). The 
corresponding data in the series is moved to the correct date in the dataframe,
which is then returned
'''
def extract_df(series):
    index = [n for n in range(1979,2019)]
    df = pd.DataFrame(index=index, columns=get_column_labels(), dtype=np.float64)
    for date in series.index:
        year = date.year
        month = date.month
        day = date.day
        md = needs_zero(month)+needs_zero(day)
        if year in df.index and needs_zero(month)+needs_zero(day) in df.columns:
            df.loc[year,md] = series[date]
    return df

'''
Returns a series of sea ice extent of the year 2019 to (available)
'''
def extract_2019(series):
    return series[datetime(2019,1,1):]
    
'''
Main uses the functions documented above to write 'data_79_18.csv' and
'data_2019.csv' files which are then stored in the same directory as this
file. The first file being all sea ice extent from 1979 to 2018 and the second
being data from 2019
'''
def main():
    series = get_data()
    clean_data(series)
    full = extract_df(series)
    this_year = extract_2019(series)
    print(full)
    full.to_csv(r'/Users/mac/Desktop/ISTA 131/hw7/data_79_18.csv')
    this_year.to_csv(r'/Users/mac/Desktop/ISTA 131/hw7/data_2019.csv')

main()















