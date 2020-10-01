import csv
import json
from atributes import Achievement, get_achv, get_titles, LEVELUP_REQUIREMENTS, MAX_LEVEL

class Player():
    ''' Defines a player in the game '''

    def __init__(self, username, telegram_id, lattest_chat=None, main_title="noob", 
                 achievements=None, level=0, points=0, titles=None):
        self.main_title = main_title        
        self.username = username
        self.telegram_id = telegram_id
        self.level = level
        self.points = points
        self.lattest_chat = lattest_chat

        if not achievements: 
            self.achievements = list()
        else:
            self.achievements = achievements
        
        if not titles:
            self.titles = list()
        else:
            self.titles = titles

    def set_chat(self, response, chat_id):
        self.lattest_chat = chat_id
        response.append("Chat atualizado com sucesso.")
   
    def set_main_title(self, response, new_main_title):
        if new_main_title == self.main_title:
            response.append("Esse já é seu título principal.")
        elif new_main_title in self.titles:
            self.main_title = new_main_title
            response.append("Título atualizado com sucesso.")
        else:
            response.append("Vocẽ não desbloqueou esse título ainda.")

    def add_achv(self, all_achvs, new_achv_id, response):
        ''' Adds a new achievements completed by the player '''
        # TODO: In order to call this method, need to verify if the sticker contaning this achievement was clicked/sent
        if new_achv_id not in self.achievements:
            new_achievement = all_achvs[new_achv_id]

            self.achievements.append(new_achv_id)
            self.points += int(new_achievement['points'])

            response.append("Conquista desbloqueada: {}".format(new_achievement['name']))
            response.append(f"{new_achievement['response']}")
            self.evaluate_levelup(response)
            self.evaluate_new_title(response)
        
        else:
            response.append("Conquista já desbloqueada")

    def evaluate_new_title(self, response):
        current_titles = get_titles(self.achievements)
        for title in current_titles:
            if title not in self.titles:
                self.titles.append(title)
                response.append(f"Título desbloqueado: {title}")
        

    def evaluate_levelup(self, response):
        ''' Evaluates if a players has enought points in order to level up '''
        current_level = self.level
        current_points = self.points
        if current_level < MAX_LEVEL and current_points >= LEVELUP_REQUIREMENTS[current_level]:
            response.append("Subindo de nível...\nParabéns!")
            self.level += 1
        else:
            response.append(f"Faltam {LEVELUP_REQUIREMENTS[current_level] - current_points} pontos para evoluir de nível")

    def show_status(self):
        status = [
            f"---  <b>@{self.username}</b> status  ---",
            f"<i>{self.main_title.title()}</i> | level {self.level} | {self.points} xp"
        ]
        
        return "\n".join(status)

    def show_titles(self):
        titles = ["Títulos desbloqueados:\n"]
        for title in self.titles:
            titles.append(f"- {title}")
        
        return titles
    
    def show_achvs(self):
        achvs = ["Conquistas desbloqueadas:\n"]
        all_achvs = get_achv(self.achievements)
        for achv in all_achvs:
            if achv.is_completed:
                achvs.append(f"- {achv.name}")
        
        return achvs




