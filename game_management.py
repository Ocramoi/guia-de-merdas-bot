import utils
from datetime import datetime as dt
from player import Player

class GameManagement:
    ''' Class corresponding to some game configurations '''

    def __init__(self, saves_file, cache_time=60*60, max_cached=10):
        self.saves_file = saves_file
        self.init_time = dt.now().timestamp()
        self.cache_time = cache_time
        self.max_cached = max_cached

    def stage_changes(self, players):
        ''' Stage a player to an save file '''
        load_file = utils.readJSON(self.saves_file)

        while players:
            player = players.pop()
            if not load_file or player not in load_file.keys():
                json_obj = {
                    player.telegram_id: {
                        'username': player.username,
                        'achievements': player.achievements,
                        'main_title': player.main_title,
                        'level': player.level,
                        'points': player.points,
                        'titles': player.titles,
                        'lattest_chat': player.lattest_chat
                    }
                }
                utils.appendJSON(self.saves_file, json_obj)

            else:
                load_file[player.telegram_id] = {
                    'username': player.username,
                    'achievements': player.achievements,
                    'main_title': player.main_title,
                    'level': player.level,
                    'points': player.points,
                    'titles': player.titles,
                    'lattest_chat': player.lattest_chat
                }
                utils.writeJSON(load_file, self.saves_file)

    def evaluate_reset(self, cached):
        current_time = dt.now().timestamp()
        reset_time = self.init_time + self.cache_time
        current_cached = len(cached)

        if current_time > reset_time or current_cached > self.max_cached:
            self.stage_changes(cached)
            self.init_time = current_time
