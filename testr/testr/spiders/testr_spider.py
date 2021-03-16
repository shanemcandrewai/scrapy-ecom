import scrapy
import os
from urllib.parse import urlparse

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        url = getattr(self, 'url', None)
        urlp = urlparse(url)
        url_json = urlp.scheme + '://' + urlp.netloc + '/lrp/api/search?attributesById[]=' + urlp.fragment.split('|')[0].split(':')[1] + '&attributesByKey[]=' + urlp.fragment.split('|')[1].replace(':', '%3A') + '&l1CategoryId=1'
        yield scrapy.Request(url=url_json, callback=self.parse)
        
    def parse(self, response):
        with open('ant.json', 'wb') as f:
            f.write(response.body)
        self.log('xxx json saved')
