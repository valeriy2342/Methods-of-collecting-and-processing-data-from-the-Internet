import requests
from lxml import html
from pymongo.errors import DuplicateKeyError
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['dbNews']
news_db = db.news

# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, dzen-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.


header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}
response = requests.get('https://lenta.ru', headers=header)

dom = html.fromstring(response.text)

lenta_news = []

items = dom.xpath("//a[contains(@class,'card-mini _topnews')]")
for item in items:
    base_url = 'https://lenta.ru'
    new = {}
    title = item.xpath(".//span[@class='card-mini__title']/text()")
    url = item.xpath(".//@href")
    publication_time = item.xpath(".//time[@class='card-mini__date']/text()")

    new['news_source'] = 'Lenta.ru'
    new['title'] = title[0]
    new['publication_time'] = publication_time
    new['url'] = str(base_url) + url[0]
    lenta_news.append(new)

# 2. Сложить собранные новости в БД Минимум один сайт, максимум - все три

    try:
        news_db.insert_one(new)
    except DuplicateKeyError:
        pprint(f'Новость - {name[0]} уже есть в базе')

pprint(lenta_news)