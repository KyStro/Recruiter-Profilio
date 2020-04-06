









"""
Kyle Strokes
SL: Aleigh Crawford
ISTA 131 hw6

This program calls csv_to_dataframe to make a dataframe from a csv file.
A growth rate column is then added to the dataframe, along with a
years to extinction column. dying_countries function returns a sorted
series of countries that will go extinct the soonest. The first five from
that series are printed.
"""
import numpy as np
import pandas as pd

'''
This function reads in a csv value of country data and returns a
dataframe in which the country names are the indices and all European
comma's for decimals are changed to '.'
'''
def csv_to_dataframe(file): 
    return pd.read_csv(file, index_col=0, decimal=',')

'''
This function takes a dataframe from the previous funciton and puts the
Region column in title case format while also deleting whitespace from
the Region and Country columns. "Country" is also removed from dataframe.
None is returned.
'''
def format_df(df):
    df["Region"] = df["Region"].str.title().str.strip()
    stripped_countries = [c.strip() for c in df.index]
    df.index = stripped_countries
    
'''
This function makes a new column for a country's growth rate by subtracting
the country's death rate from its birth rate.
'''
def growth_rate(df):
    df["Growth Rate"] = df["Birthrate"] - df["Deathrate"]    
    
'''
This function is a helper for years_to_extinction(). It takes a country's
inital population (p) and negative growth rate (r) and returns the number of
years until the population is less than 2 people.
'''
def dod(p, r):
    num_yrs = 0
    while p > 2:
        p = p + p * r / 1000
        num_yrs += 1
    return num_yrs 

'''
This function initalizes values of a new column in a dataframe "Years to Extinction" to NaN.
It then finds countries with a negative growth rate and uses dod() to determine
the years to extinction and it updates the column.
'''
def years_to_extinction(df):
    df["Years to Extinction"] = np.nan
    for country in df.index:
        if df.loc[country]["Growth Rate"] < 0:
            p = df.loc[country,"Population"]
            r = df.loc[country,"Growth Rate"]
            df.loc[country,"Years to Extinction"] = dod(p,r)
            
'''
This function takes in a dataframe and returns a sorted series of countries with
negative growth rates; sorted by how many years until they are extinct (ascending)
'''    
def dying_countries(df):
    index = []
    values = []
    dead = df.isna()
    for i in range(len(df)):
        if not dead.iloc[i,-1]:
            index.append(df.iloc[i].name)
            values.append(df.iloc[i,-1])
    return pd.Series(values, index).sort_values()

'''
Main calls csv_to_dataframe to make a dataframe from a csv file.
A growth rate column is then added to the dataframe, along with a
years to extinction column. dying_countries function returns a sorted
series of countries that will go extinct the soonest. The first five from
that series are printed.
'''
def main():
    df = csv_to_dataframe("countries_of_the_world.csv")
    growth_rate(df)
    years_to_extinction(df)
    dead_series = dying_countries(df).head()
    for i in range(len(dead_series)):
        name = dead_series.index[i].strip()
        print(f"{name}: {dead_series[i]} Years to Extinction")
    
    
    
    
    
    
    
    
    
    