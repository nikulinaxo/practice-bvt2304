import requests
from currency_symbols import CurrencySymbols
import db


url = "https://api.hh.ru/vacancies"

headers = {
    "User-Agent": "Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
}

def get(x, e, s):

    params = {
        "text": x,
        "per_page": 5,
        "experience": e,
        "schedule": s
    }

    vacancies = requests.get(url, headers=headers, params=params)

    vacancies = vacancies.json()

    found = vacancies['found']

    db.addStat(x, s, e, found)


    items = vacancies['items']

    vacancies = []

    for item in items:

        if item['salary'] == None:
            salary = "Не указано"
        elif item['salary']['from'] == None:
            currency = str(item['salary']['currency'])
            if currency == "RUR":
                currency = 'RUB'
            salary = "До " + str(item['salary']['to']) + str(CurrencySymbols.get_symbol(currency))
        elif item['salary']['to'] == None:
            currency = str(item['salary']['currency'])
            if currency == "RUR":
                currency = 'RUB'
            salary = "От " + str(item['salary']['from']) + str(CurrencySymbols.get_symbol(currency))
        else:
            currency = str(item['salary']['currency'])
            if currency == "RUR":
                currency = 'RUB'
            salary = "От " + str(item['salary']['from']) + str(CurrencySymbols.get_symbol(currency)) + " до " + str(
                item['salary']['to']) + str(CurrencySymbols.get_symbol(currency))

        requirement = str(item['snippet']['requirement'])

        if "highlighttext" in requirement:
            requirement = requirement.replace("<highlighttext>", "")
            requirement = requirement.replace("</highlighttext>", "")

        vacancy = {
            "name": item['name'],
            "area": item['area']['name'],
            "sal": salary,
            "url": item['alternate_url'],
            "req": requirement
        }

        vacancies.append(vacancy)

    return vacancies