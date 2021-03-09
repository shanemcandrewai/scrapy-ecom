import scrapy

class QuoteSpider(scrapy.Spider):
    name = "quote"

    def start_requests(self):
        url = getattr(self, 'url', None)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
