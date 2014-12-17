# -*- coding: utf-8 -*-
import scrapy
from watchdog.items import WatchdogItem


class OllyshapSpider(scrapy.Spider):
    name = "ollyshap"
    allowed_domains = ["ollyshap.ru"]
    start_urls = (
        'http://www.ollyshap.ru/',
    )

    def parse(self, response):
    	wdi = WatchdogItem()
    	r = response.xpath('/html/head/title/text()')
    	if r:
    		wdi['title']  = r.extract()[0]
    	for sel in response.xpath('/html/head/link'):
    		#print "Processing %r" % sel.xpath('@rel').extract()[0]
    		if sel.xpath('@rel'): 
    			if sel.xpath('@rel').extract()[0] == u'shortcut icon':
    			#print "Found favicon %r" % sel.xpath('@rel')
    				r = sel.xpath('@href')
    				if r:
    					wdi['favicon'] = r.extract()[0]
    	for sel in response.xpath('/html/head/meta'):
    		r = sel.xpath('@name')
    		if r: 
	    		if sel.xpath('@name').extract()[0] == 'description':
	    			r = sel.xpath('@content')
	    			if r:
	    				wdi['meta_description'] = r.extract()[0]
	    		elif sel.xpath('@name').extract()[0] == 'keywords':
	    			r = sel.xpath('@content')
	    			if r:
	    				wdi['meta_keywords'] = r.extract()[0]
	    		elif sel.xpath('@name').extract()[0] == 'author':
	    			r = sel.xpath('@content')
	    			if r:
	    				wdi['meta_author'] = r.extract()[0]

    	yield wdi

