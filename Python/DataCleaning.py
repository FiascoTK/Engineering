import pandas as pd
import numpy as np
import os.path



def Add_Year(year, master_list):

        master_list['Year'] = year

        return None

def Drop_Season_Summary(master_list):
    master_list = master_list.iloc[:-1, :]

    return master_list

def Clean_Name(master_list):
    count = 0
    for name in master_list['Name']:
        if name[-1] == '#' or name[-1] == '*' or name[-1] == '?':
            master_list['Name'][count] = name[:-1]
        count += 1

    return None

def Fill_Missing(master_list):

    return master_list.fillna(0,inplace=True)

def String_to_Num(master_list):
    for col in master_list:
        master_list[col] = pd.to_numeric(master_list[col], errors='ignore')

    return master_list

def Drop_Cols(master_list):
    # drop Rk column
    master_list.drop(['Rk'], axis=1, inplace=True)

    return None

def Drop_Rows(master_list):
    # drop rows that have 'TOT' for team to avoid double counting
    master_list = master_list[master_list['Tm'] != 'TOT']

    return master_list


def Full_Clean(year_list, batting_df):
    for i in year_list:
        Add_Year(i, batting_df)
        batting_df[i] = Drop_Season_Summary(batting_df[i])
        Clean_Name(batting_df[i])
        batting_df[i] = String_to_Num(batting_df[i])
        Fill_Missing(batting_df[i])
        Drop_Cols(batting_df[i])
        batting_df[i] = Drop_Rows(batting_df[i])

    return batting_df

def Make_Clean_Files(year_list, batting_df, file_name):
    clean_list = pd.DataFrame()

    for i in year_list:
        batting_df[i].to_csv(os.path.join('Years',i+'.csv'), index=False)
        clean_list = clean_list.append(batting_df[i], ignore_index=True)

    clean_list.to_csv(file_name+'.csv', index=False)
    # clean_list.to_json(file_name+'.json')

    return None
