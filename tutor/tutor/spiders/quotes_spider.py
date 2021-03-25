import scrapy
import itertools

class QuotesSpider(scrapy.Spider):
    name = "tutor"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        for page_num in range(9, 12):
            self.log(f"xxxxxxxxxxx /page/{page_num}/")
            res = response.follow(f"/page/{page_num}/", callback=self.parse)
            self.log(res.body)
