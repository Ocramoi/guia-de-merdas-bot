from telegram import InlineQueryResultCachedSticker, ChosenInlineResult, ParseMode, InputTextMessageContent, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, ConversationHandler, MessageHandler, Filters 

from conf.env import TOKEN
import logging

from atributes import get_achv, Achievement, ACHIEVEMENTS, get_titles, get_ranks
from player import Player 
from game_management import GameManagement
from game import Game

import signal
import sys

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 

game = Game("./static/players.json")
MAINTITLE = 0
def get_player(update, response):
    player_id = str(update.message.from_user.id)
    player_username = update.message.from_user.username
    
    game.manager.evaluate_reset(game.cached_players)
    player = game.load_player(response=response, player_id=player_id,
                              player_username=player_username)

    return player

def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Hoho, para começar a jogar primeiro escolha um chat onde receberá as informações relacionadas a suas conquistas.\nApós isso digitando @AchvBot conquistas, você verá uma série de stickers, clique naquelas que já fez para adicionar a sua lista"
    )

def change_title(update, context):
    player = get_player(update=update, response=[])
    titles = get_titles(player.achievements)
    reply_keyboard = [titles]
    
    if len(titles) < 2:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Você ainda não possui nenhum título desbloqueado."
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "OkiDoki, qual título você quer?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard)
        )
        return MAINTITLE

def main_title(update, context):
    response = list()
    player = get_player(update=update, response=[])
    player.set_main_title(response, update.message.text)
    
    update.message.reply_text(
        "\n".join(response),
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def get_rank(update, context):
    game.manager.stage_changes(game.cached_players)
    ranks = get_ranks()

    context.bot.send_message(
        chat_id = update.message.chat_id,
        text="\n".join(ranks)
    )

def titles(update, context):
    player = get_player(update=update, response=[])
    titles = player.show_titles()
    if len(titles) < 2:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Você ainda não possui nenhum título desbloqueado."
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="\n".join(titles)
        )

def achievements(update, context):
    player = get_player(update=update, response=[])
    achievements = player.show_achvs()

    if len(achievements) < 2:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Você ainda não tem nenhuma conquista desbloqueada."
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="\n".join(achievements)
        )        
    
def status(update, context):
    player = get_player(update=update, response=[])
    status = player.show_status()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=status,
        parse_mode='html'

    )
    

def set_chat(update, context):
    response = []
    chat_id = update.message.chat_id
    player_id = str(update.message.from_user.id)
    player_username = update.message.from_user.username

    player = game.load_player(response=response,
                              player_id=player_id,
                              player_username=player_username)
    player.set_chat(response=response,
                    chat_id=chat_id)

    for text in response:
        context.bot.send_message(
            chat_id=chat_id,
            text=text
        )
   
def get_chosen_achv(update, context):
    response=[]
    player_id = str(update.chosen_inline_result.from_user.id)
    player_username =  update.chosen_inline_result.from_user.username

    game.manager.evaluate_reset(game.cached_players)
    player = game.load_player(response=response,           
                             player_id=player_id, player_username=player_username)
  
    new_achv = int(update.chosen_inline_result.result_id)
    player.add_achv(ACHIEVEMENTS, new_achv, response)

    for text in response:
        context.bot.send_message(
            chat_id=player.lattest_chat,
            text=text
        )

def inline_achv(update, context):
    player_id = str(update.inline_query.from_user.id)
    player_username = update.inline_query.from_user.username

    player = game.load_player(response=[],
                             player_id=player_id, 
                             player_username=player_username)

    if not player.lattest_chat:
        context.bot.send_message(
            chat_id=player_id,
            text="Por favor, escolha um chat para mandar as mensagens com /set_chat.\nVocê poderá mudar o chat quando quiser"
        )
        return

    results = []
    achievements = get_achv(player.achievements)
    for counter,achievement in enumerate(achievements):
        if counter == 49:
            break
        
        if not achievement.is_completed:
            results.append(
                InlineQueryResultCachedSticker(id=achievement.id,
                                               sticker_file_id=achievement.sticker_id))
    
    context.bot.answer_inline_query(update.inline_query.id, results, cache_time=0)

def main(): 
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )

    dispatcher.add_handler(
        InlineQueryHandler(inline_achv)
    )

    dispatcher.add_handler(
        ChosenInlineResultHandler(get_chosen_achv)
    )
    
    dispatcher.add_handler(
        CommandHandler('set_chat', set_chat)
    )

    dispatcher.add_handler(
        CommandHandler("status", status)
    )
    
    dispatcher.add_handler(
        CommandHandler("achievements", achievements)
    )

    dispatcher.add_handler(
        CommandHandler("titles", titles)
    )
    dispatcher.add_handler(
        CommandHandler("rank", get_rank)
    )
    
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("change_title", change_title)],
            states={
                MAINTITLE: [MessageHandler(Filters.text, main_title)]
            },
            fallbacks=[]
        )
    )


    updater.start_polling()

def signal_handler(sig, frame):
    print('Saving game..')
    game.manager.stage_changes(game.cached_players)

if __name__:
    main()
    signal.signal(signal.SIGINT, signal_handler)
    print("press CTRL + C to save and CTRL + Z to stop.")
    signal.pause()
