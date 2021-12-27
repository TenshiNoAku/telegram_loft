from sqlalchemy.orm import Session
from db_main import *
import random

engine = create_engine("sqlite:///uny_loft.db",
                       connect_args={"check_same_thread": False})  # движок бота
session = Session(bind=engine)  # запуск сесии


def create_user(call):  # creating new user
    if session.query(Users).filter(
            Users.user_id.like(f"{call.from_user.id}")).count() == 0:
        user = Users(
            user_id=call.from_user.id,
            username=call.from_user.username
        )
        session.add(user)
        session.commit()


def del_direct(user_id, pd_code): #delete curr direction
    pd_id = session.query(Professional_Directions).filter(
        Professional_Directions.pd_code.like(f"{pd_code}")
    ).first().pd_id
    if session.query(Users_Directions).filter(
            Users_Directions.direction.like(f"{pd_id}"),
            Users_Directions.user.like(f"{user_id}")
    ).count() == 1:
        session.query(Users_Directions).filter(
            Users_Directions.user.like(f"{user_id}"),
            Users_Directions.direction.like(f"{pd_id}")
        ).delete(synchronize_session=False)
        session.commit()


def del_subj(user_id, subj_code): #delete curr subj
    subj_id = session.query(Subjects).filter(
        Subjects.subject_code.like(f"{subj_code}")
    ).first().subject_id
    if session.query(Users_Subjects).filter(
            Users_Subjects.subject.like(f"{subj_id}"),
            Users_Subjects.user.like(f"{user_id}")
    ).count() == 1:
        session.query(Users_Subjects).filter(
            Users_Subjects.user.like(f"{user_id}"),
            Users_Subjects.subject.like(f"{subj_id}")
        ).delete(synchronize_session=False)
        session.commit()


def check_dir_search(user_id): #checking dir search curr user
    return session.query(Users).filter(
        Users.user_id.like(f"{user_id}")
    ).first().dir_search


def change_dir_search(user_id, dir_search): #change dir search curr user
    session.query(Users).filter(
        Users.user_id.like(f"{user_id}")
    ).first().dir_search = dir_search
    session.commit()
    return "✅ Поиск изменен"


def new_direct(call, semant=False):# adding new direct to user's profile
    if semant:
        user_id = call["user_id"]
        pd_code = call["pd_code"]
    else:
        user_id = call.from_user.id
        pd_code = call.data.split("_")[1]
    pd_id = session.query(Professional_Directions).filter(
        Professional_Directions.pd_code.like(f"{pd_code}")
    ).first().pd_id
    if session.query(Users_Directions).filter(
            Users_Directions.direction.like(f"{pd_id}"),
            Users_Directions.user.like(f"{user_id}")
    ).count() == 0:
        user_direction = Users_Directions(
            user=user_id,
            direction=pd_id
        )
        session.add(user_direction)
        session.commit()
        return "✅ Направление добавлено"
    else:
        del_direct(user_id, pd_code)
        return "❌ Направление удалено"


def new_subj(call, semant=False):  # adding new subject to user's profile
    if semant:
        user_id = call["user_id"]
        subj_code = call["subj_code"]
    else:
        user_id = call.from_user.id
        subj_code = call.data.split("_")[1]
    subj_id = session.query(Subjects).filter(
        Subjects.subject_code.like(f"{subj_code}")
    ).first().subject_id
    if session.query(Users_Subjects).filter(
            Users_Subjects.subject.like(f"{subj_id}"),
            Users_Subjects.user.like(f"{user_id}")
    ).count() == 0:
        user_subject = Users_Subjects(
            user=user_id,
            subject=subj_id
        )
        session.add(user_subject)
        session.commit()
        return "✅ Предмет добавлен"
    else:
        del_subj(user_id, subj_code)
        return "❌ Предмет убран"


def clear_subj(call):  # clear all subjects of current user
    user_id = call.from_user.id
    session.query(Users_Subjects).filter(
        Users_Subjects.user.like(f"{user_id}")
    ).delete(synchronize_session=False)
    session.commit()
    return "Все предметы удалены из поиска"


def clear_direct(call):  # clear all direct of current user
    user_id = call.from_user.id
    session.query(Users_Directions).filter(
        Users_Directions.user.like(f"{user_id}")
    ).delete(synchronize_session=False)
    session.commit()
    return "Направления удалены из поиска"


def clear_all(call):  # clear all search_params
    clear_subj(call)
    clear_direct(call)
    clear_blacklist(call)


def new_city_blacklist(call):  # adding new city to user's city_blacklist
    user_id = call.from_user.id
    city = session.query(Users).filter(Users.user_id.like(f"{user_id}")).first().current_city
    u_c = Users_Cities(
        user=user_id,
        city=city
    )
    session.add(u_c)
    session.commit()
    return "✅ Город добавлен в черный список"


