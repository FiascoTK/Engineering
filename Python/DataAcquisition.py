import requests, bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import re, os
from time import sleep


# findTables and pullTable were borrowed from
# https://github.com/BenKite/baseball_data/blob/master/baseballReferenceScrape.py

def findTables(url):
    res = requests.get(url)
    ## comments break parsing.  Next 2 comments fix that
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)

    return(ids)

def pullTable(url, tableID):
    res = requests.get(url)
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text))
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    data_header = tables[0].findAll('thead')
    data_header = data_header[0].findAll("tr")
    data_header = data_header[0].findAll("th")
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    header = []
    for i in range(len(data.columns)):
        header.append(data_header[i].getText())
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)

    return(data)

def Get_Season_Batting_Stats(batter_df):
    df_dict={}
    for i in range(0, len(batter_df)):
        url = batter_df['URL'][i]
        batter_data = pullTable(url, "players_standard_batting")
        sleep(3)
        df_dict[batter_df['Year'][i]] = batter_data

    return df_dict


def Make_Year_List(first_year, last_year):
    years = list(range(first_year,last_year + 1))
    years = [str(x) for x in years]

    return years

def Make_URL_List(years):
    urls = []
    for i in years:
        urls.append('https://www.baseball-reference.com/leagues/majors/' + i +'-standard-batting.shtml')

    year_dic = {'Year': years, 'URL': urls}
    url_df = pd.DataFrame(data=year_dic)

    return url_df

def Make_Master_CSV(year_list, batting_df, file_name):
    master_list = pd.DataFrame()

    for i in year_list:
        batting_df[i] = batting_df[i].iloc[:-1, :]
        batting_df[i]['Year'] = i
        master_list = master_list.append(batting_df[i], ignore_index=True)

    master_list.to_csv(file_name)

    return None
