import numpy as np
from itertools import combinations
import pandas as pd


def make_testTable(oppteams, favteamid, ogdf, teams, gameslastseason, lst):
    oppteamids = []

    for ot in oppteams:
        o = teams[teams['full_name'] == ot].iloc[0]['id']
        oppteamids = np.append(oppteamids, o)

    home_team_col = []
    away_team_col = []
    home_total_record_so_far_col = []
    away_total_record_so_far_col = []
    home_wins_ratio_so_far_col = []
    # winner_col = []
    awayRecordAgainstTeamsHomeBeatSoFar_col = []
    homeRecordAgainstTeamsAwayBeatSoFar_col = []
    diffTeamsAvgPPG_col = []
    home_record_home_col = []
    awayRecAtAway_col = []
        
    favteam_recent_row = ogdf[ogdf['home id'] == 1610612744]
    favteam_recent_row = favteam_recent_row.iloc[-1]
    home_record = favteam_recent_row["home total record so far"]
    home_record_home = favteam_recent_row["home record home"]
    for o in oppteamids:
        home_team_col = np.append(home_team_col, favteamid)
        away_team_col = np.append(away_team_col, o)

        home_total_record_so_far_col = np.append(home_total_record_so_far_col, home_record)
        home_record_home_col = np.append(home_record_home_col, home_record_home)
        
        oppteam_recent_row = ogdf[((ogdf['home id'] == o) | (ogdf['away id'] == o))].iloc[-1]

        i = len(gameslastseason)
            
        if oppteam_recent_row["home id"] == o:
            away_total_record_so_far = oppteam_recent_row["home total record so far"]
            awayRecAtAway = oppteam_recent_row["home record home"]
            home_record_against_teams_away_beat = recordAgainstTeamsOppBeatSoFar(gameslastseason, i, favteamid, oppteam_recent_row["home id"])
            away_record_against_teams_home_beat = recordAgainstTeamsOppBeatSoFar(gameslastseason, i, oppteam_recent_row["home id"], favteamid)
            home_wins_ratio_so_far_col = np.append(home_wins_ratio_so_far_col, recagainstotherteam(2022, i, favteamid, o, teams, gameslastseason))

        else:
            away_total_record_so_far = oppteam_recent_row["away total record so far"]
            awayRecAtAway = oppteam_recent_row["away record away"]
            home_record_against_teams_away_beat = recordAgainstTeamsOppBeatSoFar(gameslastseason, i, favteamid, oppteam_recent_row["away id"])
            away_record_against_teams_home_beat = recordAgainstTeamsOppBeatSoFar(gameslastseason, i, oppteam_recent_row["away id"], favteamid)
            home_wins_ratio_so_far_col = np.append(home_wins_ratio_so_far_col, recagainstotherteam(2022, i, favteamid, oppteam_recent_row["away id"], teams, gameslastseason))
        awayRecAtAway_col = np.append(awayRecAtAway_col, awayRecAtAway)
        away_total_record_so_far_col = np.append(away_total_record_so_far_col, away_total_record_so_far)
        homeRecordAgainstTeamsAwayBeatSoFar_col = np.append(homeRecordAgainstTeamsAwayBeatSoFar_col, home_record_against_teams_away_beat)
        awayRecordAgainstTeamsHomeBeatSoFar_col = np.append(awayRecordAgainstTeamsHomeBeatSoFar_col, away_record_against_teams_home_beat)

        diffteamsavgppg = diffTeamsAvgPPG(gameslastseason, favteamid, o, i)
        diffTeamsAvgPPG_col = np.append(diffTeamsAvgPPG_col, diffteamsavgppg)
    
    d = {'home id' : home_team_col, 'away id' : away_team_col, 
         'home total record so far' : home_total_record_so_far_col, 'away total record so far' : away_total_record_so_far_col,
         'home wins over away so far' : home_wins_ratio_so_far_col,  'away record against teams home beat' : awayRecordAgainstTeamsHomeBeatSoFar_col, 
         'home record against teams away beat' : homeRecordAgainstTeamsAwayBeatSoFar_col, 
         'avg PPG diff' : diffTeamsAvgPPG_col, 'away record away' : awayRecAtAway_col, 
         'home record home' : home_record_home_col}
    
    
    tbl = pd.DataFrame(data=d)
    return tbl[lst]



