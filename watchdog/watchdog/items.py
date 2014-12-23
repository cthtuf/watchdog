# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WatchdogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    meta_description = scrapy.Field()
    meta_keywords = scrapy.Field()
    meta_author = scrapy.Field()
    favicon = scrapy.Field()
    og_title = scrapy.Field()
    og_type = scrapy.Field()
    og_url = scrapy.Field()
    og_image = scrapy.Field()
    og_audio = scrapy.Field()
    og_description = scrapy.Field()
    og_determiner = scrapy.Field()
    og_locale = scrapy.Field()
    og_locale_alternate = scrapy.Field()
    og_site_name = scrapy.Field()
    og_video = scrapy.Field()
