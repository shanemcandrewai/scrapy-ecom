import scrapy
from stem import Signal
from stem.control import Controller

class TestrSpider(scrapy.Spider):
    name = "testr"
    count = 0

    def start_requests(self):
        url = getattr(self, 'url', None)
        yield scrapy.Request(url=url, callback=self.parse)
        
        
    def parse(self, response):
        count += 1
        while count < 10:
            with Controller.from_port(port = 9051) as c:
                c.authenticate()
                c.signal(Signal.NEWNYM)
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True))
            self.log(f'Saved file {count}')
