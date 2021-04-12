from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv, dotenv_values
import os
import Summoner

# API Rate Limits:
# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)


def init():

    summoner = Summoner.Summoner(os.getenv("PREDLOL_SUMMONER_NAME"))

    try:
        summoner_name = summoner.watcher.summoner.by_name(
            summoner.lol_region, summoner.name)
        print(summoner_name)
    except ApiError as err:
        if err.response.status_code == 429:
            print('Please retry in {} seconds.'.format(
                err.response.headers['Retry-After']))
            print('This retry-after is handled by default by the RiotWatcher library.')
            print('Future requests wait until the retry-after time passes.')
        elif err.response.status_code == 404:
            print('Summoner not found.')
        else:
            raise

    match_list = summoner.matches['matches']
    print(len(match_list))
    print(match_list)

    # Note: This API request returns the last ~100 matches and can therefore only be executed once every 2 minutes
    summoner.get_matches()

    # print(
    #     f'Total gametime over the last {len(match_list)} games: {round(summoner.get_total_hours(), 2)}')

    # summoner.get_participants()
    # summoner.get_weekday_performance()

# core logic:

# summoner class

# summoner.calc_total_hours()
# summoner.analyse_xxxxxxx()

# additional class with statistical analysis functions

#   1. game modes WL rate
#   2. analyse and predict W/L per weekday


def main():
    load_dotenv()
    # print(os.getenv("PREDLOL_SUMMONER_NAME"))

    # config = dotenv_values(".env")
    # print(config)
    init()


if __name__ == '__main__':
    main()
