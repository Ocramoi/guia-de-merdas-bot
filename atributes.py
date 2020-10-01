import utils
from operator import itemgetter

ACHIEVEMENTS = utils.readCSV("./static/achievements.csv")
TITLES =  utils.readJSON("./static/titles.json")

def get_max_level(achievement_list):
    max_points = 0
    max_level = 0
    for achv in achievement_list:
        if int(achv['points']) > 0:
            max_points += int(achv['points'])
    
    tmp_max_points = max_points


    while tmp_max_points / 2 > 0:
        max_level += 1
        tmp_max_points = int(tmp_max_points / 2)
        
    return max_level, max_points

def get_levelup_requirements():
    max_level, max_points = get_max_level(ACHIEVEMENTS)
    level_info = list()
    while max_points/2 > 0:
        level_info.append(max_points)
        max_points = int(max_points/2)

    return list(reversed(level_info))

def get_achv(player_achievements):
    achievements = []
    for index, achievement in enumerate(ACHIEVEMENTS):
        if index not in player_achievements:
            achievements.append(
                Achievement(achievement_id=index,
                            name=achievement['name'],
                            sticker_id=achievement['sticker_id'],
                            points=achievement['points'],
                            response=achievement['response']))
        else:
            achievements.append(
                Achievement(achievement_id=index,
                            name=achievement['name'],
                            sticker_id=achievement['sticker_id'],
                            points=achievement['points'],
                            response=achievement['response'],
                            is_completed=True)
                )
    
    return achievements

def get_ranks():
    players = utils.readJSON("./static/players.json")
    ranks = ["Rank de players:\n"]
    for index, value in enumerate(sorted(list(players.values()), key=itemgetter("points"), reverse=True)):
        ranks.append(f"{index + 1}) {value['username']}: {value['points']} xp")
    
    return ranks

def get_titles(player_achievements):
    titles = list()

    for title, requirements in TITLES.items():
        has_requirements = True
        for requirement in requirements:
            if requirement not in player_achievements:
                has_requirements = False
        if has_requirements:
            titles.append(title)
    
    return titles
class Achievement:

    def __init__(self, achievement_id, name, sticker_id, points, response, is_completed=False):
        self.id = achievement_id
        self.name = name
        self.sticker_id = sticker_id
        self.points = points
        self.response = response
        self.is_completed = is_completed
    
    def __repr__(self):
        return self.response
        

LEVELUP_REQUIREMENTS= get_levelup_requirements()
MAX_LEVEL, trash = get_max_level(ACHIEVEMENTS)
