import pymorphy2
from db_changes import new_subj, new_direct, del_subj, del_direct


def semant_parser(text, user_id):
    func_dir = {
        "удалить": "del",
        "убрать": "del",
        "исключить": "del",
        "добавить": "add",
    }
    sub_dir = {
        "Авиационый": "aviacionnye",
        "Аграрный": "agrarnye",
        "Архитектурный": "arkhitekturnye",
        "Биологический": "biologicheskie",
        "Культура": "vuzykultury",
        "Гуманитарный": "gumanitarnye",
        "Дизайн": "dizayna",
        "Информационный": "informacionnye",
        "Географический": "geograficheskie",
        "Экономический": "ekonomicheskie",
        "Медицинский": "medicinckie",
        "Педагогический": "pedagogicheskie",
        "Сервис": "servic",
        "Спортивный": "sportivnye",
        "Строительный": "stroitelnye",
        "Технический": "tekhnicheskie",
        "Нефтяной": "neftyanye",
        "Психологический": "psihologicheskie",
        "Транспортный": "transportnye",
        "Пищевой": "pishevye",
        "Юридический": "yuridicheskie",
        "Математика": "egemat",
        "Обществознание": "egeobsh",
        "Физика": "egefiz",
        "История": "egeist",
        "Информатика": "egeinform",
        "Биология": "egebiol",
        "Химия": "egehim",
        "География": "egegeorg",
        "Литература": "egeliter",
        "Английский": "egeinyaz",
        "Немецкий": "egeinyaz",
        "Все": "all"
    }
    func_code = None
    sec_code = None
    morph = pymorphy2.MorphAnalyzer()
    text = text.split(" ")
    for i in text:
        if bool(morph.parse(i)[0].normal_form in func_dir.keys()):
            func_code = func_dir[morph.parse(i)[0].normal_form]
            break
    for i in text:
        word = morph.parse(i)[0].normal_form.title()
        if (word in sub_dir.keys()):
            sec_code = sub_dir[word]
            break
    if func_code and sec_code:
        if func_code == "add":
            if sec_code.startswith("ege"):
                new_subj({"user_id": user_id, "subj_code": sec_code}, semant=True)
            else:
                new_direct({"user_id": user_id, "pd_code": sec_code}, semant=True)
        if func_code == "del":
            if sec_code.startswith("ege"):
                del_subj(user_id, sec_code)
            else:
                del_direct(user_id, sec_code)
        return "Команда успешно выполнена"
    else:
        return "Я вас не понял"
