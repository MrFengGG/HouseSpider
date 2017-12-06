#coding=utf-8
import pymongo
from gevent.pool import Pool
import urllib.request
import json
import urllib.parse
import socket
from gevent import monkey
from parseSettings import *
import gevent
import time
import datetime
monkey.patch_all()	#修改标准库
socket.setdefaulttimeout(2) 
class LocationParser(object):
	#用于地址解析的类
	def __init__(self,ak,baseUrl):
		self.ak = ak
		self.baseUrl = baseUrl
	def parse(self,address,output,city=None):
		#通过api获取json数据
		url = self.baseUrl+"?ak="+self.ak+"&address="+urllib.parse.quote(address)+"&output="+output
		if city:
			url = url + "&city="+urllib.parse.quote(city)
		try:
			result = urllib.request.urlopen(url)
		except:
			print("连接错误")
			return None,url
		jsonresult = json.load(result)
		return jsonresult,url

class LocationDumper():
	def __init__(self,ip,port,locationDB,locationCol,sourceDB,sourceCol,requestNum = 10,city = None):
		#数据库连接
		self.client = pymongo.MongoClient(ip,port)
		#地址解析器
		self.bParser = LocationParser("vxc9SN7XHCI1M6y8djyBD98Upx5CCprX",
																  "http://api.map.baidu.com/geocoder/v2/")
		#并发数量控制
		self.requestNum = requestNum
		#带解析数据集合
		self.sourceCol = self.client[sourceDB][sourceCol]
		#用于存储结果的集合
		self.locationCol = self.client[locationDB][locationCol]
		self.oklength = 0
		self.errorlength = 0
	#用于解析每一条数据的方法
	def parseData(self,data):
		#数据集中没有带解析的数据,解析该条数据
		if self.locationCol.count({"_id":data["_id"]}) <= 0:
			if self.locationCol.count({"address":data["address"]}) > 0:
				print("同一地址不再解析"+data['address'])
				content = self.locationCol.find_one({"address":data["address"]})
				a = {'_id':data['_id'],
                "size":data['size'],
                "orient":data['orient'],
                "roomNum":data['roomNum'],
                "url":data['fromUrl'],
                "unitPrice":data['unitPrice'],
                "sumPrice":data['sumPrice'],
                "ln":content['ln'],
                "lat":content['lat'],
                "address":data['address'],
                "time":data['nowTime'],
                "city":data['city']}

				self.locationCol.insert(a)
				self.sourceCol.update({"_id":data["_id"]},{"$set":{"status":"OK"}})

				return
			result = self.bParser.parse(data["address"],"json",data["city"])
			#根据返回码判断解析结果是否正确,如果不正确,去掉城市参数重试
			if result[0] and result[0]['status'] != 0:
				result = self.bParser.parse(data["address"],"json")
			if not result[0]:
				return
			jsonResult = result[0]
			urlResult = result[1]
			ln = None
			lat = None
			if jsonResult['status'] == 0:
				ln = jsonResult['result']['location']['lng']
				lat = jsonResult['result']['location']['lat']
			else:
				try:
					print("地址解析错误,status:"+str(jsonResult['status'])+",msg:"+jsonResult['msg']+",errorUrl:"+urlResult)
					self.sourceCol.update({"_id":data["_id"]},{"$set":{"status":"ERROR"}})
					self.errorlength += 1
				except:
					print("没有错误信息,直接输出信息"+str(jsonResult))
				return
			try:
					a = {'_id':data['_id'],
								"size":data['size'],
								"orient":data['orient'],
								"roomNum":data['roomNum'],
								"url":data['fromUrl'],
								"unitPrice":data['unitPrice'],
								"sumPrice":data['sumPrice'],
								"ln":ln,
								"lat":lat,
								"address":data['address'],
								"time":data['nowTime'],
								"city":data['city']}	
			except:
				print("存储数据异常,检查该条数据sumprice:"+data['sumPrice']+data['address'])
				self.sourceCol.update({"_id":data["_id"]},{"$set":{"status":"ERROR    "}})
				return
			self.locationCol.insert(a)
			self.oklength += 1
			print("成功插入第%s条数据,解析的地址为:%s"%(self.oklength,data['address']))
			self.sourceCol.update({"_id":data['_id']},{"$set":{"status":"OK"}})	
		else:
			self.sourceCol.update({"_id":data['_id']},{"$set":{"status":"OK"}})	
			print("已经存在,不需要解析,状态设置为以解析")
	#解析main方法
	def parse(self,Number = None):
		pool=gevent.pool.Pool(self.requestNum)
		datas = self.sourceCol.find({"status":"SUBSPENDING"})
		if Number:
			datas = datas.limit(Number)
		for data in datas:
			greenlet = gevent.spawn(self.parseData,data)
			pool.add(greenlet)
		pool.join()
		print("解析完毕,共成功%s条,失败%s条"%(self.oklength,self.errorlength))
	def __del(self):
		self.client.close()
if __name__ == "__main__":
		
	starttime = datetime.datetime.now()
	d = LocationDumper(MONGO_IP,
										 MONGO_PORT,
									   LOCATION_DB,
									   LOCATION_COLL,
									   SOURCE_DB,
								     SOURCE_COLL,
											requestNum = REQUEST_NUM)
	d.parse()
	endtime = datetime.datetime.now()
	rint((endtime-starttime).seconds)
