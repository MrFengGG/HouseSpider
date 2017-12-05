#coding=utf-8
import pymongo
import requests
import re
import urllib2
from bs4 import BeautifulSoup
class ProxyUtil(object):
	def __init__(self,testUrl):
		self.testUrl = testUrl
	def vaildate(self,ip,port,contype):
		print("开始验证IP")
		header={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0'}
		proxy=urllib2.ProxyHandler({contype:ip+":"+str(port)})
		opener=urllib2.build_opener(proxy)
		print(self.testUrl)
		self.testUrl = contype + ":" + self.testUrl.split(":")[1] 
		print(self.testUrl)
		urllib2.install_opener(opener)
		rq=urllib2.Request(self.testUrl)
		rq.add_header=[('User-Agent',header['User-Agent'])]
		resp = None
		try:
			resp=urllib2.urlopen(rq,timeout=2)
		except urllib2.URLError as e:
			if hasattr(e,'reason'):
				print e.reason
			if hasattr(e,'code'):
				print e.code
		except:
			return False
		if resp:
 			text=resp.read()
			bs=BeautifulSoup(text,'lxml')
			try:
				print(bs.find('h1',attrs={'id':"ipd"}).get_text())
				print("是否正确"+ip)
			except:
				return False
			return True
		return False	
class ProxyPool(object):

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
if __name__ == "__main__":
	util = ProxyUtil("http://www.ip181.com/")
	util.vaildate("112.114.95.133	8118",8118)
		





