#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kyle Strokes
SL: Aleah Crawford
11/18/2019
ISTA 131 Hw 8
Collaborators: Samantha Robbins


This program reads in a csv file that contains the extent of sea ice.
There were some missing dates in the data, clean_data() replaces dates
with no data with the average of the date before and after. If multiple days
are missing then the average of the date a year before and after is assigned.
After the data is cleaned. A new dataframe is made indexed by year and each
column is in the format 'MMDD'. This data from the cleaned series is moved to
the dataframe. The means and standard deviation is taken from all the years
in the dataframe, which is then later expressed as a plot in make_fig_1().
The datafram is then categorized in decades and the mean is taken for each
decade and similar plot is expressed in make_fig_2()
"""

from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


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
This function returns a series from a csv file containing sea ice extent
from the year 2019. The series stops on 10/17/19.
'''
def get_2019():
    file = 'data_2019.csv'
    stop = get_column_labels().index('1018')
    index = get_column_labels()[:stop]
    df = pd.read_csv(file, header=None)
    df.index=index
    return df.iloc[:,1]
    

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
This function takes a dataframe with rows representing years 1979 to 2018.
The columns are every day in the calender year. The data is the sea ice extent
on said day and year. The dataframe returned is indexed by the means and 
standard deviations of each day through all those years.
'''
def extract_fig_1_frame(df):
    means = []
    stds = []
    for col in df.columns:
        mean = df[col].mean()
        sd_2 = df[col].std() * 2
        means.append(mean)
        stds.append(sd_2)
    df2 = pd.DataFrame(index=['mean','two_s'], data=[means,stds], columns=df.columns)
    return df2

'''
This function takes a dataframe with rows representing years 1979 to 2018.
The columns are every day in the calender year. The data is the sea ice extent
on said day and year. The dataframe returned is indexed by each decade (2010s
are up to 2018) and the means for each calender day are calculated as the values
for each decade. Indexed by decade, columns by calender day.
'''
def extract_fig_2_frame(df):
    data = []
    for year in range(1980,2010,10):
        start = year
        end = year + 9
        decade_df = df.loc[start:end]
        decade_avgs = []
        for col in decade_df.columns:
            decade_avgs.append(decade_df[col].mean())  
        data.append(decade_avgs)
    last = []
    for col in df.loc[2010:]:
        last.append(df.loc[2010:,col].mean())
    data.append(last)
    df2 = pd.DataFrame(data, index=['1980s','1990s','2000s','2010s'], columns=df.columns)
    return df2

'''
This function takes the dataframe from extract_fig_1() and makes a line plot
of year day of the year (x) by sea ice extent in 10^6 km^2 (y). A Lengend is
provided to show which lines apply to which data. The mean and -+2 standard
deviations are also highlighted. 2012 and 2019 are shown.
'''
def make_fig_1(ff,df):
    mean = ff.loc['mean']
    plt.plot(mean, label = 'mean')
    plt.plot(df.loc[2012,:], '--', label = '2012')
    plt.plot(get_2019(), label = '2019', color = 'green')
    plt.xticks(['0101','0220','0411','0531','0720','0908','1028','1217'])
    two_s = ff.loc['two_s']
    plt.fill_between(np.linspace(0,365,365), mean+two_s, mean-two_s, 
                     color = 'lightgrey', label = u'\u00B12 std devs')
    plt.ylabel('NH Sea Ice Extent ($10^6$ $km^2$)')
    plt.margins(x=0)
    plt.legend(loc = 'upper right')
    plt.show()

'''
This function takes the dataframe from extract_fig_2() and makes a line plot
of year day of the year (x) by sea ice extent in 10^6 km^2 (y). A Lengend is
provided to show which lines apply to which data. 4 decade averages of sea ice
extent are shown for each day of the year. 2019 is also shown.
'''  
def make_fig_2(df):
    for dec in df.index:
        plt.plot(df.loc[dec,:], '--', label = dec)
    plt.plot(get_2019(), label = '2019')
    plt.xticks(['0101','0220','0411','0531','0720','0908','1028','1217'])
    plt.margins(x=0)
    plt.ylabel('NH Sea Ice Extent ($10^6$ $km^2$)')
    plt.legend(loc = 'lower left')
    plt.show()
    
'''
This program reads in a csv file that contains the extent of sea ice.
There were some missing dates in the data, clean_data() replaces dates
with no data with the average of the date before and after. If multiple days
are missing then the average of the date a year before and after is assigned.
After the data is cleaned. A new dataframe is made indexed by year and each
column is in the format 'MMDD'. This data from the cleaned series is moved to
the dataframe. The means and standard deviation is taken from all the years
in the dataframe, which is then later expressed as a plot in make_fig_1().
The datafram is then categorized in decades and the mean is taken for each
decade and similar plot is expressed in make_fig_2()
'''
def main():
    series = get_data()
    clean_data(series)
    '''full is equal to 'data_79_18.csv' '''
    full = extract_df(series)
    means = extract_fig_1_frame(full)
    decades = extract_fig_2_frame(full)
    make_fig_1(means, full)
    plt.figure()
    make_fig_2(decades)
    
main()







