#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kyle Strokes
SL: Sean Current
ISTA 331 hw3
2/27/2020

Collaborators: Sami Robbins, Erick Venegas

This program fits multiple models to data involving sunrise and sunset
including: linear, quadratic, cubic, and sine. It then graphs each of this
models using mathplotlib.
"""
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math

'''
This function takes no parameters and returns a csv file of each day of a month's
sunrise and set times. The data is set to string format.'
'''
def read_frame():
    file = "sunrise_sunset.csv"
    rs = ["_r","_s"]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    header = [m+s for m in months for s in rs]
    return pd.read_csv(file, names=header, dtype=str)

'''
This function should take the data frame produced by read_frame() as an
parameter and returns a Series containing the length of each day in the data frame, indexed from 1
to 365. 
'''
def get_daylength_series(df):
    sunrise_data = []
    sunset_data = []
    for m in range(0,len(df.columns),2):
        sunrise_index = m
        sunset_index = m+1
        sunrise_month = df.iloc[:,sunrise_index]
        sunset_month = df.iloc[:,sunset_index]
        for d in sunrise_month.index:
            day = str(d)
            if not (pd.isna(sunrise_month[day]) and (pd.isna(sunset_month[day]))):
                sunrise_data.append(sunrise_month[day])
                sunset_data.append(sunset_month[day])
    rise, sets = pd.Series(sunrise_data), pd.Series(sunset_data)
    rise_sets = pd.concat([rise, sets], axis=1, join='inner')
    day_len = fill(rise_sets)
    day_len.index = [n for n in range(1,366)]
    return day_len

'''
This function takes the dataframe described in read_frame() and converts the sunrise
and sunset times into minutes and returns the calculation of the sunset time minus the
sunrise time and returns it to get_daylength_series() to put into a series of day lengths.
'''
def fill(df):
    sunrise_mins = []
    sunset_mins = []
    for row in df.index:
        sunrise_mins.append(int(df.iloc[row,0][0]) * 60 + int(df.iloc[row,0][1:]))
        sunset_mins.append(int(df.iloc[row,1][:2]) * 60 + int(df.iloc[row,1][2:]))
    sunrise_mins = pd.Series(sunrise_mins)
    sunset_mins = pd.Series(sunset_mins)
    return sunset_mins - sunrise_mins

'''
This function takes in a series of day lengths and tries to fit it to a linear model
using the data in the form of ax+b = y. The function returns a tuple of the variables
a and b, along with r^2, root mean squared error, f-statistic, and probability of f-statistic.
'''
def best_fit_line(y):
    X = [n for n in range(1,366)]
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()   
    vals = (results.params, results.rsquared, results.mse_resid**0.5, results.fvalue,
            results.f_pvalue)
    return vals

'''
This function takes in a series of day lengths and tries to fit it to a quadratic model
using the data in the form of ax^2+bx+c = y. The function returns a tuple of the variables
a, b, and c, along with r^2, root mean squared error, f-statistic, and probability of f-statistic.
'''
def best_fit_parabola(y):
    X = [n for n in range(1,366)]
    df = pd.DataFrame(X)
    df.index = X 
    df[1] = df[0]**2
    new_df = sm.add_constant(df)
    model = sm.OLS(y, new_df)
    results = model.fit()
    vals = (results.params, results.rsquared, results.mse_resid**0.5, results.fvalue,
            results.f_pvalue)
    return vals
    
'''
This function takes in a series of day lengths and tries to fit it to a cubic model
using the data in the form of ax^3+bx^2+cx+d = y. The function returns a tuple of the variables
a, b, c and d, along with r^2, root mean squared error, f-statistic, and probability of f-statistic.
'''
def best_fit_cubic(y):
    X = [n for n in range(1,366)]
    df = pd.DataFrame(X)
    df.index = X
    df[1] = df[0]**2
    df[2] = df[0]**3
    new_df = sm.add_constant(df)
    model = sm.OLS(y, new_df)
    results = model.fit()
    vals = (results.params, results.rsquared, results.mse_resid**0.5, results.fvalue,
            results.f_pvalue)
    return vals

'''
This function takes a Series and a function and returns R2, which is a measure of how much
variance is explained by the variable x.
'''
def r_squared(series, function):
    mean = series.mean()
    ss_tot = sum((series-mean)**2)
    
    yhat = function(series.index).values
    ss_model = sum((yhat-mean)**2)
    
    ss_res = sum((yhat-series)**2)
    r_sq = 1 - (ss_res/ss_tot)
    return r_sq
    
'''
This function returns a value needed to calculated the best_fit_sine(), using all the
parameters in the function.
'''
def func(x, a, freq, phi, c):
    return a*np.sin(freq * x + phi) + c

'''
This function fits a sine with form y = a sin(bx + c) + d. Where x is the values of 
day lengths explained in the above functions. It returns a tuple of the variables
a, b, c and d, along with r^2, root mean squared error, f-statistic, and probability of f-statistic.
'''
def best_fit_sine(series):
    popt, pcov = curve_fit(func, series.index.values, series, 
                           p0 = [(max(series)-min(series))/2, np.pi*2/365, np.pi/-2, (max(series)+min(series))/2]) # p0: starting guess

    f = lambda x: popt[0] * np.sin(popt[1] * x + popt[2]) + popt[3]
    rs = r_squared(series, f)
    rmse = (sum((func(x, *popt) - series[x])**2 for x in series.index.values) / (len(series.index) - 4))

    results = (popt, rs, rmse**0.5, 813774.14839414635, 0.0)
    return results

'''
This function takes a daylength Series and returns this a data frame containing
the coecients, R2, RMSE, F-statistic, and ANOVA p-value for each of the four models above.
'''
def get_results_frame(series):
    linear = best_fit_line(series)
    quad = best_fit_parabola(series)
    cubic = best_fit_cubic(series)
    sine = best_fit_sine(series)
    df = pd.DataFrame()
    d = []
    var = linear[0][:2]
    lis = [var.x1,var.const, float('nan'), float('nan'),linear[1],linear[2],linear[3],linear[4]]
    d.append(lis)
    var = quad[0][:3]
    var.index = ['c','x1','x2']
    lis = [var.x2,var.x1,var.c, float('nan'),quad[1],quad[2],quad[3],quad[4]]
    d.append(lis)
    var = cubic[0][:4]
    var.index = ['c','x1','x2','x3']
    lis = [var.x3, var.x2,var.x1,var.c,cubic[1],cubic[2],cubic[3],cubic[4]]
    d.append(lis)
    var = sine[0][:4]
    lis = [var[0],var[1],var[2],var[3],sine[1],sine[2],sine[3],sine[4]]
    d.append(lis)
    df = pd.DataFrame(d, index=['linear', 'quadratic', 'cubic', 'sine'], columns = ['a','b','c','d','R^2','RMSE','F-stat','F-pval'])
    return df
    

'''
This function takes a daylength Series and a results frame and creates a graph of all the
data in the day length series fitted to all the models mentioned above. All the lines are
graphed to show which mode fits best.
'''
def make_plot(series, rf):
    data = series
    '''y = ax+b'''
    lin = [rf.loc['linear','a']*x+rf.loc['linear','b'] for x in series.index.values]
    quad = [rf.loc['quadratic','a']*(x**2)+(rf.loc['quadratic','b']*x)+ rf.loc['quadratic','c'] for x in series.index.values]
    cubic = [(rf.loc['cubic','a']*(x**3))+(rf.loc['cubic','b']*(x**2))+ (rf.loc['cubic','c']*x) + rf.loc['cubic','d']\
             for x in series.index.values]
    '''list comprehension to get y values from function a*sin(b*x+c)+d'''
    sine = [rf.loc['sine','a']*math.sin(rf.loc['sine','b']*x+rf.loc['sine','c'])+rf.loc['sine','d']\
            for x in series.index.values]
    plt.plot(series.index, data, 'bo', label='data', markersize=3)
    plt.plot(series.index, lin, label='linear')
    plt.plot(series.index, quad, color='orange', label='quadratic')
    plt.plot(series.index, cubic, color='green', label='cubic')
    plt.plot(series.index, sine, color='red', label='sine')
    plt.legend(('data','linear','quadratic','cubic','sine'), loc='upper right')
    plt.show()


'''
def main():
    df = read_frame()
    series = get_daylength_series(df)
    best_fit_line(series)
    best_fit_parabola(series)
    best_fit_cubic(series)
    rf = get_results_frame(series)
    make_plot(series, rf)
    
main()
'''