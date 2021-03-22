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
        items = json.loads(response.body)
        extract = ['date', 'categoryId', 'verticals', 'title', 'priceCents', 'priceType',
                   'sellerName', 'sellerId', 'cityName', 'countryAbbreviation']
        for e in self.find_key(extract, items):
            yield {str(e[0]) : e[1]}
            if 'sellerId' in e[0]:
                sellerId = str(e[1])
            if 'sellerName' in e[0]:
                sellerName = e[1].replace(' ', '-').lower()
                url_seller = ('/u/' + sellerName
                              + '/' + sellerId + '/')
                yield response.follow(url=url_seller, callback=self.parse_seller)

    def parse_seller(self, response):
        user = json.loads(response.xpath('//body').re_first('>\{.*?\}\<')[1:-1])
        extract = ['date', 'categoryId', 'verticals', 'title', 'priceCents', 'priceType',
                   'sellerName', 'sellerId', 'cityName', 'countryAbbreviation']
        for e in self.find_key(extract, user):
            yield {str(e[0]) : e[1]}

    def find_key(self, keys, targ):
        """ Search JSON string `targ` for `keys`, return path and value """
        if isinstance(targ, dict):
            for k, v in targ.items():
                for key in keys:
                    if k == key:
                        yield [[k], v]
                for path, vn in self.find_key(keys, v):
                    yield [[k, *path], vn]
        if isinstance(targ, list):
            for i, v in enumerate(targ):
                for path, vn in self.find_key(keys, v):
                    yield [[i, *path], vn]
