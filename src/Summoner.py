import matplotlib.pyplot as plt
from datetime import datetime


class Summoner(object):

    def __init__(self, name, profile, match_list, match_data):
        self.name = name
        self.profile = profile
        self.match_list = match_list
        self.match_data = match_data
        self.participants = list()

    '''def _get_match_details(self, game_id):
        print(game_id)
        time.sleep((os.cpu_count()/20) + 0.1)
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

        print(match_details[0])
        self.matches_detail = match_details
        '''

    def _get_participant_id_from_summoner_name(self, d: dict):
        return list(d.keys())[list(d.values()).index(self.name)]

    def get_participants(self):
        # Participant dictionary with participantId as key and summonerName as value
        participants_dict = dict.fromkeys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        for match in self.match_data:
            for i in range(0, 10):
                participants_dict[i+1] = match['participantIdentities'][i]['player']['summonerName']
            self.participants.append(participants_dict.copy())
            participants_dict.clear()
        print(self.participants)

        return self.participants

    def get_total_hours(self):
        total_hours = 0
        for match in self.match_data:
            total_hours += int(match['gameDuration']) / 3600

        print("Total hours played: ", total_hours)
        return total_hours

    def get_weekday_performance(self):
        win_loss_per_weekday = dict.fromkeys(['Monday', 'Tuesday', 'Wednesday',
                                              'Thursday', 'Friday', 'Saturday', 'Sunday'])
        for k, v in win_loss_per_weekday.items():
            win_loss_per_weekday[k] = [0, 0]

        for idx, match in enumerate(self.match_data):
            participant_id = self._get_participant_id_from_summoner_name(self.participants[idx])
            unixtime = int(match['gameCreation']) / 1000
            weekday = datetime.utcfromtimestamp(unixtime).strftime('%A')
            for i in range(0, 10):
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

    def get_champion_v_champion_performance(self):

        # NOTE: EXCLUDE EVERYTHING EXCEPT 'gameMode': 'CLASSIC'

        # We need a lookup table for championIds -> names

        # HEATMAP Matrix comparison of Champ v Champ performance?

        for idx, match in enumerate(self.match_data):
            participant_id = self._get_participant_id_from_summoner_name(self.participants[idx])
            champion_id = match['participants'][participant_id - 1]['championId']
            print(f"Part ID {participant_id} and champ is {champion_id}")
            for i in range(0, 10):
                if match['participants'][i]['timeline']['lane'] == match['participants'][participant_id - 1]['timeline']['lane'] \
                        and (match['participants'][i]['participantId'] != participant_id):
                    opponent_id = match['participants'][i]['participantId']
                    opponent_champion = match['participants'][opponent_id - 1]['championId']
                    if match['participants'][i]['timeline']['role'] == match['participants'][participant_id - 1]['timeline']['role']:
                        opponent_id = match['participants'][i]['participantId']
                        opponent_champion = match['participants'][opponent_id - 1]['championId']
                    print(f"OPP ID {opponent_id} and champ is {opponent_champion}")



    def predict_weekday_performance(self):
        # get_weekday_performance()
        pass

