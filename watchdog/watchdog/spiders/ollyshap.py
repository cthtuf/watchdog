# -*- coding: utf-8 -*-
import scrapy
from watchdog.items import WatchdogItem
from scrapy.log import ScrapyFileLogObserver
from scrapy import log
from watchdog import settings


class OllyshapSpider(scrapy.Spider):
    name = "ollyshap"
    allowed_domains = ["yandex.ru",]
    start_urls = (
        'http://www.yandex.ru/',
    )

    def __init__(self, name=None, **kwargs):
        ScrapyFileLogObserver(open(settings.LOG_DIR+"/spider.log", 'w'), level=log.logging.INFO).start()
        ScrapyFileLogObserver(open(settings.LOG_DIR+"/spider_error.log", 'w'), level=log.logging.ERROR).start()

        super(OllyshapSpider, self).__init__(name, **kwargs)

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
            name_attr = sel.xpath('@name')
            property_attr = sel.xpath('@property')
            content_attr = sel.xpath('@content')
            if name_attr:
                if name_attr.extract()[0] == 'description':
                    wdi['meta_description'] = content_attr.extract()[0] if content_attr else 'blank'
                elif name_attr.extract()[0] == 'keywords':
                    wdi['meta_keywords'] = content_attr.extract()[0] if content_attr else 'blank'
                elif name_attr.extract()[0] == 'author':
                    wdi['meta_author'] = content_attr.extract()[0] if content_attr else 'blank'
            if property_attr:
                if property_attr.extract()[0] == 'og:title':
                    wdi['og_title'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:type':
                    wdi['og_type'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:image':
                    wdi['og_image'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:url':
                    wdi['og_url'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:audio':
                    wdi['og_audio'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:description':
                    wdi['og_description'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:determiner':
                    wdi['og_determiner'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:locale':
                    wdi['og_locale'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:description':
                    wdi['og_description'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:locale:alternate':
                    wdi['og_locale_alternate'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:site_name':
                    wdi['og_site_name'] = content_attr.extract()[0] if content_attr else 'blank'
                elif property_attr.extract()[0] == 'og:video':
                    wdi['og_video'] = content_attr.extract()[0] if content_attr else 'blank'
    	yield wdi

