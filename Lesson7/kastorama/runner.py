from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from kastorama.spiders.cast import CastSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    # search = input()
    runner = CrawlerRunner(settings)
    runner.crawl(CastSpider, search='межкомнатные двери')
    reactor.run()
