#encoding=utf-8
from scrapy.spiders import Spider
from lxml import html
from plug.utils import NumberUtil,StringUtil
from ershoufang.items import HouseItem
import re
import scrapy
import urllib2

class erShouSpider(Spider):
	name = "ershoufang"
	urlMap = {}
	allowed_domains = [".*58.com"]
	URL = "http://%s.58.com/ershoufang/"
	def start_requests(self):
		urls = []
		text = urllib2.urlopen("http://www.58.com/changecity.html?catepath=ershoufang").read().decode("utf-8")
		cities = re.findall(r'{.*}',text);
		for city in cities[:len(cities)-1]:
			self.urlMap = dict(self.urlMap.items() + eval(city).items())
		for key in self.urlMap:
			print(key+":"+self.urlMap[key])
			self.urlMap[key] = self.urlMap[key].split("|")[0]
			if not self.urlMap[key] or self.urlMap[key] == '':
				continue
			if StringUtil.filtString("http://\S+.58.com/ershoufang/",self.URL%self.urlMap[key]):
				urls.append(scrapy.Request(self.URL%self.urlMap[key]))
				for i in range(70):
					urls.append(scrapy.Request(self.URL%self.urlMap[key]+"pn"+str(i)+"/"))
		self.urlMap = {v:k for k,v in self.urlMap.items()}
		print(len(self.urlMap))
		return urls

	def parseUrls(self,html):
		links = html.xpath(".//a/@href")
		urls = []
		for link in links:
			
			if StringUtil.filtString("http://.+?\.58\.com/ershoufang/pn\d+?/",link):
				urls.append(link)
		return urls

	def parseItems(self,html,response):
		houselist = html.xpath(".//ul[@class='house-list-wrap']//div[@class='list-info']")
		items = []
		for houseinfo in houselist:
			detailurl = houseinfo.xpath(".//h2[1]/a/@href")[0]
			imageurl = houseinfo.xpath("./preceding-sibling::div[1]//a/@href")
			title = "".join(houseinfo.xpath(".//h2[1]/a/text()"))
			roomNum = "".join(houseinfo.xpath(".//p[1]/span[1]/text()")[0].split())
			size = "".join(houseinfo.xpath(".//p[1]/span[2]/text()"))
			orient =  "".join(houseinfo.xpath(".//p[1]/span[3]/text()"))
			floor = "".join(houseinfo.xpath(".//p[1]/span[4]/text()"))
			address = "".join(("".join(houseinfo.xpath(".//p[2]/span[1]//a/text()"))).split())
			sumprice = "".join(houseinfo.xpath("./following-sibling::div[1]//p[@class='sum']/b/text()"))
			unitprice = "".join(houseinfo.xpath("./following-sibling::div[@class='price']//p[@class='unit']/text()"))
			fromUrl= response.url
			key = fromUrl.split("//")[1]
			key = key.split(".")[0]
			city = self.urlMap[key]
			items.append(HouseItem(
										_id = detailurl,
										title = title,
										roomNum = roomNum,
										size = NumberUtil.fromString(size),
										orient = orient,
										floor = floor,
										address = address,
										sumPrice = NumberUtil.fromString(sumprice),
										unitPrice = NumberUtil.fromString(unitprice),
										imageurl = imageurl,
										city = city,
										fromUrl = fromUrl)
									)
		return items
	def printItem(self,item):
		print("房屋出售标题是"+item['title'])
		print("房屋数量是:"+item['roomNum'])
		print("房屋大小是:"+item['size'])
		print("房屋朝向是:"+item['orient'])
		print("房屋楼层是:"+item['floor'])
		print("房屋地址是:"+item['address'])
		print("房屋总价是:"+item['sumPrice'])
		print("房屋均价是:"+item['unitPrice'])
	def parse(self,response):
		if(response.url == 'None'):
			return
		print("开始爬取"+response.url)
		doc = html.fromstring(response.body.decode("utf-8"))
		#urls = self.parseUrls(doc)
		items = self.parseItems(doc,response)
		#for url in urls:
		#	yield scrapy.Request(url,callback=self.parse)
		for item in items:
			yield item
