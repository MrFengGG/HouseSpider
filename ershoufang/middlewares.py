# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import sys
sys.path.append("spiders")
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import http
from scrapy import signals
import pymongo
from plug.ProxyUtils import ProxyUtil 
import random
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
		self.vaildate = ProxyUtil("http://ip.filefab.com/index.php")
		self.settings = get_project_settings()
		self.client = pymongo.MongoClient(
								host = self.settings['MONGO_IP'],
								port = self.settings['MONGO_PORT'])
		self.db = self.client[self.settings['PROXY_DB']]
		self.col = self.db[self.settings['POOL_NAME']]
		self.initProxy()
	def initProxy(self):
		if self.col.count() > 0:
			contents = self.col.find().limit(10)
			for content in contents:
				if not self.vaildate.vaildate(content['ip'],
																			content['port'],
																			content['contype']):
					self.col.remove({"_id":content["_id"]})
					print("delete a ip")
				else:
					print("验证通过")
			print("目前IP池中有可用的代理IP%s条"%self.col.count())
	@classmethod
	def from_crawler(cls, crawler):
		return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

	def process_request(self, request, spider):
		agent = random.choice(self.user_agent)
		request.headers['User-Agent'] = agent

		if self.col.count() > 0:
			contents = list(self.col.find().limit(10))
			content = random.choice(contents)
			print("使用代理IP")
			request.meta['proxy'] = content['contype']+"://"+content['ip']+":"+str(content['port'])
		else:
			pass
				#request.meta['proxy'] = "http://1.194.118.17:26086"
	
