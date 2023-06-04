# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com'
user = 'valeriy2342'
r = requests.get(f'{url}/users/{user}/repos')


with open('data.json', 'w') as f:
    json.dump(r.json(), f)

print('Cписок репозиториев: ')

for i in r.json():
        print(f" - {i['name']}")
