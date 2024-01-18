import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor

winners = {
    2010: "Nicklas Lidstrom",
    2011: "Erik Karlsson",
    2012: "P.K. Subban",
    2013: "Duncan Keith",
    2014: "Erik Karlsson",
    2015: "Drew Doughty",
    2016: "Brent Burns",
    2017: "Victor Hedman",
    2018: "Mark Giordano",
    2019: "Roman Josi",
    2020: "Adam Fox",
    2021: "Cale Makar",
    2022: "Erik Karlsson"
}

def calculateValue(goals, points, icetime, games, takeaways):
    return [points / games, icetime / games, goals / games, takeaways / games]

def createDataframe():
    #Creating a 2D array to store previous winners with their data
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
    takeaways = tmp_df.at[tmp_df.index[0], "I_F_takeaways"]

    return calculateValue(goals, points, icetime, games, takeaways)

def gather2023Data():
    df = pd.read_csv("../data/_data - skaters2023.csv")
    X = []
    y = []
    threshold_games = max(df["games_played"]) * 0.80
    threshold_icetime = max(df["icetime"]) * 0.6
    
    name_values = []

    for name in df["name"]:
        tmp_df = df.loc[df["name"] == name]
        goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
        games = tmp_df.at[tmp_df.index[0], "games_played"]
        icetime = tmp_df.at[tmp_df.index[0], "icetime"]
        points = tmp_df.at[tmp_df.index[0], "I_F_points"]
        position = tmp_df.at[tmp_df.index[0], "position"]
        takeaways = tmp_df.at[tmp_df.index[0], "I_F_takeaways"]
        
        if (games >= threshold_games and icetime >= threshold_icetime and position == "D"):
            X.append([2023])
            value = calculateValue(goals, points, icetime, games, takeaways)
            y.append(value)
            name_values.append([name, value])

    return name_values

def findDistance(data, pred):
    #Calculating total distance from predicted value
    total = 0
    index = 0

    for n in data:
        total += abs(pred[index] - n)
        index += 1

    return total


def findClosest(name_values, pred):
    #Looping through the name_values to find the top 5 closest players
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

def norrisTrophyData():
    X_train = []

    for key in winners.keys():
        X_train.append([key])

    
    y_train = createDataframe()
    
    #Fitting the model with a regressive model using the data
    regr =  MultiOutputRegressor(LinearRegression())
    regr.fit(X_train, y_train)

    X_test = np.array([[2022.5], [2023], [2023.5]])

    #Testing the data with new values
    y_pred = regr.predict(X_test)

    #Finding the top 5 closest and returning it
    name_values = gather2023Data()
    closest_player = findClosest(name_values, y_pred[1])

    return closest_player