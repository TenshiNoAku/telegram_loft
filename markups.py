from telebot import types


def main_markup():
    mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🌟 Избранное")
    item2 = types.KeyboardButton("📖 Предметы")
    item3 = types.KeyboardButton("💯 Баллы ЕГЭ")
    item4 = types.KeyboardButton("💼 Направления")
    item5 = types.KeyboardButton("⚙ Параметры поиска")
    item6 = types.KeyboardButton("🍀 Мне повезет")
    mark_up.add(item1, item2, item3, item4, item5, item6)
    return mark_up


def random_uny_markup():
    mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🔎 Найти ВУЗ")
    item2 = types.KeyboardButton("🔄 Сменить поиск")
    item3 = types.KeyboardButton("🚫Очистить ЧС городов")
    item4 = types.KeyboardButton("🔙 Назад")
    mark_up.add(item1, item2, item3, item4)
    return mark_up


def change_search_type_markup():
    mark_up = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("По ЕГЭ",
                                       callback_data="search_ege")
    item2 = types.InlineKeyboardButton("По направлениям",
                                       callback_data="search_dir")
    mark_up.add(item1, item2)
    return mark_up


def set_ege_markup():
    mark_up = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("101-150",
                                       callback_data="ege_min")
    item2 = types.InlineKeyboardButton("151-200",
                                       callback_data="ege_average")

    item3 = types.InlineKeyboardButton("201-250",
                                       callback_data="ege_average_plus")

    item4 = types.InlineKeyboardButton("251-300",
                                       callback_data="ege_max")
    mark_up.add(item1, item2, item3, item4)
    return mark_up


def subjects_markup():
    mark_up = types.InlineKeyboardMarkup(row_width=3)
    item2 = types.InlineKeyboardButton("Ин. яз",
                                       callback_data="subj_egeinyaz")
    item3 = types.InlineKeyboardButton("Обществознание",
                                       callback_data="subj_egeobsh")
    item4 = types.InlineKeyboardButton("Физика",
                                       callback_data="subj_egefiz")
    item5 = types.InlineKeyboardButton("История", callback_data="subj_egeist")
    item6 = types.InlineKeyboardButton("Информатика", callback_data="subj_egeinform")
    item7 = types.InlineKeyboardButton("Биология", callback_data="subj_egebiol")
    item8 = types.InlineKeyboardButton("Химия", callback_data="subj_egehim")
    item9 = types.InlineKeyboardButton("География", callback_data="subj_egegeorg")
    item10 = types.InlineKeyboardButton("Литература", callback_data="subj_egeliter")
    item11 = types.InlineKeyboardButton("Математика (Проф.)",
                                        callback_data="subj_egemat")

    item12 = types.InlineKeyboardButton("Очистить",
                                        callback_data="clear_subj")
    mark_up.add(item2, item3, item4, item5, item6, item7, item8, item9, item10, item11,
                item12)
    return mark_up


def directs_markup():
    mark_up = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("Авиационое", callback_data="dir_aviacionnye")
    item2 = types.InlineKeyboardButton("Аграрное", callback_data="dir_agrarnye")
    item3 = types.InlineKeyboardButton("Архитектурное", callback_data="dir_arkhitekturnye")
    item4 = types.InlineKeyboardButton("Биологическое", callback_data="dir_biologicheskie")
    item5 = types.InlineKeyboardButton("Культура", callback_data="dir_vuzykultury")
    item6 = types.InlineKeyboardButton("Гуманитарное", callback_data="dir_gumanitarnye")
    item7 = types.InlineKeyboardButton("Дизайн", callback_data="dir_dizayna")
    item8 = types.InlineKeyboardButton("Информационное", callback_data="dir_informacionnye")
    item9 = types.InlineKeyboardButton("Географическое", callback_data="dir_geograficheskie")
    item10 = types.InlineKeyboardButton("Экономическое", callback_data="dir_ekonomicheskie")
    item11 = types.InlineKeyboardButton("Медицинское", callback_data="dir_medicinckie")
    item12 = types.InlineKeyboardButton("Педагогическое", callback_data="dir_pedagogicheskie")
    item13 = types.InlineKeyboardButton("Сервис", callback_data="dir_servic")
    item14 = types.InlineKeyboardButton("Спортивное", callback_data="dir_sportivnye")
    item15 = types.InlineKeyboardButton("Строительное", callback_data="dir_stroitelnye")
    item16 = types.InlineKeyboardButton("Техническое", callback_data="dir_tekhnicheskie")
    item17 = types.InlineKeyboardButton("Нефтяное", callback_data="dir_neftyanye")
    item18 = types.InlineKeyboardButton("Психологическое", callback_data="dir_psihologicheskie")
    item19 = types.InlineKeyboardButton("Транспортное", callback_data="dir_transportnye")
    item20 = types.InlineKeyboardButton("Пищевое", callback_data="dir_pishevye")
    item21 = types.InlineKeyboardButton("Юридическое", callback_data="dir_yuridicheski")
    item22 = types.InlineKeyboardButton("Очистить", callback_data="clear_dir")
    mark_up.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11,
                item12, item13, item14, item15, item16, item17, item18, item19, item20, item21,
                item22)
    return mark_up


def university_search_markup():
    mark_up = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("Добавить в избранное", callback_data="search_favorites")
    item2 = types.InlineKeyboardButton("Убрать город из поиска",
                                       callback_data="search_city_blacklist")
    mark_up.add(item1, item2)
    return mark_up
