# import scrapy
# from scrapy.http import HtmlResponse
#
# from jobparser.items import JobparserItem
#
#
# class SupjSpider(scrapy.Spider):
#     name = 'supj'
#     allowed_domains = ['superjob.ru']
#
#     start_urls = ['https://kstovo.superjob.ru/vacancy/search/?keywords=Python']
#
#     def parse(self, response: HtmlResponse, **kwargs):
#         links = response.xpath("//div[@class='QLXR1 cuSpN _2s0QR _3fgaD']/@href").getall()
#         for link in links:
#             yield response.follow(link, callback=self.vacancy_parse)
#
#             # link_f = []
#             # for l in links:
#             #     link_f.append(f"https://kstovo.superjob.ru{l}")
#
#     def vacancy_parse(self, response: HtmlResponse):
#         name = response.xpath("//h1/text()").get()
#         url = response.url
#         salary = response.xpath("//span[@class='_2eYAG _1R5IY _16BIl _2ZnQY']//text()").getall()
#         yield JobparserItem(name=name, url=url, salary=salary)
