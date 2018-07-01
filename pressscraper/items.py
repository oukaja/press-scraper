# -*- coding: utf-8 -*-
import scrapy


class ArticleItem(scrapy.Item):
    journal = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()

