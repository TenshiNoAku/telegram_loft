import telebot  # Для работы с api телеграма
import time
import datetime
from markups import *
from db_changes import *
from uny_parser import *
from Answers import *
from semant_parser import semant_parser

print(datetime.datetime.now().strftime("%d.%m.%Y"))
Token = open("Token.txt", "r").readline()  # Bot's Token
bot = telebot.TeleBot(Token, parse_mode=None)  # bot creation


def key_board(message):
    '''Creating keyboard'''
    bot.send_message(message.chat.id, hello_answ(), reply_markup=main_markup())


@bot.message_handler(commands=["start"])
def start(message):  # the starting func
    create_user(message)
    key_board(message)  # set main keyboard


@bot.message_handler(commands=["semant"])
def semant(message):
    bot.send_message(message.chat.id,
                     semant_parser(" ".join(message.text.split(" ")[1:]), message.from_user.id))


@bot.message_handler()
def word_comands(message):  # word command processing
    if message.text == "🍀 Мне повезет":
        bot.send_message(message.chat.id,
                         "Вы понравились одному ВУЗу, является ли симпатия взаимной🤔❤?",
                         reply_markup=random_uny_markup())
    elif message.text == "🔄 Сменить поиск":
        bot.send_message(message.chat.id, "По какому критерию будем искать ВУЗ?",
                         reply_markup=change_search_type_markup())
    elif message.text == "🔎 Найти ВУЗ":
        bot.send_message(message.chat.id,
                         "Поиск запущен, ожидайте....",
                         )
        uny_params = None
        score = get_ege_score_curr_user(message.from_user.id)
        start_time = datetime.datetime.now()
        stuck_flag = False
        while uny_params is None:
            if check_dir_search(message.from_user.id):
                uny_params = rand_uny(check_dir_search(message.from_user.id),
                                      gen_dir_url(message.from_user.id))
            else:
                uny_params = rand_uny(check_dir_search(message.from_user.id),
                                      gen_subj_url(message.from_user.id))
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
                             reply_markup=university_search_markup())
    elif message.text == "📖 Предметы":
        bot.send_message(message.chat.id,
                         "Когда на голову падает яблоко, открывают всемирный закон."
                         " А когда вся яблоня - вводят ЕГЭ. По каким предметам ты сдавал ЕГЭ? 🎓📕📚",
                         reply_markup=subjects_markup())
    elif message.text == "🌟 Избранное":
        bot.send_message(message.chat.id,
                         fav_answ(list_of_favorites_curr_user(message.from_user.id)))
    elif message.text == "💼 Направления":
        bot.send_message(message.chat.id, "1", reply_markup=directs_markup())
    elif message.text == "💯 Баллы ЕГЭ":
        bot.send_message(message.chat.id,
                         "Сколько у тебя баллов?💯",
                         reply_markup=set_ege_markup())
    elif message.text == "⚙ Параметры поиска":
        bot.send_message(message.chat.id, params_answ(*search_params(message)))
    elif message.text == "🔙 Назад":
        bot.send_message(message.chat.id, "Возвращаемся на главную страницу.....",
                         reply_markup=main_markup())
    else:
        bot.send_message(message.chat.id, "💡 Неизвестная команда")


@bot.callback_query_handler(
    func=lambda call: True)  # handler callback functions
def callback_inline(call):  # Feedback Handler
    '''handler callback functions'''
    try:
        if call.message:  # call.data is None?
            if call.data.startswith("dir"):  # call.data is direction handler

                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, new_direct(call))
            elif call.data.startswith("subj"):  # call.data is subject handler
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, new_subj(call))
            elif call.data.startswith("search"):  # call.data is search handler
                if call.data == "search_city_blacklist":
                    # bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, new_city_blacklist(call))
                elif call.data == "search_favorites":  # call.data is facorites handler
                    # bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, new_fav(call.from_user.id))
                elif call.data == "search_dir":
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, change_dir_search(call.from_user.id, 1))
                elif call.data == "search_ege":
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, change_dir_search(call.from_user.id, 0))
            elif call.data.startswith("ege"):  # call.data is ege handler
                ege_scores = {
                    "min": 125,
                    "average": 175,
                    "average_plus": 225,
                    "max": 275
                }
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, set_ege_score_curr_user(call.from_user.id,
                                                                               ege_scores[
                                                                                   call.data[4:]]))
            elif call.data.startswith("clear"):
                if call.data == "clear_subj":
                    bot.send_message(call.message.chat.id, clear_subj(call))
                elif call.data == "clear_dir":
                    bot.send_message(call.message.chat.id, clear_direct(call))
                elif call.data == "clear_all":
                    clear_all(call)
                bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as ex:  # Troubles?
        print(ex)


def poll():
    bot.polling(True)


try:
    poll()
except requests.exceptions.Timeout:
    print("Timeout occurred")
    time.sleep(3)