def get_total_records(numgames, teamid, gamestbl):
    
    # temp_games = gamestbl[gamestbl['season_id'] >= 20000 + start_season]
    temp_games = gamestbl.iloc[0:numgames]
    games_home = temp_games[temp_games['team_id_home'] == teamid]
    games_away = temp_games[temp_games['team_id_away'] == teamid]

    wins = len(games_home[games_home['wl_home'] == 'W'])
    wins += len(games_away[games_away['wl_away'] == 'W'])

    losses = len(games_home[games_home['wl_home'] == 'L'])
    losses += len(games_away[games_away['wl_away'] == 'L'])

    if (wins + losses == 0):
        return 0
    else:
        return wins/(wins + losses)


def recagainstotherteams(start_season, end_season, fav_team, teamstbl, gamestbl):
    records = []
    team_ids = teamstbl['id']
    temp = teamstbl[teamstbl['full_name'] == fav_team]
    fav_team_id = temp.iloc[0]['id']
    for x in team_ids:
        if x == fav_team_id:
            records = np.append(records, "NA")
            continue
        temp_games = gamestbl[gamestbl['season_id'] == 20000 + season]
        games_away = temp_games[temp_games['team_id_home'] == x]
        games_away = games_away[games_away['team_id_away'] == fav_team_id]
        games_home = temp_games[temp_games['team_id_away'] == x]
        games_home = games_home[games_home['team_id_home'] == fav_team_id]
        
        wins = len(games_home[games_home['wl_home'] == 'W'])
        wins += len(games_away[games_away['wl_away'] == 'W'])

        losses = len(games_home[games_home['wl_home'] == 'L'])
        losses += len(games_away[games_away['wl_away'] == 'L'])
        
        total = wins + losses
        if total == 0:
            records = np.append(records, "NA")
        else:
            records = np.append(records, (wins/total))
    return records

def recagainstotherteam(start_season, numberofgames, home_team, away_team, teamstbl, gameslastseason):
    records = []
    gameslastseason = gameslastseason.iloc[0:numberofgames]

    games_away = gameslastseason[gameslastseason['team_id_home'] == away_team]
    games_away = games_away[games_away['team_id_away'] == home_team]
    games_home = gameslastseason[gameslastseason['team_id_away'] == away_team]
    games_home = games_home[games_home['team_id_home'] == home_team]

    wins = len(games_home[games_home['wl_home'] == 'W'])
    wins += len(games_away[games_away['wl_away'] == 'W'])

    losses = len(games_home[games_home['wl_home'] == 'L'])
    losses += len(games_away[games_away['wl_away'] == 'L'])
    
    return wins

def recentRecord(teamid, gameslastseason, numberofgames):
    temp_games = gameslastseason.iloc[0:numberofgames]
    temp_games = temp_games[(temp_games['team_id_home'] == teamid) | (temp_games['team_id_away'] == teamid)]
    if len(temp_games) < 10:
        temp_games = temp_games.iloc[0:numberofgames]
    else:
        temp_games = temp_games.iloc[-10:]
    wins = len(temp_games[temp_games['wl_home'] == 'W'])
    losses = len(temp_games[temp_games['wl_home'] == 'L'])
    if (wins + losses == 0):
        return 0
    else:
        return wins/(wins + losses)

