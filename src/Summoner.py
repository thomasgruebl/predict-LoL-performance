import collections
from datetime import datetime

import matplotlib.pyplot as plt


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

    """
    # handling data from deprecated match-v4 API call
    def get_participants_v4(self):
        # Participant dictionary with participantId as key and summonerName as value
        participants_dict = dict.fromkeys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        for match in self.match_data:
            for i in range(0, 10):
                try:
                    participants_dict[i+1] = match['participantIdentities'][i]['player']['summonerName']
                except KeyError:
                    continue
            self.participants.append(participants_dict.copy())
            participants_dict.clear()
        print(self.participants)

        return self.participants
    """

    def get_participants_v5(self):
        # Participant dictionary with participantId as key and summonerName as value
        participants_dict = dict.fromkeys([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        for match in self.match_data:
            for i in range(0, 10):
                try:
                    participants_dict[i + 1] = match['info']['participants'][i]['summonerName']
                except KeyError:
                    continue
            self.participants.append(participants_dict.copy())
            participants_dict.clear()
        print(self.participants)

        return self.participants

    def get_total_hours(self):
        total_hours = 0
        for match in self.match_data:
            total_hours += int(match['info']['gameDuration']) / 3600000

        print("Total hours played: ", total_hours)
        return total_hours

    def get_weekday_performance(self):
        win_loss_per_weekday = dict.fromkeys(['Monday', 'Tuesday', 'Wednesday',
                                              'Thursday', 'Friday', 'Saturday', 'Sunday'])
        for k, v in win_loss_per_weekday.items():
            win_loss_per_weekday[k] = [0, 0]

        for idx, match in enumerate(self.match_data):
            participant_id = self._get_participant_id_from_summoner_name(self.participants[idx])
            unixtime = int(match['info']['gameCreation']) / 1000
            weekday = datetime.utcfromtimestamp(unixtime).strftime('%A')
            for i in range(0, 10):
                if match['info']['participants'][i]['participantId'] == participant_id:
                    if match['info']['participants'][i]['win']:
                        win_loss_per_weekday[weekday][0] += 1
                    else:
                        win_loss_per_weekday[weekday][1] += 1

        print(win_loss_per_weekday)

        # Optional: plot weekday performance

        chart_labels = win_loss_per_weekday.keys()
        wins = [x[0] for x in win_loss_per_weekday.values()]
        losses = [x[1] for x in win_loss_per_weekday.values()]
        wins_percentage = [round(x / (x + y), 2) if (x + y) > 0 else 0 for x, y in zip(wins, losses)]
        losses_percentage = [round(x / (x + y), 2) if (x + y) > 0 else 0 for x, y in zip(losses, wins)]
        width = 0.35

        fig, ax = plt.subplots()
        ax.bar(chart_labels, wins_percentage, width, label='Wins')
        ax.bar(chart_labels, losses_percentage, width, bottom=wins_percentage, label='Losses')
        ax.set_ylabel('Percentage')
        ax.set_title('W/L percentage comparison per weekday')
        ax.legend()
        plt.show()

        return win_loss_per_weekday

    def get_champion_v_champion_performance(self, champion_id_name_lookup):
        """returns champion v champion performance based on win/loss ratio"""
        # HEATMAP Matrix comparison of Champ v Champ performance?

        # farming stats

        # Format: k: -> (summoner_champ, opponent_champ) v: -> [summoner wins and losses]
        performance_dict = collections.defaultdict(list)

        for idx, match in enumerate(self.match_data):
            # exclude all other game modes
            if match['info']['gameMode'] != 'CLASSIC':
                continue

            participant_id = self._get_participant_id_from_summoner_name(self.participants[idx])
            champion_id = match['info']['participants'][participant_id - 1]['championId']
            print(f"Part ID {participant_id} and champ is {champion_id}")
            for i in range(0, 10):
                if match['info']['participants'][i]['individualPosition'] == match['info']['participants'][participant_id - 1]['individualPosition'] \
                        and (match['info']['participants'][i]['participantId'] != participant_id):

                    opponent_id = match['info']['participants'][i]['participantId']
                    opponent_champion = match['info']['participants'][opponent_id - 1]['championId']

                    # print(f"OPP ID {opponent_id} and champ is {opponent_champion}")

                    try:
                        if match['info']['participants'][i]['win']:
                            performance_dict[(champion_id_name_lookup[str(champion_id)],
                                              champion_id_name_lookup[str(opponent_champion)])].append('loss')
                        else:
                            performance_dict[(champion_id_name_lookup[str(champion_id)],
                                              champion_id_name_lookup[str(opponent_champion)])].append('win')
                    except KeyError:
                        continue

        print(performance_dict)

    def predict_next_game_outcome(self):
        """Markov Chain prediction of next game win/loss"""
        match_outcomes = list()
        most_recent_game = True
        most_recent_game_outcome = True
        for idx, match in enumerate(self.match_data):
            participant_id = self._get_participant_id_from_summoner_name(self.participants[idx])
            for i in range(0, 10):
                if match['info']['participants'][i]['participantId'] == participant_id:
                    if most_recent_game:
                        most_recent_game_outcome = match['info']['participants'][i]['win']
                    most_recent_game = False

                    if match['info']['participants'][i]['win']:
                        match_outcomes.append('win')
                    else:
                        match_outcomes.append('loss')

        pairs = self.__make_pairs(match_outcomes)
        win_loss_dict = self.__make_chains(pairs)

        if most_recent_game_outcome:
            count_wins = win_loss_dict['win'].count('win')
            count_losses = win_loss_dict['win'].count('loss')
            return {'win_prob': count_wins / (count_wins + count_losses),
                    'loss_prob': count_losses / (count_wins + count_losses)}
        else:
            count_wins = win_loss_dict['loss'].count('win')
            count_losses = win_loss_dict['loss'].count('loss')
            return {'win_prob': count_wins / (count_wins + count_losses),
                    'loss_prob': count_losses / (count_wins + count_losses)}

    @staticmethod
    def __make_pairs(match_outcomes):
        for i in range(len(match_outcomes) - 1):
            yield match_outcomes[i], match_outcomes[i + 1]

    @staticmethod
    def __make_chains(pairs):
        win_loss_dict = dict()
        for outcome1, outcome2 in pairs:
            if outcome1 in win_loss_dict.keys():
                win_loss_dict[outcome1].append(outcome2)
            else:
                win_loss_dict[outcome1] = [outcome2]
        return win_loss_dict

    def predict_weekday_performance(self):
        """Extrapolating average historical data to future events"""
        # get_weekday_performance()
        pass
