# Author: name (banner no) <@dal.ca>
# File: This will return all the visualization in tab for Continents.

# imports
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


def one_hot_encoder(df, column):
    ohe = OneHotEncoder()
    # hotencoder accepts 2-D array so converting the column into 2D array
    ohe.fit(pd.DataFrame(df[column]))
    columnNames = []
    for i in df.columns:
        if i != column:
            columnNames.append(i)
    enc_df = pd.DataFrame(ohe.fit_transform(df[[column]]).toarray())
    df = df.drop(column, axis=1)
    temp = []
    for i in range(len(df)):
        temp.append(i)
    df["temp"]=temp
    enc_df["temp"]=temp
    df = pd.merge(enc_df, df, on='temp')
    df = df.drop('temp', axis=1)
    columnNames = list(ohe.get_feature_names()) + columnNames
    df.columns = columnNames
    return df
