#coding: utf-8
import codecs
import json
import pymongo
from scrapy.utils.project import get_project_settings		

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ershoufang.items import ProxyItem

class ErshoufangPipeline(object):
		def __init__(self):
			self.settings = get_project_settings()
			self.client = pymongo.MongoClient(
				host=self.settings['MONGO_IP'],
				port=self.settings['MONGO_PORT'])
			self.db = self.client[self.settings['MONGO_DB']]
			self.proxyclient = self.proxy = self.client[self.settings['PROXY_DB']][self.settings['POOL_NAME']]
			self.itemNumber = 0
		def process_proxy(self,item):
			self.proxyclient.insert(dict(item))
		def process_item(self, item, spider):
			if isinstance (item,ProxyItem):
				self.process_proxy(item)
				return item
			try:
				if not item['address']:	
					print(item["fromUrl"+"网页异常"])
					return item
				'''
				if self.db.ershoufang.count({"_id":item["_id"],"city":item['city']})<= 0:
					print("删除")
					self.db.ershoufang.remove({"_id":item["_id"]})
				'''
				coll = self.db[self.settings['ALL']]
				coll.insert(dict(item))
				self.itemNumber += 1
				print("爬取到第%s个房屋,地址为%s"%(self.itemNumber,item['address']))
			except Exception,e:
				pass
			return item
		def spider_closed(self,spider):
			self.client.close()
			self.db.close()	
			print("本次爬取共爬取到%s条房屋数据"%self.itemNumber)
