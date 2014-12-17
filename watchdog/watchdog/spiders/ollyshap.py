# -*- coding: utf-8 -*-
import scrapy


class OllyshapSpider(scrapy.Spider):
    name = "ollyshap"
    allowed_domains = ["ollyshap.ru"]
    start_urls = (
        'http://www.ollyshap.ru/',
    )

    def parse(self, response):
    	for sel in response.xpath('/html/body/div[2]/div/div[1]/div/a'):
    		print sel.xpath('@href').extract()[0]
    		
