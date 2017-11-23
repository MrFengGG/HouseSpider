#encoding=utf-8
from scrapy.spiders import Spider
from lxml import html
from utils import NumberUtil,StringUtil
from ershoufang.items import HouseItem
import re
import scrapy

class erShouSpider(Spider):
	name = "ershoufang"
	
	allowed_domains = ["wh.58.com"]
	start_urls = ["http://wh.58.com/ershoufang/"]
	
	def parseUrls(self,html):
		links = html.xpath(".//a/@href")
		urls = []
		for link in links:
			#print(link)
			if StringUtil.filtString("http://wh.58.com/ershoufang/pn\d+?/",link):
				
				urls.append(link)
		return urls
	def parseItems(self,html):
		houselist = html.xpath(".//ul[@class='house-list-wrap']//div[@class='list-info']")
		items = []
		for houseinfo in houselist:
			detailurl = houseinfo.xpath(".//h2[1]/a/@href")
			title = "".join(houseinfo.xpath(".//h2[1]/a/text()"))
			roomNum = "".join(houseinfo.xpath(".//p[1]/span[1]/text()")[0].split())
			size = "".join(houseinfo.xpath(".//p[1]/span[2]/text()"))
			orient =  "".join(houseinfo.xpath(".//p[1]/span[3]/text()"))
			floor = "".join(houseinfo.xpath(".//p[1]/span[4]/text()"))
			address = "".join(("".join(houseinfo.xpath(".//p[2]/span[1]//a/text()"))).split())
			sumprice = "".join(houseinfo.xpath("./following-sibling::div[1]//p[@class='sum']/b/text()"))
			unitprice = "".join(houseinfo.xpath("./following-sibling::div[@class='price']//p[@class='unit']/text()"))
			items.append(HouseItem(
										_id = detailurl,
										title = title,
										roomNum = roomNum,
										size = NumberUtil.fromString(size),
										orient = orient,
										floor = floor,
										address = address,
										sumPrice = NumberUtil.fromString(sumprice),
										unitPrice = NumberUtil.fromString(unitprice))
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
		print("开始爬取%s"%response.url)
		doc = html.fromstring(response.body.decode("utf-8"))
		urls = self.parseUrls(doc)
		items = self.parseItems(doc)
		for url in urls:
			yield scrapy.Request(url,callback=self.parse)
		for item in items:
			yield item
