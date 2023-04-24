# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:24:57 2023

@author: Graduate
"""

from stat_funcs import player_stats, team_stats, league_stats_team, league_stats_opponent

df_3 = league_stats_team()
df_4 = league_stats_opponent()

def player_search(player_name):
    df = player_stats(player_name)
    df_2 = team_stats(df)
    #percentiles = per_36_stats(player_name)
    
    opp_ft = int(df_2.loc['Opponent']['FT'])
    team_fouls = int(df_2.loc['Team']['PF'])
    min_played = int(df_2.loc['Team']['MP'])
    team_blocks = int(df_2.loc['Team']['AST'])
    team_assists = int(df_2.loc['Team']['BLK'])
    
    
    prod = round(float(df.loc['3P'])*0.064 + float(df.loc['2P'])*0.032 + float(df.loc['FT'])*0.017 + (float(df.loc['FGA']) - float(df.loc['FG']))*-0.032 + (float(df.loc['FTA']) - float(df.loc['FT']))*-0.017 + float(df.loc['DRB'])*0.033 + float(df.loc['ORB'])*0.032 + float(df.loc['TOV'])*-0.032 + float(df.loc['STL'])*0.033 + (float(df.loc['PF']) / team_fouls * opp_ft)*-0.017 + float(df.loc['BLK'])*0.019 + float(df.loc['AST'])*0.022, 2)
    p48_val_blk_ast = (team_blocks*0.019 + team_assists*0.022) / min_played * 48
    p48_val_blk_ast_league = (float(df_3['BLK'].mean())*0.019 + float(df_3['AST'].mean()*0.022)) / min_played * 48
    mate_48 = p48_val_blk_ast - p48_val_blk_ast_league
    
    player_p48 = (prod / int(df.loc['MP']) * 48) - mate_48
    
    team_defense = (int(df_2.loc['Opponent']['2P'])*-0.032 + int(df_2.loc['Opponent']['3P'])*-0.064 + int(df_2.loc['Opponent']['TOV'])*0.033 + int(df_2.loc['Team']['TOV'])*-0.032 + int(df_2.loc['Team']['TRB'])*0.033) / min_played *48
    league_defense = (float(df_4['2P'].mean())*-0.032 + float(df_4['3P'].mean())*-0.064 + float(df_4['TOV'].mean())*0.033 + float(df_3['TOV'].mean())*-0.032 + float(df_3['TRB'].mean())*0.033) / min_played *48
    deftm48 = league_defense - team_defense
    
    player_adj_p48 = player_p48 - deftm48
    
    pos_avg = 0
    if df.loc['Pos'] == 'PG' or df.loc['Pos'] == 'SG':
        pos_avg = 0.36
    elif df.loc['Pos'] == 'C' or df.loc['Pos'] == 'PF':
        pos_avg = 0.31
    else:
        pos_avg = 0.33
        
    player_rel_adj_p48 = player_adj_p48 - pos_avg
    wp48 = player_rel_adj_p48 + 0.099
    wp = wp48 / 48 * float(df.loc['MP'])
    wp = round(wp, 2)
    
    return wp
    