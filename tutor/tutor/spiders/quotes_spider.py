import scrapy
import itertools

class QuotesSpider(scrapy.Spider):
    name = "tutor"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        quotes_sel = response.css('div.quote')
        for quote in quotes_sel:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        if quotes_sel:
            page_ind = response.url.find('page/')
            slash_ind = response.url.rfind('/')
            page_num = response.url[page_ind+5:slash_ind]
            next_num = int(page_num) + 1
            next_page = f"/page/{str(next_num)}"
            yield response.follow(next_page)
