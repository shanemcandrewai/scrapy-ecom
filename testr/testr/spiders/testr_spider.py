import scrapy
import os

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        url = getattr(self, 'url', None)
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        with open('ant.json', 'wb') as f:
            f.write(response.body)
        self.log('xxx json saved')
