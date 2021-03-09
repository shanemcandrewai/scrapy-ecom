# [Scrapy quote](https://docs.scrapy.org/en/latest/intro/tutorial.html)
## Create new project
    scrapy startproject quote
    cd quote
## Create spider quote/spiders/quote_spider.py
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
### Test procedure
    scrapy crawl quote -a url='http://quotes.toscrape.com'
    scrapy crawl quote -a url="http://quotes.toscrape.com"
## Tor
### Linux
[Install tor service](https://2019.www.torproject.org/docs/debian.html.en)
#### To use source lines with https in /etc/apt/sources.list
    sudo apt install apt-transport-https
#### Add to /etc/apt/sources.list
    deb https://deb.torproject.org/torproject.org bionic main
    deb-src https://deb.torproject.org/torproject.org bionic main
#### Install tor
    apt install tor
### Windows
#### [Download Expert Bundle](http://expyuzz4wqqyqhjn.onion/download/tor/index.html)
#### execute [unzipped bundle location]\Tor\tor.exe
###  [Test procedure](https://sylvaindurand.org/use-tor-with-python)
    import requests
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    requests.get('https://check.torproject.org', proxies=proxies).text
#### Response
    Congratulations. This browser is configured to use Tor.
    However, it does not appear to be Tor Browser.
### Alternative test
    requests.get('https://ident.me', proxies=proxies).text
## [Scrapy over Tor](https://blog.michaelyin.info/scrapy-socket-proxy/)
### [Install Privoxy](https://www.privoxy.org/)
### Linux
    sudo apt-get install privoxy
### Windows
[Download](https://www.privoxy.org/sf-download-mirror/)
### configure privoxy/config, restart
    forward-socks4a / 127.0.0.1:9050 .
#### Privoxy version 3.0.26
    forward-socks5t   /               127.0.0.1:9050 .
### configure scrapy project settings.py
    DOWNLOADER_MIDDLEWARES = {
	'quote.middlewares.EcomDownloaderMiddleware': 543,
    }
### configure scrapy project middlewares.py
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8118"
        return None
#### Test procedure
    scrapy crawl quote -a url='https://check.torproject.org'
##### check resulting file quotes-.html
    <h1 class="not">
	Congratulations. This browser is configured to use Tor.
    </h1>
    <p>Your IP address appears to be:  <strong>81.6.43.167</strong></p>
      <p class="security">
	However, it does not appear to be Tor Browser.<br />
	<a href="https://www.torproject.org/download/">Click here to go to the download page</a>
    </p>

