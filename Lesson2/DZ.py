import re
import requests
from bs4 import BeautifulSoup
import pprint
from pymongo import MongoClient

url = 'https://nn.hh.ru/search/vacancy'
params = {'search_field': 'name', 'text': 'Python', 'page': 0, 'tems_on_page': '100'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.172 Yowser/2.5 Safari/537.36'}
vacancy_list = []
session = requests.Session()

client = MongoClient('localhost', 27017)
db = client['data_base']
vacancy_db3 = db.vacancy

while True:
    response = session.get(url=url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancy = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})
    if len(vacancy) == 0 or response.status_code == '404':
        break
    params['page'] += 1
    for item in vacancy:
        vacancy_data = {}
        block_a = item.find('a', {'class': 'serp-item__title'})
        href = block_a.get('href')
        name = block_a.text
        salary = item.find('span', {'class': 'bloko-header-section-3'})
        if salary:
            salary = salary.text
        vacancy_data['name'] = name
        vacancy_data['reference'] = href
        vacancy_data['where_published'] = 'hh.ru'
        salary_data = {}
        salary_value = (str(salary)).replace('\u202f', '')
        if salary_value[0].isdigit():
            re_minimum_maximum = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            minimum = re_minimum_maximum.findall(salary_value)[1]
            maximum = re_minimum_maximum.findall(salary_value)[0]
            currency = re_currency.findall(salary_value)[-1]
            salary_data['maximum'] = int(maximum)
            salary_data['minimum'] = int(minimum)
            salary_data['currency'] = currency
            vacancy_data['salary'] = salary_data
        if salary_value[0] == 'о':
            re_minimum_maximum = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            minimum = re_minimum_maximum.findall(salary_value)[0]
            currency = re_currency.findall(salary_value)[-1]
            salary_data['minimum'] = int(minimum)
            salary_data['currency'] = currency
            vacancy_data['salary'] = salary_data
        if salary_value[0] == 'д':
            re_minimum_maximum = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            maximum = re_minimum_maximum.findall(salary_value)[0]
            currency = re_currency.findall(salary_value)[-1]
            salary_data['maximum'] = int(maximum)
            salary_data['currency'] = currency
            vacancy_data['salary'] = salary_data
        if salary_value == 'None':
            vacancy_data['salary'] = None
        if db.vacancy_db4.find_one({'reference': vacancy_list}) is None:
            db.vacancy_db4.insert_one(
                {'name': vacancy_data['name'],
                 'href': vacancy_data['reference'],
                 'minimum': salary_value
                 }
            )

# print(vacancy_list)

for i in db.vacancy_db4.find({}):
    print(i)


def salary_db():
    salary_amount = int(input('Размер зарплаты: '))

    vacancy_ans = []
    for i in db.vacancy_db4.find({'&or': [{salary_data['minimum']: {'$gte': salary_amount}}, {salary_data['maximum']: {'$lte': salary_amount}}]}):
        vacancy_ans.append(i)

    return vacancy_ans


print(salary_db())
