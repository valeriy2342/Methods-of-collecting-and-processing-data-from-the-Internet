# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy


    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy
        # self.mongo_base = client.vacancy_hh_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base['vacancy']
        if spider.name == 'hhru':
            salary_list = []
            for _ in item['salary']:
                s = _.replace(" ", "").replace("\xa0", "")
                salary_list.append(s)
            item['salary'] = salary_list

        if item['salary'] == []:
            item['salary'] = 'None'
            item['salary_min'] = 'None'
            item['salary_max'] = 'None'

        if item['salary'][0] == 'от':
            item['salary_min'] = int(item['salary'][1])
            if item['salary'][2] == 'до':
                item['salary_max'] = int(item['salary'][3])
            else:
                item['salary_max'] = 'None'

        elif item['salary'][0] == 'до':
            item['salary_min'] = 'None'
            item['salary_max'] = int(item['salary'][1])
        elif item['salary'][0] == 'з/пнеуказана':
            item['salary_min'] = 'None'
            item['salary_max'] = 'None'

        del item['salary']

        # if spider.name == 'supj':
        #     salary_list = []
        #     for _ in item['salary']:
        #         s = _.replace(" ", "").replace("\xa0", "")
        #         salary_list.append(s)
        #     item['salary'] = salary_list
        #
        #     if item['salary'][0] == 'Подоговорённости':
        #         item['salary_min'] = 'NA'
        #         item['salary_max'] = 'NA'
        #
        #     elif item['salary'][2] == '—':
        #         item['salary_min'] = int(item['salary'][0])
        #         item['salary_max'] = int(item['salary'][4])
        #         item['currency'] = item['salary'][6]
        #
        #     elif item['salary'][0] == 'от':
        #         pos = item['salary'][2].find('руб.')
        #         item['salary_min'] = item['salary'][2][:pos]
        #         item['currency'] = item['salary'][2][pos:]
        #
        #     elif item['salary'][0] == 'до':
        #         pos = item['salary'][2].find('руб.')
        #         item['salary_max'] = item['salary'][2][:pos]
        #         item['currency'] = item['salary'][2][pos:]
        #
        #     elif item['salary'][2] == 'руб.':
        #         item['salary_min'] = item['salary'][0]
        #         item['salary_max'] = item['salary'][0]
        #         item['currency'] = item['salary'][2]
        #     else:
        #         item['salary_min'] = 'wrong'
        #         item['salary_max'] = 'wrong'
        #     del item['salary']
        #
        #     item['location'] = ' '.join(item['location']).replace("  ", " ")\
        #         .replace(" ,", ",").replace(" Показать на карте", "")
        #     item['site'] = 'https://superjob.ru'

        collection.insert_one(item)  # Добавляем в базу данных
        return item
