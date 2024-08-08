# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MovieItem(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   year = scrapy.Field()
   parrent_guide = scrapy.Field()
   run_time = scrapy.Field()
   rating = scrapy.Field()
   num_reviews = scrapy.Field()
   popularity = scrapy.Field()
   genre = scrapy.Field()
   description = scrapy.Field()
   director = scrapy.Field()
   writers = scrapy.Field()
   stars = scrapy.Field()
   budget = scrapy.Field()
   gross_na = scrapy.Field()
   gross_globe = scrapy.Field()