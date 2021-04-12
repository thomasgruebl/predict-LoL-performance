from riotwatcher import LolWatcher, ApiError
import constants

from multiprocessing import Pool
import matplotlib.pyplot as plt
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
        self.matches_detail = list()
        self.participants = list()

    def _get_match_details(self, game_id):
        print(game_id)
        time.sleep((os.cpu_count()/20) + 0.1)
        return self.watcher.match.by_id(self.lol_region, game_id)

    def _get_participant_id_from_summoner_name(self, d: dict):
        return list(d.keys())[list(d.values()).index(self.name)]

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

        print(match_details[0])
        self.matches_detail = match_details

    def get_participants(self):
        # Participant dictionary with participantId as key and summonerName as value
        participants_dict = dict.fromkeys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        for match in self.matches_detail:
            for i in range(0, 10):
                participants_dict[i+1] = match['participantIdentities'][i]['player']['summonerName']
            self.participants.append(participants_dict.copy())
            participants_dict.clear()
        print(self.participants)

        return self.participants

    def get_total_hours(self):
        total_hours = 0
        for match in self.matches_detail:
            total_hours += int(match['gameDuration']) / 3600
        return total_hours

    def get_weekday_performance(self):
        win_loss_per_weekday = dict.fromkeys(['Monday', 'Tuesday', 'Wednesday',
                                              'Thursday', 'Friday', 'Saturday', 'Sunday'])
        for k, v in win_loss_per_weekday.items():
            win_loss_per_weekday[k] = [0, 0]

        print("The dict looks like: ", win_loss_per_weekday)

        for idx, match in enumerate(self.matches_detail):
            weekday = constants.unixtime_extract_day(int(match['gameCreation']) / 1000)
            for i in range(0, 10):
                participant_id = self._get_participant_id_from_summoner_name(self.participants[idx])
                # print(f"Participant ID of match {idx} is {participantId}")
                if match['participants'][i]['participantId'] == participant_id:
                    # print(match['participants'][i]['participantId'])
                    # print(match['participants'][i]['stats']['win'])
                    if match['participants'][i]['stats']['win']:
                        win_loss_per_weekday[weekday][0] += 1
                    else:
                        win_loss_per_weekday[weekday][1] += 1

        print(win_loss_per_weekday)

        # Optional: plot weekday performance

        chart_labels = win_loss_per_weekday.keys()
        wins = [x[0] for x in win_loss_per_weekday.values()]
        losses = [x[1] for x in win_loss_per_weekday.values()]
        wins_percentage = [round(x / (x + y), 2) for x, y in zip(wins, losses)]
        losses_percentage = [round(x / (x + y), 2) for x, y in zip(losses, wins)]
        width = 0.35

        fig, ax = plt.subplots()
        ax.bar(chart_labels, wins_percentage, width, label='Wins')
        ax.bar(chart_labels, losses_percentage, width, bottom=wins_percentage, label='Losses')
        ax.set_ylabel('Percentage')
        ax.set_title('W/L percentage comparison per weekday')
        ax.legend()
        plt.show()

        return win_loss_per_weekday

    def predict_weekday_performance(self):
        # get_weekday_performance()
        pass
