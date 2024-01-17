import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor


winners = {
    2010: "Corey Perry",
    2011: "Evgeni Malkin",
    2012: "Alex Ovechkin",
    2013: "Sidney Crosby",
    2015: "Patrick Kane",
    2016: "Connor McDavid",
    2017: "Taylor Hall",
    2018: "Nikita Kucherov",
    2019: "Leon Draisaitl",
    2020: "Connor McDavid",
    2021: "Auston Matthews",
    2022: "Connor McDavid"
}

def calculateValue(goals, points, icetime, games):
    return [goals / games, points / games, icetime / games]

def createDataframe():
    #Creating a 2D array to store previous winners with their data
    values = []
    for key in winners.keys():
        values.append(gatherData(winners.get(key), key))

    return values

    
def gatherData(name, year):
    #Separating dataframe to only the specified player
    tmp_df = pd.read_csv("../data/_data - skaters" + str(year) + ".csv")
    tmp_df = tmp_df.loc[tmp_df["name"] == name]

    #Gathering relevant data for the player
    goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
    points = tmp_df.at[tmp_df.index[0], "I_F_points"]
    icetime = tmp_df.at[tmp_df.index[0], "icetime"]
    games = tmp_df.at[tmp_df.index[0], "games_played"]

    #Returning the calculated data points based on number of games played
    return calculateValue(goals, points, icetime, games)

def gather2023Data():
    #Reading current data and determining thresholds
    df = pd.read_csv("../data/_data - skaters2023.csv")
    X = []
    y = []
    threshold_games = max(df["games_played"]) * 0.70
    threshold_icetime = max(df["icetime"]) * 0.40
    threshold_points = max(df["I_F_points"]) * 0.60
    
    name_values = []

    #Loop to gather data on each player who meets the required thresholds
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

def hartTrophyData():
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