def recordAgainstTeamsOppBeatSoFar(gameslastseason, numberofgames, fav_teamid, op_teamid):
    gameslastseason = gameslastseason.iloc[0:numberofgames]
    teamsoppbeat = gameslastseason[
        (
            (gameslastseason['team_id_home'] == op_teamid)
            & (gameslastseason['wl_home'] == 'W')
        )
        | (
            (gameslastseason['team_id_away'] == op_teamid)
            & (gameslastseason['wl_away'] == 'W')
        )
    ]
    teamsoppbeattemp = teamsoppbeat['team_id_home'].tolist()
    teamsoppbeattemp = np.append(teamsoppbeattemp, teamsoppbeat['team_id_away'].tolist())
    teamsoppbeattemp = list(set(teamsoppbeattemp))
    games_home = gameslastseason[
        (
            gameslastseason['team_id_home'] == fav_teamid
        )
        & (
            gameslastseason['team_id_away'].isin(teamsoppbeattemp) == True
        )
    ]
    games_away = gameslastseason[
        (
            gameslastseason['team_id_away'] == fav_teamid
        )
        & (
            gameslastseason['team_id_home'].isin(teamsoppbeattemp) == True
        )
    ]
        
    wins = len(games_home[games_home['wl_home'] == 'W'])
    wins += len(games_away[games_away['wl_away'] == 'W'])

    losses = len(games_home[games_home['wl_home'] == 'L'])
    losses += len(games_away[games_away['wl_away'] == 'L'])
    
    if (wins + losses == 0):
        return 0
    else:
        return wins/(wins + losses)
    
def daysOfRest(gameslastseason, numberofgames, favteamid):
    if (numberofgames < 4):
        return 3
    gameslastseasontemp = gameslastseason.iloc[0:numberofgames]
    cur = gameslastseasontemp["game_date"].tolist()
    cur = cur[numberofgames - 1][5:10]
    cur_month = int(cur[0:2])
    cur_day = int(cur[3:5])
    dates = gameslastseasontemp["game_date"].tolist()
    i = numberofgames - 2
    days_passed = 0

    while (i > 1):
        this = gameslastseasontemp["game_date"].tolist()[i][5:10]

        this_month = int(this[0:2])
        this_day = int(this[3:5])
        if this_day != cur_day:
            days_passed += 1
            cur_day = this_day
        if gameslastseasontemp.iloc[i]['team_id_home'] == favteamid:
            return days_passed
        if gameslastseasontemp.iloc[i]['team_id_away'] == favteamid:
            return days_passed
        i = i - 1
    return 3

def diffTeamsAvgPPG(gameslastseason, one, two, numgames):
    tblgames = gameslastseason.iloc[0:numgames]

    one_home = gameslastseason[gameslastseason['team_id_home'] == one]
    one_away = gameslastseason[gameslastseason['team_id_away'] == one]
    two_home = gameslastseason[gameslastseason['team_id_home'] == two]
    two_away = gameslastseason[gameslastseason['team_id_away'] == two]
    
    points_one = sum(one_home['pts_home'].tolist())
    points_one += sum(one_home['pts_away'].tolist())
    avg_pts_one = points_one / (len(one_home['pts_home'].tolist()) + len(one_away['pts_home'].tolist()))
    
    points_two = sum(two_home['pts_home'].tolist())
    points_two += sum(two_home['pts_away'].tolist())
    avg_pts_two = points_two / (len(two_home['pts_home'].tolist()) + len(two_away['pts_home'].tolist())) 
    
    return avg_pts_one - avg_pts_two

def recordAtHome(gameslastseason, numberofgames, teamid):
    gameslastseason = gameslastseason.iloc[0:numberofgames]
    games_home = gameslastseason[gameslastseason['team_id_home'] == teamid]
    wins = len(games_home[games_home['wl_home'] == 'W'])
    losses = len(games_home[games_home['wl_home'] == 'L'])    
    if wins + losses == 0:
        return 0
    else:
        return wins / (wins + losses)

def recordAtAway(gameslastseason, numberofgames, teamid):
    gameslastseason = gameslastseason.iloc[0:numberofgames]
    games_away = gameslastseason[gameslastseason['team_id_away'] == teamid]
    wins = len(games_away[games_away['wl_away'] == 'W'])
    losses = len(games_away[games_away['wl_away'] == 'L'])    
    if wins + losses == 0:
        return 0
    else:
        return wins / (wins + losses)


