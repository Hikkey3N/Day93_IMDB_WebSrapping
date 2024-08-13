import scrapy
from imdb_scrape.items import MovieItem



class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    # custom_settings = {
    #     'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # }

    def parse(self, response):
        movies = response.css('a.ipc-title-link-wrapper')
        
        for movie in movies:
            affix_url = movie.css('a ::attr(href)').get()
            movie_url = "https://www.imdb.com" + affix_url

            yield scrapy.Request(movie_url, callback = self.parse_movie_page)
    

    def parse_movie_page(self, response):
        movie_items = MovieItem()
        movie_items['url'] = response.url
        movie_items['title'] = response.css('span.hero__primary-text::text').get()
        movie_items['year'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()').get()
        movie_items['parent_guide'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a/text()').get()
        movie_items['run_time'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]/text()').get()
        movie_items['rating'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[1]/span[1]/text()').get()
        movie_items['num_reviews'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[3]/text()').get()
        movie_items['popularity'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[3]/a/span/div/div[2]/div[1]/text()').get()
        movie_items['genre'] = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a/span/text()').get()
        movie_items['director'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div/ul/li/a/text()').get()
        movie_items['writer'] = response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[2]/div/ul/li/a/text()').getall()
        movie_items['stars'] = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[3]/div/ul/li/a/text()').getall()
        movie_items['budget'] = response.xpath('//li[@data-testid="title-boxoffice-budget"]//span[@class="ipc-metadata-list-item__list-content-item"]/text()').get()
        movie_items['gross_na'] = response.xpath('//li[@data-testid="title-boxoffice-grossdomestic"]//span[@class="ipc-metadata-list-item__list-content-item"]/text()').get()
        movie_items['gross_globe'] = response.xpath('//li[@data-testid="title-boxoffice-cumulativeworldwidegross"]//span[@class="ipc-metadata-list-item__list-content-item"]/text()').get()

        # Ensure no field is None
        for field in movie_items.fields:
            if movie_items.get(field) is None:
                self.logger.error(f"Missing field {field} in {response.url}")

        yield movie_items
