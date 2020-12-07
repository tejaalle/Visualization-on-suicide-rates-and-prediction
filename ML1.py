# Author: name (banner no) <@dal.ca>
# File: This will return all the visualization in tab for Continents.

# imports
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from data_encoding import *

#
def simple_random_forest_regressor(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)
    model = RandomForestRegressor()  # Now I am doing a regression!
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    score = model.score(X_test, y_test)
    return dict(model=model, score=score, test_prediction=y_predict)

#
def linear_regressor(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    score = model.score(X_test, y_test)
    return dict(model=model, score=score, test_prediction=y_predict)

#
def suciderate_prediction(df, country="Albania",age="75+ years",sex="male",year=2020):
    df = pd.read_csv("master.csv")
    df = df.loc[df["country"]==country]
    df1 = df.loc[:, ['year', 'sex', 'age', 'suicides_no']]
    df1.loc[len(df1)]= [year,sex,age,0]
    df1 = one_hot_encoder(df1,"sex")
    df1 = one_hot_encoder(df1,"age")
    testdf = df1.tail(1)
    df1 = df1.iloc[:-1,:]
    X = df1.iloc[:,:-1]
    y = df1.iloc[:,-1]
    random = simple_random_forest_regressor(X,y)
    linear = linear_regressor(X,y)
    if(linear["score"]>random["score"]):
        answer= linear["model"].predict(testdf.iloc[:,:-1])
        return answer,linear["score"]
    else:
        answer = random["model"].predict(testdf.iloc[:,:-1])
        return answer,random["score"]

df = pd.read_csv("master.csv")
suciderate_prediction(df)


