import scrapy
import os

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        url = getattr(self, 'url', None)
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        print('xxxxx')
        print(response.url.split('/')[-2] + '.html')
