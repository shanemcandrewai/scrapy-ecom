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
#        with Controller.from_port(port = 9051) as c:
#            c.authenticate()
#            c.signal(Signal.NEWNYM)
        while TestrSpider.count < 10:
            TestrSpider.count += 1
            filename = f'{TestrSpider.count}.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {TestrSpider.count}')
#            self.log('xxx', response.url)
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
