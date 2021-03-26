import scrapy
import os
from urllib.parse import urlparse
import json

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        self.url = getattr(self, 'url', None)
        yield scrapy.Request(url=self.url, callback=self.parse)
        
    def parse(self, response):
        items = json.loads(response.xpath('//body').re_first(
                '>\{.*?\}\<')[1:-1])
        extract = ['date', 'categoryId', 'verticals', 'title', 'priceCents',
                   'priceType', 'sellerName', 'sellerId', 'cityName',
                   'countryAbbreviation', 'itemId']
        ge = {}
        for e in self.find_key(extract, items):
            ge[str(e[0])] = e[1]
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
                for page in range(2, 10):
                    yield response.follow(url=f"{url_seller}p/{page}/",
                                          callback=self.parse)
        yield ge
        if items:
            page_ind = response.url.find('p/')
            slash_ind = response.url.rfind('/')
            if page_ind == -1:
                page_num = 1
            else:
                page_num = response.url[page_ind+2:slash_ind]
            next_num = int(page_num) + 1
            next_page = f"/p/{str(next_num)}"
            yield scrapy.Request(url=next_page,
                                 callback=self.parse)

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

