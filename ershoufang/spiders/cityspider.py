#encoding=utf-8
from scrapy.spiders import Spider
from lxml import html
from utils import NumberUtil,StringUtil
from ershoufang.items import HouseItem
import re
import scrapy
from datas import CITYLIST
import time
from scrapy.utils.project import get_project_settings
class erShouSpider(Spider):
	name = "ershoufang2"
	settings = get_project_settings()
	city = settings['CITY']
	cityP = ''
	allowed_domains = ["58.com"]
	fillUrl = [""]
	def start_requests(self):
			result = []
			for pro in CITYLIST:
				if self.city in CITYLIST[pro]:
					print(self.city)
					self.cityP = CITYLIST[pro][self.city].split("|")[0]
					print(self.cityP)
					self.fillUrl[0] = "http://"+self.cityP+".58.com/ershoufang/"
					print(self.fillUrl)
					result.append(scrapy.Request(self.fillUrl[0]))
					return result
			return None
	def parseUrls(self,html):
		links = html.xpath(".//a/@href")
		urls = []
		for link in links:
			#print(link)
			if StringUtil.filtString(self.fillUrl[0]+"pn\d+?/",link):
				
				urls.append(link)
		return urls
	def parseItems(self,html,url):
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
										_id = "".join(detailurl),
										title = title,
										roomNum = roomNum,
										size = NumberUtil.fromString(size),
										orient = orient,
										floor = floor,
										address = address,
										sumPrice = NumberUtil.fromString(sumprice),
										unitPrice = NumberUtil.fromString(unitprice),
										city=self.city,
										fromUrl = url,
										nowTime = time.time(),
										status = False)
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
		if(response.body =='None'):
			print("存在")
			return
		print("开始爬取%s"%response.url)
		doc = html.fromstring(response.body.decode("utf-8"))
		urls = self.parseUrls(doc)
		items = self.parseItems(doc,response.url)
		for url in urls:
			yield scrapy.Request(url,callback=self.parse)
		for item in items:
			yield item

