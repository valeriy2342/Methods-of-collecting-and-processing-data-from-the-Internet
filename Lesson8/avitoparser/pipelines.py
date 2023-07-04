# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from scrapy import Request
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from pymongo import MongoClient, collection

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AvitoparserPipeline:
    def process_item(self, item, spider):
        print()
        return item


class AvitophotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['photos']:
            try:
                yield scrapy.Request(img)
            except Exception as e:
                print(e)


    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
            return item


