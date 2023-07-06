# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


class AvitoparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()


# def clean_name(value: list):
#     try:
#         value = value[0].replace('\n', '')
#     except Exception as e:
#         print(e)
#         return value
#     return value
#
# def clean_price(value):
#     new_value = value.replace('\xa0', '').replace('  ', '')
#     try:
#         new_value = int(new_value)
#     except:
#         pass
#     return new_value
#
# class AvitoparserItem(scrapy.Item):
#     _id = scrapy.Field()
#     name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_name))
#     price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_price))
#     photos = scrapy.Field()
#     link_prod = scrapy.Field()
#     description = scrapy.Field()
