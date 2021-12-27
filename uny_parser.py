# (dies from cringe)
import random
import pymorphy2
import requests
from bs4 import BeautifulSoup


def rand_uny(dir_search, url=f"https://vuzopedia.ru/region/city/59?s=aviacionnye"):  # parsing url
    # url for parse
    morph = pymorphy2.MorphAnalyzer()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    titles = soup.find_all("div", class_="itemVuzTitle")
    if len(titles) == 0:  # we have a university with the given parameters?
        return None
    city = soup.find_all("h4")[0]
    city = city.text.strip().split(" ")
    if dir_search:
        city_title = morph.parse(city[3])[0].normal_form.title()
    else:
        if city[4] == "с":
            city_title = city[3]
        else:
            city_title = city[3] + city[4]
    uni_parametrs = soup.find_all("a", class_="tooltipq")[4:]  # universities  parameters
    flag = True
    counter = 0  # counter of universities
    un_list = []  # creating list of universities
    for parameter in uni_parametrs:
        if flag:  # is new university?
            d = {
                "city_title": city_title,  # creating dict with university characteristics
                "title": "-",  # university title
                "paid": "-",  # minimum passing score for paid
                "nonpaid": "-",  # minimum passing score for budget
                "paid_place": "-",  # number of paid places
                "nonpaid_place": "-",  # number of nonpaid places
                "min_price": "-",  # minimum tuition fees
                "href": "None"  # link to more information
            }
            href = soup.find_all("h6", class_="fitemVv")[counter]
            d["title"] = titles[counter].text.strip()
            d["href"] = "https://vuzopedia.ru" + href.find("a").get("href")[
                                                 :href.find("a").get("href").find('/p')]
            flag = False  # not a new university
        if "минимальная стоимость по вузу (руб/год)" in parameter.text:
            d["min_price"] = parameter.text[3:parameter.text.find("⃏") - 1]
        if "минимальный суммарный проходной балл на бюджет по вузу" in parameter.text:
            d["nonpaid"] = parameter.text[:parameter.text.find("м")]
        if "минимальный суммарный проходной балл на платное по вузу" in parameter.text:
            d["paid"] = parameter.text[:parameter.text.find("м")]
        if "местколичество бюджетных мест по вузу" in parameter.text:
            d["nonpaid_place"] = parameter.text[:parameter.text.find("м") - 1]
        if "местколичество платных мест по вузу" in parameter.text:
            d["paid_place"] = parameter.text[:parameter.text.find("м") - 1]
            flag = True  # new university
            counter += 1  # id university
            un_list.append(d)  # add university to list
    if un_list:
        return un_list[random.randint(0, len(titles) - 1)]  # return random university from the list
