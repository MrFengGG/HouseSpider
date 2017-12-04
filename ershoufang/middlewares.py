# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import http
from scrapy import signals
import random
import pymongo

class UrlFilter(object):
	#初始化过滤器（使用mongodb过滤）
	def __init__(self):
		self.settings = get_project_settings()
		self.client = pymongo.MongoClient(
			host = self.settings['MONGO_IP'],
			port = self.settings['MONGO_PORT'])
		self.db = self.client[self.settings['MONGO_DB']]
		self.col = self.db[self.settings['CITY']]
	def process_request(self,request,spider):
		if self.col.count({"fromUrl":request}) > 0:
			print("查询的数据大于0")
			url = request.url
			return http.Response(url=url,body="None")
				
class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):	
				self.user_agent = user_agent
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
				agent = random.choice(self.user_agent)
				request.headers['User-Agent'] = agent
				#request.meta['proxy'] = "http://1.194.118.17:26086"
