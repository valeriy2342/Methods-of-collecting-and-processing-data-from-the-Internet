from scrapy import Request
import scrapy
from scrapy_splash import SplashRequest

from avitoparser.items import AvitoparserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = ["https://www.avito.ru/all?q=%D0%BA%D0%BE%D1%82%D1%8F%D1%82%D0%B0"]

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield SplashRequest(url)

    def parse(self, response: HtmlResponse):
        links = response.xpath("//h3[@itemprop='name']/../@href").getall()  # Извлекаем ссылку до конца
        for link in links:
            yield SplashRequest("https://avito.ru" + link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath("//h1/span/text()").get()
        price = response.xpath("//span[@class='style-price-value-main-TIg6u']//text()").get()
        description = response.xpath("//div[@itemprop='description']/p/text()").get()
        url = response.url
        photos = response.xpath("//li//img/@src | //div[@class='image-frame-wrapper-_NvbY']/@data-url").getall()
        yield AvitoparserItem(name=name, price=price, description=description, photos=photos, url=url)

    # def parse_abs(self, response: HtmlResponse):
    #     loader = ItemLoader(item=AvitoparserItem(), response=response)
    #     loader.add_xpath('name', "/h1/span/text()")
    #     loader.add_xpath('photos', "//li//img/@src | //div[@class='image-frame-wrapper-_NvbY']/@data-url")
    #     loader.add_xpath('price', "//span[@class='style-price-value-main-TIg6u']//text()")
    #     loader.add_xpath('description', "//div[@itemprop='description']/p/text()")
    #     loader.add_value('link_prod', response.url)
    #     yield loader.load_item()