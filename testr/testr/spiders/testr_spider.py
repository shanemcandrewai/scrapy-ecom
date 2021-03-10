import scrapy
from stem import Signal
from stem.control import Controller
from time import sleep

class TestrSpider(scrapy.Spider):
    name = 'testr'
    count = 0

    def start_requests(self):
        url = getattr(self, 'url', None)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        
    def parse(self, response):
        sleep(10)
        self.log(f'Saved file {TestrSpider.count}')
        with Controller.from_port(port = 9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
        TestrSpider.count += 1
        filename = f'{TestrSpider.count}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(response.url)
