# -*- coding: utf-8 -*-

# Scrapy settings for watchdog project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = BASE_DIR+'/logs'
BOT_NAME = 'watchdog'

SPIDER_MODULES = ['watchdog.spiders']
NEWSPIDER_MODULE = 'watchdog.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'watchdog (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrapy_mongodb.MongoDBPipeline' : 300,
}
#MONGODB_UNIQUE_KEY = 'GUID'
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "watchdog"
MONGODB_COLLECTION = "ollyshap"
MONGODB_ADD_TIMESTAMP = True