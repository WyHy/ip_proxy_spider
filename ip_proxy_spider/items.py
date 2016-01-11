# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IPItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    anonymous = scrapy.Field()
    http_type = scrapy.Field()
    location = scrapy.Field()
    latency = scrapy.Field()
    last_verify_time = scrapy.Field()
    source = scrapy.Field()
