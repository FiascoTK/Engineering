import pandas as pd
import os.path
from pymongo import MongoClient
from pprint import pprint


def LoadMongo():
    client = MongoClient()
    batters = client.batters
    stats = batters.stats
    return stats

def CreateDB(stats):
    stats.drop()
    stat_files = os.listdir('Years')

    for i in stat_files:
        df = pd.read_csv('Years/'+ i)
        stats.insert_many(df.to_dict('records'))


def StatsByYear(my_stat, stats):
    agg_stat = '$' + my_stat
    StatsPerYear = list(stats.aggregate([
                    {'$group' : {'_id': '$Year', my_stat: {'$sum':agg_stat}}},
                    {'$sort':{'_id': 1}}
                    ]))
    StatDF = pd.DataFrame(StatsPerYear)
    StatDF.rename(columns={'_id': 'Year'}, inplace=True)

    return StatDF

'''
def AvgAge(stats):
    DistinctPlayers = stats.aggregate([
                        {$group::{'_id':{Year: '$Year', Name: '$Name', Age: '$Age'}}}
                        ]
                    )

    TotalAgePerYear = list(YearPlayerAge.aggregate([
                            {'$group' : {'_id': '$Year', Age: {'$sum':'$Age'}}},
                            {'$sort':{'_id': 1}}
                            ]
                    ))
'''
'''
# of players with greater than 20 HRs by Year


def TwentyHRClub(stats):
    twenty_club = stats.find({'HR': {'$gte': 20}},{'HR':1, 'Year'})
    twenty_club_count = list(twenty_club.aggregate([
                        {'$group':{'_id':'Year', 'count':{'$sum:1'}}},
                    ]))
    return twenty_club_count
'''

def ExportDF(stats):
    paDF = StatsByYear('PA', stats)
    paDF['HR'] = StatsByYear('HR', stats)['HR']
    paDF['H'] = StatsByYear('H', stats)['H']
    paDF['BB'] = StatsByYear('BB', stats)['BB']
    paDF['SO'] = StatsByYear('SO', stats)['SO']
    paDF['HBP'] = StatsByYear('HBP', stats)['HBP']
    paDF['Home Runs per 600 Plate Appearances'] = (paDF['HR'] * 600)/ paDF['PA']
    paDF['Hits per 600 Plate Appearances'] = (paDF['H'] * 600)/ paDF['PA']
    paDF['Strike Outs per 600 Plate Appearances'] = (paDF['SO'] * 600)/ paDF['PA']
    paDF['On Base Percentage'] = ((paDF['H'] + paDF['BB'] + paDF['HBP'])/paDF['PA'])


    paDF.rename(columns={'HR': 'Home Runs'}, inplace=True)
    paDF.rename(columns={'H': 'Hits'}, inplace=True)
    paDF.rename(columns={'BB': 'Walks'}, inplace=True)
    paDF.rename(columns={'SO': 'Strike Outs'}, inplace=True)
    paDF.rename(columns={'HBP': 'Hit by Pitch'}, inplace=True)
    return paDF


def FiftyABClub(stats):
    club = stats.find({'PA': {'$gte': 50}},{'HR':1, 'PA':1, 'R':1, 'H':1, '2B':1, 'RBI':1, 'BB':1, 'SO':1})
    LRdf = pd.DataFrame(list(club))
    LRdf.rename(columns={'2B': 'Db'}, inplace=True)
    LRdf.drop(['_id'], axis=1, inplace=True)
    return LRdf
