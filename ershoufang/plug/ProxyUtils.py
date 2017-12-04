#coding=utf-8
import pymongo

class ProxyUtil(object):

	def __init__(self,host,port,db,collection):
		self.size = size
		self.host = host
		self.port = port
		self.client = pymongo.MongoClient(self.host,self.port)
		self.db = self.client[db]
		self.collection = self.db[collection]
	def __del__(self):
		self.client.close()

	def getProxys(self,size = None):
		if size:
			return self.collection.find().limit(size)
		return self.collection.find()
		
		





