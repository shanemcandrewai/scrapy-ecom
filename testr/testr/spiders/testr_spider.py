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
                          'countryAbbreviation', 'itemId',
                          'periodSinceRegistrationDate', 'score', 'count']

        listings = items['props']['pageProps']['searchRequestAndResponse']['listings']
        if '/l/' in response.url:
            for cat_item in listings:
                sellerId = None
                sellerName = None
                for cat_field in self.find_key(extract_fields, cat_item):
                    if cat_field[0][-1] == 'sellerId':
                        sellerId = str(cat_field[1])
                    if cat_field[0][-1] == 'sellerName':
                        sellerName = cat_field[1].replace(' ', '-').lower()
                        sellerName = sellerName.replace('.', '-')
                        sellerName = sellerName.replace('--', '-')
                        sellerName = sellerName.replace("'", '')
                        if sellerName[-1] == '-':
                            sellerName = sellerName[:-1]
                if sellerId is not None and sellerName is not None:
                    url_seller = ('/u/' + sellerName + '/' + sellerId + '/')
                    urlp = urlparse(response.url)._replace(path=url_seller)
                    yield scrapy.Request(url=urlp.geturl(), callback=self.parse)
        else:
            item_set = {}
            seller = items['props']['seller']
            for cat_item in listings:
                for cat_field in self.find_key(extract_fields, seller):
                    item_set[str(cat_field[0][-1])] = cat_field[1]
                for cat_field in self.find_key(extract_fields, cat_item):
                    item_set[str(cat_field[0][-1])] = cat_field[1]
                yield item_set
                item_set = {}

        self.log(f'xxx {response.url}')
        self.log(f'xx2 {len(listings)}')
        if len(listings) > 0:
            np = self.get_next_page_url(response.url)
            self.log(f'xx3 {np}')
            yield scrapy.Request(url=np, callback=self.parse)

    def get_next_page_url(self, url):
        page_ind = url.find('/p/')
        slash_ind = url.rfind('/')
        if page_ind == -1:
            page_num = 1
        else:
            page_num = url[page_ind+3:slash_ind]
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

