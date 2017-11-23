#coding: utf-8
import codecs
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ErshoufangPipeline(object):
		def __init__(self):
			self.file = codecs.open("hose.json","w",encoding="utf-8")
		def process_item(self, item, spider):
			lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
			self.file.write(lines)
			return item
		def spider_closed(self,spider):
			self.file.close()	
