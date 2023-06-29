# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from pymongo import MongoClient, collection


class KastoramaPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.kast

    def process_item(self, item, spider):
        collection = self.mongo_base['kast']
        print()
        return item


class KastoramaphotosPipeline(ImagesPipeline):
    @staticmethod
    def add_url(link):
        return 'https://www.castorama.ru' + link

    def get_media_requests(self, item, info):
        if item['photos']:
            if isinstance(item['photos'], str):
                try:
                    yield Request(KastoramaphotosPipeline.add_url(item['photos']))
                except Exception as e:
                    print(e)
            elif isinstance(item['photos'], list):
                for img in (item['photos']):
                    try:
                        yield Request(KastoramaphotosPipeline.add_url(img))
                    except Exception as e:
                        print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
            return item

        collection.insert_one(item)  # Добавляем в базу данных
        return item
