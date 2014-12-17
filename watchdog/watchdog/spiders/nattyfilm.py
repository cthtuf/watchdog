# -*- coding: utf-8 -*-
import scrapy


class NattyfilmSpider(scrapy.Spider):
    name = "nattyfilm"
    allowed_domains = ["nattyfilm.com"]
    start_urls = (
        'http://www.nattyfilm.com/',
    )

    def parse(self, response): 
       pass
