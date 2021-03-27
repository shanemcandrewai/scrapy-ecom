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
        extract_fields = ['date', 'categoryId', 'verticals', 'title', 'priceCents',
                   'priceType', 'sellerName', 'sellerId', 'cityName',
                   'countryAbbreviation', 'itemId']

        if '/u/' not in response.url:
            seller_items = {}
            for cat_item in self.find_key(extract_fields, items):
                seller_items[str(cat_item[0])] = cat_item[1]
                if 'sellerId' in cat_item[0]:
                    sellerId = str(cat_item[1])
                if 'sellerName' in cat_item[0]:
                    sellerName = cat_item[1].replace(' ', '-').lower()
                    sellerName = sellerName.replace('.', '-')
                    sellerName = sellerName.replace('--', '-')
                    sellerName = sellerName.replace("'", '')
                    if sellerName[-1] == '-':
                        sellerName = sellerName[:-1]
                    url_seller = ('/u/' + sellerName + '/' + sellerId + '/')

                    if response.follow(url=url_seller, callback=self.parse):
                        self.log(f"xxxxx {url_seller}")
                        np = self.get_next_page_url(response.url)
                        self.log(f"xxxxx {np}")
                        yield scrapy.Request(url=np,
                                             callback=self.parse)
            yield seller_items
        if items:
            yield scrapy.Request(url= self.get_next_page_url(response.url),
                                 callback=self.parse)

    def get_next_page_url(self, url):
        page_ind = url.find('p/') - 1
        slash_ind = url.rfind('/')
        if page_ind == -1:
            page_num = 1
        else:
            page_num = url[page_ind+2:slash_ind]
        next_num = int(page_num) + 1
        return f"{url[:page_ind]}/p/{str(next_num)}/"

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

