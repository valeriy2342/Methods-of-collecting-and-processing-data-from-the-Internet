from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import re
import time
import json
from pymongo.errors import DuplicateKeyError
from pprint import pprint


client = MongoClient('127.0.0.1', 27017)
db = client['danabase']
vacancy_db = db.vacancy

name_text = input("Введите должность: ")

base_url = 'https://hh.ru'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}

url = f'https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text={name_text}&excluded_text=&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page=1'
response = requests.get(url, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')

pages = dom.find('div', {'class': 'pager'}).find_all('span', recursive=False)[-1].text.replace('...', '')
page_count = int(pages)

vacancy_list = []
for page in range(page_count):
    url = f'https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text={name_text}&excluded_text=&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={page}'
    vacancies = dom.find_all('div', {'class': 'serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}
        info = vacancy.find('a', {'class': 'serp-item__title'})
        link = info['href']
        name = info.getText()
        # description = info.find('span')
        salary_info = vacancy.find('span', {'class': 'bloko-header-section-3'})

        if salary_info == None:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = (str(salary_info.getText())).replace('\u202f', '')
            salary = re.split(r'\s|-', salary)
            vacancy_id = re.findall('\d+', link)[0]

            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
                salary_currency = salary[2]
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
                salary_currency = salary[2]
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[2])
                salary_currency = salary[3]

        vacancy_data['_id'] = vacancy_id
        vacancy_data['Название ваккансии'] = name
        vacancy_data['Ссылка на вакансию'] = link
        vacancy_data['Минимальная зарплата'] = salary_min
        vacancy_data['Максимальная зарплата'] = salary_max
        vacancy_data['Валюта расчета в'] = salary_currency

        vacancy_list.append(vacancy_data)

        try:
            vacancy_db.insert_one(vacancy_data)
        except DuplicateKeyError:
            pprint(f'Вакансия c _ID = {vacancy_id} уже существует')
            pprint(vacancy_data)

with open(f'Вакансии_{name_text}.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_list, f, indent=4, ensure_ascii=False)


sum_salary = int(input('Mинимальная заработная плата: '))

def salary (sum_salary):
    vacancy_db = db.vacancy.find({'$or':[{'Salary_min': {'$gte':sum_salary}}, {'Salary_max':{'$lte':sum_salary}}]})
    for vac in vacancy_db:
        pprint(vac)

salary(sum_salary)

pprint('Done')