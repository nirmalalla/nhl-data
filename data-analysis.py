import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn import linear_model


winners = {
    2018: "Taylor Hall",
    2019: "Nikita Kucherov",
    2020: "Leon Draisaitl",
    2021: "Connor McDavid",
    2022: "Auston Matthews"
}

def calculateValue(goals, points, icetime, games):
    return ((goals + points) / (icetime / games))

def createDataframe():
    values = {}
    for key in winners.keys():
        values[key] = gatherData(winners.get(key), key)

    df = pd.DataFrame(columns=winners.keys())
    df.loc[len(df)] = values
    return df

    
def gatherData(name, year):
    tmp_df = pd.read_csv("./data/_data - skaters" + str(year) + ".csv")
    tmp_df = tmp_df.loc[tmp_df["name"] == name]

    goals = tmp_df.at[tmp_df.index[0], "I_F_goals"]
    points = tmp_df.at[tmp_df.index[0], "I_F_points"]
    icetime = tmp_df.at[tmp_df.index[0], "icetime"]
    games = tmp_df.at[tmp_df.index[0], "games_played"]

    return calculateValue(goals, points, icetime, games)

def plotData():
    df = createDataframe()

    X_train = []

    for key in winners.keys():
        X_train.append([key])

    
    y_train = np.array(df.values[0])
    
    regr =  LinearRegression()
    regr.fit(X_train, y_train)

    X_test = np.array([[2023]])

    y_pred = regr.predict(X_test)
    
    plt.plot(X_test, y_pred, linewidth="3", marker="o")
    plt.show()

plotData()