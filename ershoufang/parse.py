#coding=utf-8
import pymongo
import urllib.request
import json
import urllib.parse
from parseSettings import * 
class LocationParser(object):
	#用于地址解析的类
	def __init__(self,ak,baseUrl):
		self.ak = ak
		self.baseUrl = baseUrl
	def parse(self,address,output,city):
		#通过api获取json数据
		url = self.baseUrl+"?ak="+self.ak+"&address="+urllib.parse.quote(address)+"&city="+urllib.parse.quote(city)+"&output="+output
		result = urllib.request.urlopen(url)
		jsonresult = json.load(result)
		return jsonresult

class dumpLocation():
	def __init__(self,ip,port):
		self.client = pymongo.MongoClient(ip,port)
		self.bParser = LocationParser("vxc9SN7XHCI1M6y8djyBD98Upx5CCprX",
																  "http://api.map.baidu.com/geocoder/v2/")
	
	def getDatas(self,dbName,colName):
		col = self.client[dbName][colName]
		datas = col.find({"status":False})
		return datas
	def parse(self,city,location):
		datas = self.getDatas("ershoufang",city)
		col = self.client["ershoufang"][location]
		for data in datas:
			if col.count({"_id":data["_id"]}) <= 0:
				jsonResult = self.bParser.parse(data["address"],"json",data["city"])
				ln = None
				lat = None
				try:
					ln = jsonResult['result']['location']['lng']
					lat = jsonResult['result']['location']['lat']
				except:
					print("地址解析错误")
					continue
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
					print("存储数据异常,删除该条数据")
					self.client['ershoufang'][city].remove({"_id":data['_id']})
					continue
				col.insert(a);
				print("成功插入一条数据"+data['address'])
			else:
				self.client['ershoufang'][city].update({"_id":data['_id']},{"$set":{"status":True}})	
				print("已经存在,不需要解析,添加状态信息")
	def __del(self):
		self.client.close()

if __name__ == "__main__":
	d = dumpLocation("127.0.0.1",27017)
	d.parse("武汉","location")

