import scrapy


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://imdb.com"]

    def parse(self, response):
        pass
