#coding=utf-8
import sys
from scrapy.spiders import Spider
from lxml import html
import time
import scrapy
from ershoufang.items import ProxyItem
from plug.ProxyUtils import ProxyUtil 
from scrapy.utils.project import get_project_settings
class proxySpider(Spider):
	name = "proxyspider"
	allowed_domains = ["xicidaili.com"]
	def __init__(self):
		super(proxySpider,self)
		self.settings = get_project_settings()
		self.size = self.settings['SIZE']
		self.vaildate = ProxyUtil("http://ip.filefab.com/index.php")
		self.OKcount = 0
		self.Errorcount = 0
	def start_requests(self):
		requests = []
		url = "http://www.xicidaili.com/nn"
		requests.append(scrapy.Request(url))
		for i in range(2,self.size):
			requests.append(scrapy.Request(url+str(i)))
		return requests
	def parseProxy(self,text,url):
		doc = html.fromstring(text)
		maincontents = doc.xpath(".//table[@id='ip_list']//tr[@class]")
		items = []
		for maincontent in maincontents:
			ip = "".join(maincontent.xpath(".//td[2]/text()"))
			port = int("".join(maincontent.xpath(".//td[3]/text()")))
			contype = "".join(maincontent.xpath(".//td[6]/text()")).lower()
			if contype == 'https':
				print("舍弃https")
				continue
			nowtime = time.time()
			if self.vaildate.vaildate(ip,port,contype):
				print("完美的IP"+contype+"://"+ip+":"+str(port))
				items.append(ProxyItem(
											_id = ip + str(port),
											ip = ip,
											port = port,
											contype = contype,
											nowtime = nowtime
											))
			else:
				print("IP不可用"+contype+"://"+ip+":"+str(port))
		return items
	def parse(self,response):
		text = response.body.decode("utf-8")
		items = self.parseProxy(text,response.url)
		for item in items:
			yield item
		
