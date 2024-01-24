# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Uk49ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()


class ResultsItem(scrapy.Item):
    date = scrapy.Field()
    lunch_draw = scrapy.Field()
    tea_draw = scrapy.Field()


