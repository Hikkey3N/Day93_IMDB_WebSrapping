import scrapy
from imdb_scrape.items import MovieItem



class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        pass
