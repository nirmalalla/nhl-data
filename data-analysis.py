import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import linear_model

df = pd.read_csv("./data/_data - skaters2022.csv")

goals_X_train = df[["games_played"]]
goals_y_train = df["I_F_points"]
labels = df["name"]

regr = linear_model.LinearRegression()
regr.fit(goals_X_train, goals_y_train)

goals_y_pred = regr.predict(goals_X_train)

plt.plot(goals_X_train, goals_y_pred, color="blue", linewidth="3", label="Predicted Values")
plt.scatter(goals_X_train, goals_y_train, label="Real Data Points")
plt.xlabel("Total Games Played")
plt.ylabel("Total Points Scored")

plt.legend()
plt.show()