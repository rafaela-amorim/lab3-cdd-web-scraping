import scrapy


class MySpiderSpider(scrapy.Spider):
    name = 'my_spider'
    allowed_domains = ['my_spider.com']
    start_urls = ['http://my_spider.com/']

    def parse(self, response):
        pass
