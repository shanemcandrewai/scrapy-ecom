import scrapy
import os
from urllib.parse import urlparse
import json

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        urlp = urlparse(getattr(self, 'url', None))
        url_json = (urlp.scheme + '://' + urlp.netloc 
                   + '/lrp/api/search?attributesById[]=' 
                   + urlp.fragment.split('|')[0].split(':')[1]
                   + '&attributesByKey[]=' 
                   + urlp.fragment.split('|')[1].replace(':', '%3A')
                   + '&l1CategoryId=1')
        yield scrapy.Request(url=url_json, callback=self.parse)
        
    def parse(self, response):
        urlp = urlparse(response.url)
        items = json.loads(response.body)
        extract = ['itemId', 'title', 'sellerName', 'sellerId']
        ext_it = list(self.find_key(extract, items))
        self.log(ext_it)

        for k, v in ext_it.items():
            url_seller = (urlp.scheme + '://' + urlp.netloc + '/u/'
                     + items['listings'][0]['sellerInformation'][
                         'sellerName'].replace( ' ', '-').lower()
                     + '/' + str(items['listings'][0]['sellerInformation'][
                         'sellerId']) + '/')
        self.log('xxx ' + url_seller)
        yield scrapy.Request(url=url_seller, callback=self.parse_seller)

    def parse_seller(self, response):
        yield None

    def find_key(self, keys, targ):
        if isinstance(targ, dict):
            for k, v in targ.items():
                for key in keys:
                    if k == key:
                        yield [k], v
                for path, vn in self.find_key(keys, v):
                    yield [k, *path], vn
        if isinstance(targ, list):
            for i, v in enumerate(targ):
                for path, vn in self.find_key(keys, v):
                    yield [i, *path], vn
