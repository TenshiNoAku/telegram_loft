import telebot  # Для работы с api телеграма
import time
import datetime
from markups import *
from db_changes import *
from uny_parser import *
from Answers import *

print(datetime.datetime.now().strftime("%d.%m.%Y"))
Token = open("Token.txt","r").readline()  # Bot's Token
bot = telebot.TeleBot(Token, parse_mode=None)  # bot creation


def key_board(message):
    '''Creating keyboard'''
    bot.send_message(message.chat.id, hellow_answer, reply_markup=main_markup())


@bot.message_handler(commands=["start"])
def start(message):  # the starting func
    key_board(message)  # set main keyboard


@bot.message_handler()
def word_comands(message):  # word command processing
    if message.text == "🍀 Мне повезет":
        uny_params = rand_uny(gen_subj_url(message.from_user.id))
        score = get_ege_score_curr_user(message.from_user.id)
        start_time = datetime.datetime.now()
        stuck_flag = False
        while uny_params is None:
            uny_params = rand_uny(gen_subj_url(message.from_user.id))
            if uny_params is not None and uny_params["nonpaid"].isdigit():
                if int(uny_params["nonpaid"]) < int(score):
                    continue
            end_time = datetime.datetime.now()
            if (end_time - start_time).total_seconds() > 30:  # checking search is stuck?
                stuck_flag = True
                break
        if stuck_flag:
            bot.send_message(message.chat.id,
                             "ВУЗов по данным параметрам не найдено, попробуйте их изменить",
                             )
        else:
            current_city(uny_params["city_title"], message.from_user.id)
            current_url(uny_params["href"], message.from_user.id)
            bot.send_message(message.chat.id, uny_answ(uny_params),
                             reply_markup=university_search())
    elif message.text == "📖 Предметы":
        bot.send_message(message.chat.id, "Выберите предметы которые собираетесь сдавать на ЕГЭ",
                         reply_markup=subjects_markup())
    elif message.text == "🌟 Избранное":
        bot.send_message(message.chat.id, list_of_favorites_curr_user(message.from_user.id))
    elif message.text == "💼 Направления":
        bot.send_message(message.chat.id, "1", reply_markup=directs_markup())
    elif message.text == "💯 Баллы ЕГЭ":
        bot.send_message(message.chat.id,
                         "Выберите количество баллов егэ из предложенных диапозонов",
                         reply_markup=set_ege_markup())
    elif message.text == "Параметры поиска":
        bot.send_message(message.chat.id, params_answ(*search_params(message)))
    elif message.text == "По направлениям":
        bot.send_message(message.chat.id, "1")
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Возвращаемся, на главную страницу",
                         reply_markup=main_markup())
    else:
        bot.send_message(message.chat.id, "неизвестная команда")


@bot.callback_query_handler(
    func=lambda call: True)  # handler callback functions
def callback_inline(call):  # Feedback Handler
    '''handler callback functions'''
    try:
        if call.message:  # call.data is None?
            if call.data.startswith("dir"):  # call.data is direction handler
                new_direct(call)
                bot.send_message(call.message.chat.id, "Направление успешно добавлено")
            if call.data.startswith("subj"):  # call.data is subject handler
                new_subj(call)
                bot.send_message(call.message.chat.id, "Предмет успешно добавлен")
            if call.data.startswith("search"):  # call.data is search handler
                if call.data == "search_city_blacklist":
                    new_city_blacklist(call)
                    bot.send_message(call.message.chat.id, "Город успешно убран из поиска")
                if call.data == "search_favorites":  # call.data is facorites handler
                    new_fav(call.from_user.id)
                    bot.send_message(call.message.chat.id, "Универ успешно добавлен в избарнное")
            if call.data.startswith("ege"):  # call.data is ege handler
                ege_scores = {
                    "min": 125,
                    "average": 175,
                    "average_plus": 225,
                    "max": 275
                }
                set_ege_score_curr_user(call.from_user.id, ege_scores[call.data[4:]])
            if call.data.startswith("clean"):
                if call.data == "clear_subj":
                    clear_subj(call)
                if call.data == "clear_dir":
                    clear_direct(call)
                if call.data == "clear_all":
                    clear_all(call)
    except Exception as ex: #Troubles?
        print(ex)


def poll():
    bot.polling(True)


try:
    poll()
except requests.exceptions.Timeout:
    print("Timeout occurred")
    time.sleep(3)
