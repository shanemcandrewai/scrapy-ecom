import scrapy
import os
from urllib.parse import urlparse
import json

class TestrSpider(scrapy.Spider):
    name = "testr"
    urlp = ''

    def start_requests(self):
        url = getattr(self, 'url', None)
        self.urlp = urlparse(url)
        url_json = self.urlp.scheme + '://' + self.urlp.netloc + '/lrp/api/search?attributesById[]=' + self.urlp.fragment.split('|')[0].split(':')[1] + '&attributesByKey[]=' + self.urlp.fragment.split('|')[1].replace(':', '%3A') + '&l1CategoryId=1'
        yield scrapy.Request(url=url_json, callback=self.parse)
        
    def parse(self, response):
        with open('ant.json', 'wb') as f:
            f.write(response.body)
        self.log('xxx json saved')
        items = json.loads(response.body)
        yield items
        url_seller = (self.urlp.scheme + '://' + self.urlp.netloc + '/u/'
                     + items['listings'][0]['sellerInformation']['sellerName'].replace(
                         ' ', '-').lower()
                     + '/' + str(items['listings'][0]['sellerInformation']['sellerId']) + '/')
        self.log('xxx ' + url_seller)
        yield scrapy.Request(url=url_seller, callback=self.parse_seller)

    def parse_seller(self, response):
        yield None
