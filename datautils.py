import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import subprocess
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from pandas import DataFrame
import datetime
from glob import glob; from os.path import expanduser
from itertools import combinations



def get_latest_data():
    subprocess.run(["kaggle","datasets","download","-d","wyattowalsh/basketball"])

def edit_gamescsv(gamestbl, season):
    temp_games = gamestbl[gamestbl['season_id'] == 20000 + season]
    return temp_games

def whatseason():
    cur_year = datetime.date.today().year
    cur_date = datetime.date.today()
    if (cur_date.month <= 10):
        return cur_year - 1
    else:
        return cur_year

def getteamid(teams, fname):
    return teams[teams['full_name'] == fname].iloc[0]['id']

def get_proba(df, x_predict, lst):
    ys = df["winner"].tolist()
    X = df.drop(columns="winner")[lst]
    lr = LogisticRegression()
    clf = lr.fit(X, ys)
    y_hat = clf.predict(x_predict)
    y_prob = clf.predict_proba(x_predict)[:,1]
    return y_prob


