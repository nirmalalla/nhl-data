import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import linear_model

winners = {
    2015: "Alex Ovechkin",
    2016: "Sidney Crosby",
    2017: "Alex Ovechkin",
    2018: "Alex Ovechkin",
    2019: "David Pastrnak",
    2019: "Alex Ovechkin",
    2020: "Auston Matthews",
    2021: "Auston Matthews",
    2022: "Connor McDavid"
}

def calculateValue(goals, icetime, games):
    return (goals / (icetime))

def createDataframe():
    values = {}
    for key in winners.keys():
        values[key] = gatherData(winners.get(key), key)

    df = pd.DataFrame(columns=winners.keys())
    df.loc[len(df)] = values
    return df

def gatherData(name, year):
    tmp_df = pd.read_csv("../data/_data - skaters" + str(year) + ".csv")
    tmp_df = tmp_df.loc[tmp_df["name"] == name]

    goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
    icetime = tmp_df.at[tmp_df.index[0], "icetime"]
    games = tmp_df.at[tmp_df.index[0], "games_played"]

    return calculateValue(goals, icetime, games)

def gather2023Data():
    df = pd.read_csv("../data/_data - skaters2023.csv")
    X = []
    y = []
    threshold_games = max(df["games_played"]) * 0.5
    threshold_icetime = max(df["icetime"]) * 0.5
    
    name_values = []

    for name in df["name"]:
        tmp_df = df.loc[df["name"] == name]
        games = tmp_df.at[tmp_df.index[0], "games_played"]
        icetime = tmp_df.at[tmp_df.index[0], "icetime"]
        position = tmp_df.at[tmp_df.index[0], "position"]
        points = tmp_df.at[tmp_df.index[0], "I_F_points"]
        
        if (games >= threshold_games and icetime >= threshold_icetime and position != "D"):
            X.append([2023])
            goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
            value = calculateValue(goals, icetime, games)
            y.append(value)
            name_values.append([name, value])

    return name_values

def findClosest(name_values, pred):
    min = []
    for n in name_values:
        if (len(min) < 5 or abs(n[1] - pred) < abs(min[len(min) - 1][1] - pred)):
            if(len(min) == 5):
                min[4] = [n[0], n[1]]
            else:
                min.append([n[0], n[1]])
            
            min = sorted(min, key=lambda x: x[1])

    return min

def rocketRichardTrophyData():
    df = createDataframe()

    X_train = []

    for key in winners.keys():
        X_train.append([key])

    
    y_train = np.array(df.values[0])
    
    regr =  LinearRegression()
    regr.fit(X_train, y_train)

    X_test = np.array([[2022.5], [2023], [2023.5]])

    y_pred = regr.predict(X_test)
    
    name_values = gather2023Data()
    closest_player = findClosest(name_values, y_pred[0])

    return closest_player
