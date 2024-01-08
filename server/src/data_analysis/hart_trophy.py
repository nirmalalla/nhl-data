import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor


winners = {
    2016: "Patrick Kane",
    2017: "Connor McDavid",
    2018: "Taylor Hall",
    2019: "Nikita Kucherov",
    2020: "Leon Draisaitl",
    2021: "Connor McDavid",
    2022: "Auston Matthews"
}

def calculateValue(goals, points, icetime, games):
    return [goals / games, points / games, icetime / games]

def createDataframe():
    values = []
    for key in winners.keys():
        values.append(gatherData(winners.get(key), key))

    return values

    
def gatherData(name, year):
    tmp_df = pd.read_csv("../data/_data - skaters" + str(year) + ".csv")
    tmp_df = tmp_df.loc[tmp_df["name"] == name]

    goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
    points = tmp_df.at[tmp_df.index[0], "I_F_points"]
    icetime = tmp_df.at[tmp_df.index[0], "icetime"]
    games = tmp_df.at[tmp_df.index[0], "games_played"]

    return calculateValue(goals, points, icetime, games)

def gather2023Data():
    df = pd.read_csv("../data/_data - skaters2023.csv")
    X = []
    y = []
    threshold_games = max(df["games_played"]) * 0.70
    threshold_icetime = max(df["icetime"]) * 0.40
    threshold_points = max(df["I_F_points"]) * 0.60
    
    name_values = []

    for name in df["name"]:
        tmp_df = df.loc[df["name"] == name]
        games = tmp_df.at[tmp_df.index[0], "games_played"]
        icetime = tmp_df.at[tmp_df.index[0], "icetime"]
        position = tmp_df.at[tmp_df.index[0], "position"]
        points = tmp_df.at[tmp_df.index[0], "I_F_points"]
        
        if (games >= threshold_games and icetime >= threshold_icetime and position != "D" and points >= threshold_points):
            X.append([2023])
            goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
            value = calculateValue(goals, points, icetime, games)
            y.append(value)
            name_values.append([name, value])

    return name_values

def findDistance(data, pred):
    total = 0
    index = 0

    for n in data:
        total += abs(pred[index] - n)
        index += 1

    return total


def findClosest(name_values, pred):
    min = []
    for n in name_values:
        distance = findDistance(n[1], pred)

        if (len(min) < 5 or distance < min[len(min) - 1][1]):
            if(len(min) == 5):
                min[4] = [n[0], distance]
            else:
                min.append([n[0], distance])
            
            min = sorted(min, key=lambda x: x[1])

    return min

def hartTrophyData():
    X_train = []

    for key in winners.keys():
        X_train.append([key])

    
    y_train = createDataframe()
    
    regr =  MultiOutputRegressor(LinearRegression())
    regr.fit(X_train, y_train)

    X_test = np.array([[2022.5], [2023], [2023.5]])

    y_pred = regr.predict(X_test)

    name_values = gather2023Data()
    closest_player = findClosest(name_values, y_pred[1])
    
    return closest_player