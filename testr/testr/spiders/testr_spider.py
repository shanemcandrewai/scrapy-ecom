import scrapy
from stem import Signal
from stem.control import Controller

class TestrSpider(scrapy.Spider):
    name = "testr"

    def start_requests(self):
        with Controller.from_port(port = 9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
        url = getattr(self, 'url', None)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