def get_table(last_season, teamstbl, gameslastseason):
    # recagainstotherteams = recagainstotherteams(last_season, fav_team, teams, games)
    
    num_games = len(gameslastseason)
    home_team_col = gameslastseason["team_id_home"].tolist()
    away_team_col = gameslastseason["team_id_away"].tolist()
    home_total_record_so_far_col = []
    away_total_record_so_far_col = []
    home_wins_ratio_so_far_col = []
    winner_col = []
    awayRecordAgainstTeamsHomeBeatSoFar_col = []
    homeRecordAgainstTeamsAwayBeatSoFar_col = []
    awayRecentRecord_col = []
    homeRecentRecord_col = []
    daysRestHome_col = []
    daysRestAway_col = []
    daysRestDiff_col = []
    diffTeamsAvgPPG_col = []
    homeRecAtHome_col = []
    awayRecAtAway_col = []
    for i in range(num_games):
        home_record = get_total_records(i, home_team_col[i], gameslastseason)
        home_total_record_so_far_col = np.append(home_total_record_so_far_col, home_record)
        away_record = get_total_records(i, away_team_col[i], gameslastseason)
        away_total_record_so_far_col = np.append(away_total_record_so_far_col, away_record)
        home_wins_ratio_so_far_col = np.append(home_wins_ratio_so_far_col, recagainstotherteam(2021, i, home_team_col[i], away_team_col[i], teamstbl, gameslastseason))
        away_recordAgainstHomesWins = recordAgainstTeamsOppBeatSoFar(gameslastseason, i, away_team_col[i], home_team_col[i])
        home_recordAgainstAwayWins = recordAgainstTeamsOppBeatSoFar(gameslastseason, i, home_team_col[i], away_team_col[i])
        awayRecordAgainstTeamsHomeBeatSoFar_col = np.append(awayRecordAgainstTeamsHomeBeatSoFar_col, away_recordAgainstHomesWins)
        homeRecordAgainstTeamsAwayBeatSoFar_col = np.append(homeRecordAgainstTeamsAwayBeatSoFar_col, home_recordAgainstAwayWins)
        away_recentRecord = recentRecord(away_team_col[i], gameslastseason, i)
        home_recentRecord = recentRecord(home_team_col[i], gameslastseason, i)
        awayRecentRecord_col = np.append(awayRecentRecord_col, away_recentRecord)
        homeRecentRecord_col = np.append(homeRecentRecord_col, home_recentRecord)
        daysRestHome = daysOfRest(gameslastseason, i, home_team_col[i])
        daysRestAway = daysOfRest(gameslastseason, i, away_team_col[i])
        daysRestHome_col = np.append(daysRestHome_col, daysRestHome)
        daysRestAway_col = np.append(daysRestAway_col, daysRestAway)
        daysRestDiff_col = np.append(daysRestDiff_col, daysRestHome - daysRestAway)
        teamsAvgPPG = diffTeamsAvgPPG(gameslastseason, home_team_col[i], away_team_col[i], i)
        diffTeamsAvgPPG_col = np.append(diffTeamsAvgPPG_col, teamsAvgPPG)
        homeRecAtHome = recordAtHome(gameslastseason, i, home_team_col[i])
        awayRecAtAway = recordAtAway(gameslastseason, i, away_team_col[i])
        homeRecAtHome_col = np.append(homeRecAtHome_col, homeRecAtHome)
        awayRecAtAway_col = np.append(awayRecAtAway_col, awayRecAtAway)
        if (gameslastseason.iloc[i]['wl_home'] == "W"):
            winner_col = np.append(winner_col, 1)
        else:
            winner_col = np.append(winner_col, 0)
    d = {'home id' : home_team_col, 'winner' : winner_col, 'away id' : away_team_col, 
         'home total record so far' : home_total_record_so_far_col, 'away total record so far' : away_total_record_so_far_col,
         'home wins over away so far' : home_wins_ratio_so_far_col,  'away record against teams home beat' : awayRecordAgainstTeamsHomeBeatSoFar_col, 
         'home record against teams away beat' : homeRecordAgainstTeamsAwayBeatSoFar_col, 'away recent record' : awayRecentRecord_col, 
         'home recent record' : homeRecentRecord_col, "days rest home" : daysRestHome_col, "days rest away" : daysRestAway_col, 
         'avg PPG diff' : diffTeamsAvgPPG_col, 'days rest diff' : daysRestDiff_col, 'away record away' : awayRecAtAway_col, 
         'home record home' : homeRecAtHome_col}
    
    
    tbl = pd.DataFrame(data=d)
    return tbl

