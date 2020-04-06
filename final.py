import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


'''
Gets all games 1966-2018
'''


def get_vegas_data():
    file = "vegas_odds.csv"
    df = pd.read_csv(file, usecols=["schedule_date", "team_home","score_home","score_away","team_away"])
    return df.iloc[:12411,:]


def get_all_teams():
    file = "nfl_teams.csv"
    df = pd.read_csv(file)
    teams = df["team_name"]
    return teams


def make_team_dict(teams):
    dic = {}
    for t in teams:
        if t not in dic:
            dic[t] = [0,0]
    return dic


def update_win_pct(dic, df):
    for i in df.index:
        home = df.iloc[i].team_home
        home_score = df.iloc[i].score_home
        away = df.iloc[i].team_away
        away_score = df.iloc[i].score_away
        win, loss = get_winner_loser(home,home_score,away_score,away)
        if win != None or loss != None:
            dic[win][0] += 1
            dic[win][1] += 1
            dic[loss][1] += 1
    for team in dic:
        dic[team] = dic[team][0]/dic[team][1]
        
        
def remove_old_teams(dic):
    old = ['Phoenix Cardinals','St. Louis Cardinals','Baltimore Colts','San Diego Chargers',
           'St. Louis Rams','Boston Patriots','Los Angeles Raiders','Houston Oilers','Tennessee Oilers']
    for key in old:
        del dic[key]
        

def get_top_10_winning(dic):
    teams = sorted(dic,key=dic.get)
    return teams[-10:]



def make_graph_1(dic, top_10):
    x = np.arange(len(top_10))
    top_10_pct = [dic[t]*100 for t in top_10]

    plt.barh(x, top_10_pct, align='center', alpha=1, tick_label=top_10,
             color=['r','indigo','darkviolet','c','orange','midnightblue','crimson','yellow','silver','deepskyblue'])
    plt.title('Top 10 Most Winningest Teams in the NFL (1966-2018)')
    plt.xlim(0, 100)
    plt.xlabel('Win Percentage (% Out of 100)', labelpad=15)
    plt.show()
    

def get_winner_loser(home,home_score,away_score,away):
    if home_score == away_score:
        return None, None
    elif home_score > away_score:
        return home, away
    return away, home



def get_winner_loser(home,home_score,away_score,away):
    if home_score == away_score:
        return None, None
    elif home_score > away_score:
        return home, away
    return away, home

    
def get_vegas_data2():
    file = "vegas_odds.csv"
    df = pd.read_csv(file, usecols=["team_home","score_home","score_away","team_away", "team_favorite_id"])
    return df.iloc[:12411,:]

def get_vegas_actual(df):
    correct = 0
    wrong = 0
    tot = 0
    code_teams = map_code_to_teams()
    for row in df.index:
        win, loss = get_winner_loser(df.iloc[row,0],df.iloc[row,1],df.iloc[row,2],
                               df.iloc[row,3])
        if win == None or pd.isna(df.iloc[row,4]):
            continue
        winner_id = code_match(code_teams, win)
        if teams_match(winner_id, df.iloc[row,4]):
            correct += 1
        else:
            wrong += 1
        tot += 1
    return correct/tot * 100, wrong/tot * 100
    
    
def make_graph_2(c, w):
    y = [c,w]
    x = np.arange(len(y))
    plt.ylim(0, 100)
    plt.bar(x, y, align='center', alpha=1, width=0.7, tick_label=['Correct','Incorrect'],
            color=['green','red'])
    plt.xlabel('Prediction Outcome')
    plt.ylabel('Frequency (%)')
    plt.title('Vegas Favorite Prediction Outcomes for NFL Games (1979-2018)', pad=15)
    plt.show()

def map_code_to_teams():
    file = "nfl_teams.csv"
    df = pd.read_csv(file, usecols=[0,2])
    d = {}
    for row in df.index:
        code = df.iloc[row,1]
        team = df.iloc[row,0]
        if code not in d:
            d[code] = []
            d[code].append(team)
        else:
            d[code].append(team)
    return d

def code_match(dic, team):
    for key in dic.keys():
        for teams in dic[key]:
            if team in teams:
                return key
            
def teams_match(t,s):
    return t == s

def main():
    vegas2 = get_vegas_data2()
    correct, wrong = get_vegas_actual(vegas2)
    make_graph_2(correct,wrong)
    
main()
'''
        
'''
def map_code_to_teams():
    file = "nfl_teams.csv"
    df = pd.read_csv(file, usecols=[0,2])
    d = {}
    for row in df.index:
        code = df.iloc[row,1]
        team = df.iloc[row,0]
        if code not in d:
            d[code] = []
            d[code].append(team)
        else:
            d[code].append(team)
    return d

def teams_match(t,s):
    return t == s

def code_match(dic, team):
    for key in dic.keys():
        for teams in dic[key]:
            if team in teams:
                return key
            
def get_years_points():
    file = "vegas_odds.csv"
    df = pd.read_csv(file, usecols=["schedule_season","score_home","score_away"])
    return df.iloc[:12411,:]
    

def get_xy_years_pts(df):
    years = [n for n in range(1966,2019)]
    pts = []
    for year in years:
        mini_df = df.loc[df['schedule_season'] == year]
        total = mini_df.sum(skipna=True)['score_away'] + mini_df.sum(skipna=True)['score_home']
        pts.append(total/len(mini_df))
    return years, pts






    
    
def make_graph_2(c, w):
    y = [c,w]
    x = np.arange(len(y))
    plt.ylim(0, 100)
    plt.bar(x, y, align='center', alpha=1, width=0.7, tick_label=['Correct','Incorrect'],
            color=['green','red'])
    plt.xlabel('Prediction Outcome')
    plt.ylabel('Frequency (%)')
    plt.title('Vegas Favorite Prediction Outcomes for NFL Games (1979-2018)', pad=15)
    plt.show()

def scatterplot(x, y):
    plt.scatter(x,y, marker='x', color='darkblue')
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='crimson')
    plt.xlabel('Year', labelpad=15)
    plt.ylabel('Average Total Points Per Game', labelpad=15)
    plt.title('Average Total Points For a NFL Game vs. Year', pad=15)






def main():
    
    vegas2 = get_vegas_data2()
    correct, wrong = get_vegas_actual(vegas2)
    make_graph_2(correct,wrong)

    vegas = get_vegas_data()
    teams = get_all_teams()
    team_dict = make_team_dict(teams)
    update_win_pct(team_dict, vegas)
    remove_old_teams(team_dict)
    top_10 = get_top_10_winning(team_dict)
    make_graph_1(team_dict, top_10)


    years_pts = get_years_points()
    x, y = get_xy_years_pts(years_pts)
    scatterplot(x, y)
    
    
main()
