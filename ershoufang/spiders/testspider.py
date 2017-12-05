import scrapy
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
class testSpider(Spider):
	name = 'test'
	start_urls = ["http://ip.filefab.com/index.php"]
	def parse(self,response):
		bs = BeautifulSoup(response.decode("utf-8"),'lxml')
		print("jeghjjjjjjjj:"+bs.find('h1',attrs={'id':"ipd"}).get_text())

		
	
