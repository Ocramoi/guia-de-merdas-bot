import utils
from player import Player
from game_management import GameManagement

class Game:
    ''' Class corresponding an instance of a game'''

    def __init__(self, saves_file):
        self.manager = GameManagement(saves_file)
        self.saves_file = saves_file
        self.cached_players = []
   
    def get_cached_player(self, player_id, player_username):
        for player in self.cached_players:
            if player_id == player.telegram_id:
                return player
        return None

    def load_player(self, response, player_id, player_username):
        ''' Loads a instance of a player from the saves file or
        creates one and adds it too cache '''
        cachedPlayer = self.get_cached_player(player_id, player_username)
        if cachedPlayer:
            return cachedPlayer

        load_file = utils.readJSON(self.saves_file)

        if not load_file or player_id not in load_file.keys():
                response.append (f"@{player_username} registrado com sucesso")
                player = Player(player_username, player_id)
        else:
            load_player = load_file[player_id]

            player = Player(username=player_username, telegram_id=player_id,
                            achievements=load_player["achievements"],level=load_player["level"],
                            points=load_player["points"], titles=load_player["titles"],
                            lattest_chat=load_player["lattest_chat"], main_title=load_player["main_title"])
        
        self.cached_players.append(player)
        return player


        
