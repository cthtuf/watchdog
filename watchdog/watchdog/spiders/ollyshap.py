# -*- coding: utf-8 -*-
import scrapy


class OllyshapSpider(scrapy.Spider):
    name = "ollyshap"
    allowed_domains = ["ollyshap.ru"]
    start_urls = (
        'http://www.ollyshap.ru/',
    )

    def parse(self, response):
    	print response.xpath('//title')
    	print response.xpath('//meta')
    	print response.xpath('//link')
