from DataAcquisition import *
from DataCleaning import *
from MongoStats import*

def main():

    year1 = int(input("Enter first year for Batting Stat Acquisition:\n"))
    year2 = int(input("Enter last year for Batting Stat Acquisition:\n"))
    year_list = Make_Year_List(year1,year2)

    string_years = str(year1) + 'to' + str(year2)

    url_df = Make_URL_List(year_list)
    batting_df = Get_Season_Batting_Stats(url_df)
    Make_Master_CSV(year_list, batting_df,'raw_batter'+string_years+'.csv')



    clean_list = Full_Clean(year_list, batting_df)
    Make_Clean_Files(year_list, clean_list,'clean_batter'+string_years)



    stats = LoadMongo()
    CreateDB(stats)

    yearly_stats = ExportDF(stats)
    yearly_stats.to_csv('StatsByYear.csv', index=False)
    modelDF = FiftyABClub(stats)
    modelDF.to_csv('modelDF.csv', index=False)


main()
