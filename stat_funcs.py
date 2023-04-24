# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 12:43:48 2023

@author: Graduate
"""
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
from unidecode import unidecode

def get_player_url(player_name):
    search_url = "https://www.basketball-reference.com/search/search.fcgi"
    params = {"search": player_name}

    response = requests.get(search_url, params=params)
    current_url = response.url
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    content_div = soup.find("div", {"id": "content"})
    search_results_div = content_div.find("div", {"class": "search-results"})
    if search_results_div is None:
        url = current_url
    else:
        searches_div = search_results_div.find("div", {"id": "searches"})

        player_url = searches_div.find("div", {"class": "search-item-url"}).text.strip()
        url = 'https://www.basketball-reference.com/' + player_url
    
    return url


def player_stats(player_name):
    player_name = player_name.lower()
    player_url = get_player_url(player_name)
    
    r = requests.get(player_url)
        
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')

    stats_table = soup.find('table', {'id': 'totals'})
    header_row = stats_table.find('thead').find('tr')

    headers = []
    for th in header_row.findAll('th'):
        headers.append(th.text)

    data_rows = stats_table.findAll('tbody')[0].findAll('tr')

    data = []
    for row in data_rows:
        row_data = []
        season = row.find('th').text
        row_data.append(season)
        for cell in row.findAll('td'):
            row_data.append(cell.text)
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    df = df.loc[df.index[-1]]
    return df




def team_stats(df):
    team_url = f'https://www.basketball-reference.com/teams/{df.loc["Tm"]}/2023.html'
    r = requests.get(team_url)
    html_content = r.text

    soup = BeautifulSoup(html_content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    tables = []
    for each in comments:
        if 'table' in str(each):
            try:
                tables.append(pd.read_html(each, attrs = {'id': 'team_and_opponent'}, header=0)[0])
            except:
                continue
    df_2 = pd.DataFrame(tables[0])
    df_2.set_index('Unnamed: 0', inplace=True)
    df_2 = df_2.iloc[[0, 4]]
    df_2 = df_2.astype(float)
    return df_2

def league_stats_team():
    season_url = 'https://www.basketball-reference.com/leagues/NBA_2023.html'

    r = requests.get(season_url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')

    stats_table = soup.find('table', {'id': 'totals-team'})
    header_row = stats_table.find('thead').find('tr')

    headers = []
    for th in header_row.findAll('th'):
        headers.append(th.text)

    data_rows = stats_table.findAll('tbody')[0].findAll('tr')

    data = []
    for row in data_rows:
        row_data = []
        season = row.find('th').text
        row_data.append(season)
        for cell in row.findAll('td'):
            row_data.append(cell.text)
        data.append(row_data)

    df_3 = pd.DataFrame(data, columns=headers)
    df_3.iloc[:, 2:] = df_3.iloc[:, 2:].astype(float)
    return df_3



def league_stats_opponent():
    season_url = 'https://www.basketball-reference.com/leagues/NBA_2023.html'

    r = requests.get(season_url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')

    stats_table = soup.find('table', {'id': 'totals-opponent'})
    header_row = stats_table.find('thead').find('tr')

    headers = []
    for th in header_row.findAll('th'):
        headers.append(th.text)

    data_rows = stats_table.findAll('tbody')[0].findAll('tr')

    data = []
    for row in data_rows:
        row_data = []
        season = row.find('th').text
        row_data.append(season)
        for cell in row.findAll('td'):
            row_data.append(cell.text)
        data.append(row_data)

    df_4 = pd.DataFrame(data, columns=headers)
    df_4.iloc[:, 2:] = df_4.iloc[:, 2:].astype(float)

    return df_4



def per_36_stats(player_name):
    stats = player_stats(player_name)
    position = str(stats.loc['Pos'])
    team_url = 'https://www.basketball-reference.com/leagues/NBA_2023_per_minute.html'

    r = requests.get(team_url)
    html_content = r.text

    soup = BeautifulSoup(html_content, 'html.parser')

    stats_table = soup.find('table', {'id': 'per_minute_stats'})

    header_row = stats_table.find('thead').find('tr')

    headers = []
    for th in header_row.findAll('th'):
        headers.append(th.text)

    data_rows = stats_table.findAll('tbody')[0].findAll('tr')

    data = []
    for row in data_rows:
        row_data = []
        season = row.find('th').text
        row_data.append(season)
        for cell in row.findAll('td'):
            row_data.append(cell.text)
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    df = df[df['Rk'] != 'Rk']
    df['Pos'] = df['Pos'].str.slice(stop=2).replace('-', '')
    df = df[df['Pos'] == position]
    df = df.drop_duplicates(subset=['Player'])
    df['Player'] = df['Player'].apply(lambda x: unidecode(x).replace('.', '').replace("'", "").lower())
    df = df.replace('', 0.0)

    df.iloc[:, 5:] = df.iloc[:, 5:].astype(float)
    #df = df[df['MP'] > 200]

    pts_sorted = df.sort_values(by='PTS', ascending=False).reset_index()
    fg_sorted = df.sort_values(by='FG', ascending=False).reset_index()
    fga_sorted = df.sort_values(by='FGA', ascending=False).reset_index()
    fgp_sorted = df.sort_values(by='FG%', ascending=False).reset_index()
    threep_sorted = df.sort_values(by='3P', ascending=False).reset_index()
    threepa_sorted = df.sort_values(by='3PA', ascending=False).reset_index()
    threepp_sorted = df.sort_values(by='3P%', ascending=False).reset_index()
    twop_sorted = df.sort_values(by='2P', ascending=False).reset_index()
    twopa_sorted = df.sort_values(by='2PA', ascending=False).reset_index()
    twopp_sorted = df.sort_values(by='2P%', ascending=False).reset_index()
    ft_sorted = df.sort_values(by='FT', ascending=False).reset_index()
    fta_sorted = df.sort_values(by='FTA', ascending=False).reset_index()
    ftp_sorted = df.sort_values(by='FT%', ascending=False).reset_index()
    orb_sorted = df.sort_values(by='ORB', ascending=False).reset_index()
    drb_sorted = df.sort_values(by='DRB', ascending=False).reset_index()
    trb_sorted = df.sort_values(by='TRB', ascending=False).reset_index()
    ast_sorted = df.sort_values(by='AST', ascending=False).reset_index()
    stl_sorted = df.sort_values(by='STL', ascending=False).reset_index()
    blk_sorted = df.sort_values(by='BLK', ascending=False).reset_index()
    tov_sorted = df.sort_values(by='TOV', ascending=False).reset_index()
    pf_sorted = df.sort_values(by='PF', ascending=False).reset_index()
    mp_sorted = df.sort_values(by='MP', ascending=False).reset_index()
    
    pts_index = pts_sorted.index[pts_sorted['Player'] == player_name][0]
    fg_index = fg_sorted.index[fg_sorted['Player'] == player_name][0]
    fga_index = fga_sorted.index[fga_sorted['Player'] == player_name][0]
    fgp_index = fgp_sorted.index[fgp_sorted['Player'] == player_name][0]
    threep_index = threep_sorted.index[threep_sorted['Player'] == player_name][0]
    threepa_index = threepa_sorted.index[threepa_sorted['Player'] == player_name][0]
    threepp_index = threepp_sorted.index[threepp_sorted['Player'] == player_name][0]
    twop_index = twop_sorted.index[twop_sorted['Player'] == player_name][0]
    twopa_index = twopa_sorted.index[twopa_sorted['Player'] == player_name][0]
    twopp_index = twopp_sorted.index[twopp_sorted['Player'] == player_name][0]
    ft_index = ft_sorted.index[ft_sorted['Player'] == player_name][0]
    fta_index = fta_sorted.index[fta_sorted['Player'] == player_name][0]
    ftp_index = ftp_sorted.index[ftp_sorted['Player'] == player_name][0]
    orb_index = orb_sorted.index[orb_sorted['Player'] == player_name][0]
    drb_index = drb_sorted.index[drb_sorted['Player'] == player_name][0]
    trb_index = trb_sorted.index[trb_sorted['Player'] == player_name][0]
    ast_index = ast_sorted.index[ast_sorted['Player'] == player_name][0]
    stl_index = stl_sorted.index[stl_sorted['Player'] == player_name][0]
    blk_index = blk_sorted.index[blk_sorted['Player'] == player_name][0]
    tov_index = tov_sorted.index[tov_sorted['Player'] == player_name][0]
    pf_index = pf_sorted.index[pf_sorted['Player'] == player_name][0]
    mp_index = mp_sorted.index[mp_sorted['Player'] == player_name][0]
    
    rows = df.shape[0]
    
    pts_percentile = int(((rows - pts_index) / rows) * 100)
    fg_percentile = int(((rows - fg_index) / rows) * 100)
    fga_percentile = int(((rows - fga_index) / rows) * 100)
    fgp_percentile = int(((rows - fgp_index) / rows) * 100)
    threep_percentile = int(((rows - threep_index) / rows) * 100)
    threepa_percentile = int(((rows - threepa_index) / rows) * 100)
    threepp_percentile = int(((rows - threepp_index) / rows) * 100)
    twop_percentile = int(((rows - twop_index) / rows) * 100)
    twopa_percentile = int(((rows - twopa_index) / rows) * 100)
    twopp_percentile = int(((rows - twopp_index) / rows) * 100)
    ft_percentile = int(((rows - ft_index) / rows) * 100)
    fta_percentile = int(((rows - fta_index) / rows) * 100)
    ftp_percentile = int(((rows - ftp_index) / rows) * 100)
    orb_percentile = int(((rows - orb_index) / rows) * 100)
    drb_percentile = int(((rows - drb_index) / rows) * 100)
    trb_percentile = int(((rows - trb_index) / rows) * 100)
    ast_percentile = int(((rows - ast_index) / rows) * 100)
    stl_percentile = int(((rows - stl_index) / rows) * 100)
    blk_percentile = int(((rows - blk_index) / rows) * 100)
    tov_percentile = int(((rows - tov_index) / rows) * 100)
    pf_percentile = int(((rows - pf_index) / rows) * 100)
    mp_percentile = int(((rows - mp_index) / rows) * 100)
    
    percentiles = [pts_percentile, fg_percentile, fga_percentile, fgp_percentile, threep_percentile, threepa_percentile, threepp_percentile, twop_percentile, twopa_percentile, twopp_percentile, ft_percentile, fta_percentile, ftp_percentile, orb_percentile, drb_percentile, trb_percentile, ast_percentile, stl_percentile, blk_percentile, tov_percentile, pf_percentile, mp_percentile]
    return percentiles
    