# -*- coding: utf-8 -*-
import scrapy


class OllyshapSpider(scrapy.Spider):
    name = "ollyshap"
    allowed_domains = ["ollyshap.ru"]
    start_urls = (
        'http://www.ollyshap.ru/',
    )

    def parse(self, response):
    	#print response.xpath('//title')
    	#print response.xpath('//meta')
    	for sel in response.xpath('//link'):
    		print sel.extract()
    		#print sel.xpath('/@rel').extract()
    		#if sel.xpath('/@rel').extract() == 'shortcut icon':
    		#	print 'busted!'
