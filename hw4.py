#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kyle Strokes
SL: Sean Current
ISTA 331 Hw4
3/30/2020

This module takes dataframe the Tucson Airport from 1987 to 2016.
The dataframe is first cleaned and then scaled. Intial centroids
are set based on what parameter k is set to. Then a loop is run
updating the centroid values and each day of the year. The days
of the year are then finally mapped to a cluster, being the nearest
centroid.
"""
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
import math

'''
Takes a int year and returns if the year is a leap year
'''
def is_leap_year(year):
    return year%4==0

'''
Takes two feature vectors v1 and v2 and returns the euclidean
distance between the two points
'''
def euclidean_distance(v1, v2):
    l = []
    for i in range(len(v1)):
        l.append((v1[i] - v2[i])**2)
    return math.sqrt(sum(l))

'''
Makes a dataframe of Tucson Airport weather data from the years
1987-2016. Adds an index of datetime objects of the dates from
1/1/1987' to '31/12/2016'. Returns the dataframe.
'''
def make_frame():
    df = pd.read_csv('TIA_1987_2016.csv')
    dr = pd.date_range('1/1/1987','31/12/2016')
    df.set_index(dr, inplace = True)
    return df

'''
Takes in make_frame() dataframe and replaces March 10 & 11, 1987
Dewpt from -999 to the average of all other 29 years Dewpts for each
date.
'''
def clean_dewpoint(df):
    fix = [datetime.datetime(1987, 3, 10), datetime.datetime(1987, 3, 11)]
    for d in fix:
        all_others = [df.loc[datetime.datetime(d.year+x,d.month,d.day),'Dewpt'] for x in range(30) if x != 2010-1987]
        avg = sum(all_others)/len(all_others)
        df.loc[d.replace(year=2010),'Dewpt'] = avg    
    
'''
Takes a datetime object and returns the # day of the year for the
date. On leap years Febuary 29 returs 366.
'''
def day_of_year(dto):
    tt = dto.timetuple()
    if is_leap_year(tt[0]): 
        if tt[1] == 2 and tt[2] == 29:
            return 366
        else:
            new = dto.replace(year=1999)
            tt = new.timetuple()
            return tt[-2]
    else:
        return tt[-2]

'''
Takes a dataframe and returns a dataframe of the means of each
column for every # day of the year
'''  
def climatology(df):
    means = df.groupby(day_of_year).mean()[lambda x: x.index != 366]
    return means

'''
Takes a dataframe and scales the values in the dataframe to prevent
skew in the algorithm.
'''
def scale(df):
    scaler = MinMaxScaler(copy = False)
    scaler.fit_transform(df)

'''
Takes a dataframe df and a int k and splits the dataframe into k equal
points. The centroids are the k-th value inside the dataframe. A dataframe
of these centroids is returned.
'''
def get_initial_centroids(df, k):
    idx = [x for x in range(k)]
    vals = [nd * (len(df) // k) + 1 for nd in idx]
    data = [df.loc[vals[n]] for n in idx]
    cents = pd.DataFrame(data=data, index=idx)
    return cents

'''
Takes a centroid frame and a feature vector and returns the closest
centroid to the feature vector: (int)
'''
def classify(cf, fv):
    eds = [(x,euclidean_distance(cf.loc[x], fv)) for x in cf.index]
    eds.sort(key=lambda x: x[1])
    return eds[0][0]

'''
Takes a scaled dataframe and a centroid frame and returns a series
of each row in the dataframe mapped to a centroid it is nearest
'''
def get_labels(sdf, cf):
    l = [classify(cf, sdf.loc[day]) for day in sdf.index]
    return pd.Series(data=l, index=sdf.index)

'''
Takes a scaled dataframe, a centroid frame, and a series.

Gets the mean of every like centroid in the centroid frame

Then updates the values in the scaled dataframe with those means.
'''
def update_centroids(sdf, cf, s):
    for cent in cf.index:
        matches = [day for day in s.index if s[day] == cent]
        matchdf = sdf.loc[matches]
        cf.loc[cent] = matchdf.mean()

'''
Takes a dataframe and a int k and uses the functions above to
execute the k_means cluster algorithm to return a series of k
updated centroids and an updated series with each day of the 
year mapped to its final centroid cluster.
'''    
def k_means(df, k):
    cents = get_initial_centroids(df, k)
    old = get_labels(df,cents)
    while True:
        update_centroids(df, cents, old)
        new = get_labels(df,cents)
        if old.equals(new):
            break
        else:
            old = new       
    return cents, new


def main():
    raw = make_frame()
    clean_dewpoint(raw)    
    climo = climatology(raw)
    cents, new = k_means(climo, 10)
    
main()