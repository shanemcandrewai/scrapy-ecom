import scrapy
import os
from urllib.parse import urlparse
import json
from stem import Signal
from stem.control import Controller

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        self.url = getattr(self, 'url', None)
        self.new_id(getattr(self, 'pword', None))

        try:
            urlp = urlparse(self.url)
            url_items = (urlp.scheme + '://' + urlp.netloc 
                       + '/lrp/api/search?attributesById[]=' 
                       + urlp.fragment.split('|')[0].split(':')[1]
                       + '&attributesByKey[]=' 
                       + urlp.fragment.split('|')[1].replace(':', '%3A')
                       + '&l1CategoryId=1')
        except IndexError:
            url_items = self.url
        yield scrapy.Request(url=url_items, callback=self.parse)
        
    def parse(self, response):
        try:
            items = json.loads(response.body)
        except json.decoder.JSONDecodeError:
            items = json.loads(response.xpath('//body').re_first(
                '>\{.*?\}\<')[1:-1])
        extract = ['date', 'categoryId', 'verticals', 'title', 'priceCents',
                   'priceType', 'sellerName', 'sellerId', 'cityName',
                   'countryAbbreviation']
        for e in self.find_key(extract, items):
            yield {str(e[0]) : e[1]}
            if 'sellerId' in e[0]:
                sellerId = str(e[1])
            if 'sellerName' in e[0]:
                sellerName = e[1].replace(' ', '-').lower()
                sellerName = sellerName.replace('.', '-')
                sellerName = sellerName.replace('--', '-')
                sellerName = sellerName.replace("'", '')
                if sellerName[-1] == '-':
                    sellerName = sellerName[:-1]
                url_seller = ('/u/' + sellerName + '/' + sellerId + '/')
                yield response.follow(url=url_seller, callback=self.parse)
 #       yield scrapy.Request(url=(self.url + '/p/2/'), callback=self.parse)

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

    def new_id(self, pword):
        with Controller.from_port(port = 9051) as controller:
            controller.authenticate(pword)
            controller.signal(Signal.NEWNYM)
