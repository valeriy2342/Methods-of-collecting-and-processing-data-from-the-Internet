import scrapy
from itemloaders.processors import TakeFirst, Compose


def clean_name(value: list):
    try:
        value = value[0].replace('\n', '').replace('  ', '')
    except Exception as e:
        print(e)
        return value
    return value


class CastparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(input_processor=Compose(clean_name), output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    link_prod = scrapy.Field()
