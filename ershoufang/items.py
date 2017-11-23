# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
		title = scrapy.Field()
		roomNum = scrapy.Field()
		size = scrapy.Field()
		orient = scrapy.Field()
		floor = scrapy.Field()
		address = scrapy.Field()
		sumPrice = scrapy.Field()
		unitPrice = scrapy.Field()
		_id = scrapy.Field()
