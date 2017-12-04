#coding: utf-8
import codecs
import json
import pymongo
from scrapy.utils.project import get_project_settings		

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ErshoufangPipeline(object):
		def __init__(self):
			self.settings = get_project_settings()
			self.client = pymongo.MongoClient(
				host=self.settings['MONGO_IP'],
				port=self.settings['MONGO_PORT'])
			self.db = self.client[self.settings['MONGO_DB']]
			self.coll = self.db[self.settings['CITY']]
	
		def process_item(self, item, spider):
			try:
				if not item['address']:	
					print(item["fromUrl"+"网页异常"])
					return item
				'''
				if self.db.ershoufang.count({"_id":item["_id"],"city":item['city']})<= 0:
					print("删除")
					self.db.ershoufang.remove({"_id":item["_id"]})
				'''
				self.coll.insert(dict(item))
				print("插入一个房子"+item['address']+"城市为"+item['city'])
			except Exception,e:
				print(item['address']+'已经存在城市是'+item['city'])
			return item
		def spider_closed(self,spider):
			self.client.close()
			self.db.close()	
