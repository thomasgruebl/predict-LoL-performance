from riotwatcher import LolWatcher, ApiError
import constants

from multiprocessing import Pool
import os
import time


class Summoner(object):
    api_key = constants.GET_API_KEY()
    lol_region = constants.GET_REGION()
    watcher = LolWatcher(api_key)

    def __init__(self, name):
        self.name = name
        self.profile = self.watcher.summoner.by_name(self.lol_region, name)
        self.matches = self.watcher.match.matchlist_by_account(self.lol_region, self.profile['accountId'], begin_time=0)
        self.matches_detail = []

    def _get_match_details(self, game_id):
        print(game_id)
        time.sleep(os.cpu_count()/20)
        return self.watcher.match.by_id(self.lol_region, game_id)

    def get_matches(self):
        game_ids = list()
        game_ids = [match['gameId'] for match in self.matches['matches']]
        print(game_ids)
        game_ids = game_ids[:95]

        pool_offset = Pool(os.cpu_count())
        try:
            match_details = pool_offset.map(self._get_match_details, game_ids)
        finally:
            pool_offset.close()
            pool_offset.join()

        print(match_details)
        self.matches_detail = match_details

    def get_total_hours(self):
        total_hours = 0
        for match in self.matches_detail:
            total_hours += int(match['gameDuration']) / 3600
        return total_hours

    def get_weekdays(self):
        for match in self.matches_detail:
            unixtime = constants.unixtime_extract_day(int(match['gameCreation']) / 1000)
            print(unixtime)