def current_city(city_title, user_id):  # setting city of current university in user profile
    city_id = session.query(Cities).filter(
        Cities.city_title.like(f"{city_title}")).first().city_id
    session.query(Users).filter(Users.user_id.like(f"{user_id}")).first().current_city = city_id
    session.commit()


def clear_blacklist(call): #clear blacklist
    user_id = call.from_user.id
    session.query(Users_Cities).filter(
        Users_Cities.user.like(f"{user_id}")
    ).delete(synchronize_session=False)
    session.commit()
    return "✅ Все города удалены из черного списка"


def current_url(url, user_id):  # setting url of current university in user profile
    session.query(Users).filter(Users.user_id.like(f"{user_id}")).first().current_url = url
    session.commit()


def list_of_directions_curr_user(user_id, code=True):  # return list of directions current user
    directions = session.query(Users_Directions).filter(
        Users_Directions.user.like(f"{user_id}")
    ).all()
    pd_list = []
    if code:
        for direction in directions:
            pd_list.append(session.query(Professional_Directions).filter(
                Professional_Directions.pd_id.like(f"{direction.direction}")).first().pd_code)
    else:
        for direction in directions:
            pd_list.append(session.query(Professional_Directions).filter(
                Professional_Directions.pd_id.like(f"{direction.direction}")).first().pd_name)
    return pd_list


def new_fav(user_id):  # adding new fav to user's fav_list
    fav = session.query(Users).filter(Users.user_id.like(f"{user_id}")).first().current_url[:-5]
    if session.query(Users_Subjects).filter(
            Users_Favorites.fav_url.like(f"{fav}"),
            Users_Favorites.user.like(f"{user_id}")
    ).count() == 0:
        u_f = Users_Favorites(
            user=user_id,
            fav_url=fav
        )
        session.add(u_f)
        session.commit()
    return "✅ ВУЗ добавлен в избранное"


def set_ege_score_curr_user(user_id, score):  # setting new ege_score for user
    session.query(Users).filter(Users.user_id.like(f"{user_id}")).first().ege_score = score
    session.commit()
    return "✅ Баллы ЕГЭ установлены!"


def get_ege_score_curr_user(user_id):  # return ege_score current user
    return session.query(Users).filter(Users.user_id.like(f"{user_id}")).first().ege_score


def list_of_favorites_curr_user(user_id):  # return list of favorites current user
    favorites = session.query(Users_Favorites).filter(
        Users_Favorites.user.like(f"{user_id}")
    ).all()
    fav_list = []
    for fav in favorites:
        fav_list.append(fav.fav_url)
    if fav_list:
        return "\n".join(fav_list)
    else:
        return "💡 Вы еще не добавили ни один ВУЗ в избранное"


def list_of_subjects_curr_user(user_id,
                               code=True):  # return list of subject current user (code or name)
    subjects = session.query(Users_Subjects).filter(
        Users_Subjects.user.like(f"{user_id}")
    ).all()
    subj_list = []
    if code:
        for subject in subjects:
            subj_list.append(session.query(Subjects).filter(
                Subjects.subject_id.like(f"{subject.subject}")).first().subject_code)
    else:
        for subject in subjects:
            subj_list.append(session.query(Subjects).filter(
                Subjects.subject_id.like(f"{subject.subject}")).first().subject_name)
    return subj_list


def list_of_cities():  # return list of all cities
    cities_list = []
    cities = session.query(Cities).all()
    for city in cities:
        cities_list.append(city.city_id)
    return cities_list


def list_city_curr_user(user_id):  # return list of cities excluding user's blacklist
    city_list = set(list_of_cities())
    black_list = set()
    user_city_blacklist = session.query(Users_Cities).filter(
        Users_Cities.user.like(f"{user_id}")
    ).all()
    user_city_blacklist = set(user_city_blacklist)
    for city in user_city_blacklist:
        black_list.add(int(city.city))
    return list(city_list.difference(black_list))


def gen_subj_url(user_id):  # generating new url using user's subjects
    city_list = list_city_curr_user(user_id)
    subj_list = list_of_subjects_curr_user(user_id)
    city = random.choice(city_list)
    try:
        url = f"https://vuzopedia.ru/region/city/{city}/poege/egerus;{';'.join(random.choices(subj_list, k=2))}"
    except Exception as ex:
        url = f"https://vuzopedia.ru/region/city/{city}/poege/egerus"
    return url


def gen_dir_url(user_id):  # generating new url using user's subjects
    city_list = list_city_curr_user(user_id)
    dir_list = list_of_directions_curr_user(user_id)
    city = random.choice(city_list)
    try:
        url = f"https://vuzopedia.ru/region/city/{city}?s={random.choice(dir_list)}"
    except Exception as ex:
        url = f"https://vuzopedia.ru/region/city/{city}?s=fsb"
    return url


def search_params(call):  # return all search params of current user
    user_id = call.from_user.id
    subj_list = "\n".join(list_of_subjects_curr_user(user_id, code=False))
    dir_list = "\n".join(list_of_directions_curr_user(user_id, code=False))
    return subj_list, dir_list
