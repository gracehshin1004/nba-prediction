import numpy as np
import datautils
import datatable
import pandas as pd
import tkinter as tk
lst = ["home total record so far", "away total record so far", "away record against teams home beat", 
        "home record against teams away beat", "avg PPG diff", "home wins over away so far", 
        "away record away", "home record home"]
window = tk.Tk()
def main():
 

    bool_getseason = input("Would you like to import the latest data? (necessary for the first time) (Y/N) ")

    while (True):
        if ((bool_getseason == "Y") | (bool_getseason == "N")):
            break
        bool_getseason = input("Please make sure your input is 'Y' or 'N'" )
    if bool_getseason == "Y":
        datautils.get_latest_data()
        input("Unzip 'basketball.zip' now. When you've unzipped the file, press enter ")

    games = pd.read_csv("basketball/csv/game.csv")
    teams = pd.read_csv("basketball/csv/team.csv")


    fav_team = input("Input the full name of your team: (ex: Golden State Warriors) ")
    while (True):
        if (len(teams[teams['full_name'] == fav_team]) == 1):
            break
        fav_team = input("Inputted name not found, please try again: (ex: Golden State Warriors) ")

    favteamid = datautils.getteamid(teams, fav_team)
    
    opteams = []
    print("Now input one at a time the full names of teams your team will play at home. ")
    while (True):
        op = input("Input the full name of the opposing team or if done enter 'Done' ")
        if op == "Done":
            break
        elif (len(teams[teams['full_name'] == op]) != 1):
            print("Inputted name not found, please try again: (ex: Golden State Warriors) ")
            continue
        else:
            opteams = np.append(opteams, op)
    input("Press enter to continue. ")
    print("Now predicting which of those teams your favorite team is most likely to beat. This will take awhile. ")


    season = datautils.whatseason()


    games_lastseason = datautils.edit_gamescsv(games, season - 1)
    games_thisseason = datautils.edit_gamescsv(games, season)
    games_twoseasonsago = datautils.edit_gamescsv(games, season - 2)
    df_thisseason = datatable.get_table(season, teams, games_thisseason)
    x_predict = datatable.make_testTable(opteams, favteamid, df_thisseason, teams, games_lastseason, lst)

    df_lastseason = datatable.get_table(season - 1, teams, games_lastseason)

    df_twoseasonago = datatable.get_table(season - 2, teams, games_twoseasonsago)
    frames = [df_lastseason, df_twoseasonago]
    df = pd.concat(frames)


    proba = datautils.get_proba(df, x_predict, lst)

    max_team = None
    max_p = 0
    for p in range(len(proba)):
        if proba[p] > max_p:
            max_p = proba[p]
            max_team = opteams[p]
    max_p = np.round(max_p, 2)
    print("The " + fav_team + " are most likely to beat the " + max_team + " with a probability of " + str(max_p))


main()


