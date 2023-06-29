import scrapy
from kastorama.items import CastparserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
import response
import wget

URL = 'https://www.castorama.ru'


class CastSpider(scrapy.Spider):
    name = "cast"
    allowed_domains = ["castorama.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(URL + next_page, callback=self.parse)
        product_links = response.xpath("//a[@class='product-card__img-link']/@href").getall()
        for link in product_links:
            yield response.follow(URL + link, callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        loader = ItemLoader(item=CastparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "////div[@class='js-zoom-container']/img/@data-src")
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_value('link_prod', response.url)
        yield loader.load_item()
