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
#### Linux
    scrapy crawl quote -a url="http://quotes.toscrape.com"
#### Windows
    scrapy crawl quote -a url='http://quotes.toscrape.com'
### Resume scrape and append to csv
    scrapy crawl quote -s JOBDIR=crawls -a url='https://www.example.com' -o mp.csv 2> error.log
## Tor
### [Linux](https://2019.www.torproject.org/docs/debian.html.en)
#### To use source lines with https in /etc/apt/sources.list
    sudo apt install apt-transport-https
#### Add to /etc/apt/sources.list
    deb https://deb.torproject.org/torproject.org bionic main
    deb-src https://deb.torproject.org/torproject.org bionic main
#### Install tor
    apt install tor
### Windows
#### [Download Expert Bundle](http://expyuzz4wqqyqhjn.onion/download/tor/index.html)
#### Execute [unzipped bundle location]\Tor\tor.exe
###  [Test procedure](https://sylvaindurand.org/use-tor-with-python)
    import requests
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    requests.get('https://check.torproject.org', proxies=proxies).text
#### Expected response
    Congratulations. This browser is configured to use Tor.
    However, it does not appear to be Tor Browser.
### Alternative test
    requests.get('https://ident.me', proxies=proxies).text
## [Scrapy over Tor](https://blog.michaelyin.info/scrapy-socket-proxy/)
### [Install Privoxy](https://www.privoxy.org/)
### Linux
    sudo apt-get install privoxy
### Windows
[Download installer](https://www.privoxy.org/sf-download-mirror/)
### Configure privoxy/config, restart
    forward-socks5t   /               127.0.0.1:9050 .
#### Privoxy Fatal error: init_error_log(): can't open logfile: '.\privoxy.log'
##### Solution
Launch privoxy as admin
### Configure scrapy project settings.py
    DOWNLOADER_MIDDLEWARES = {
        'quote.middlewares.EcomDownloaderMiddleware': 543,
    }
#### [Set user agent](https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-USER_AGENT)
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
### Configure scrapy project middlewares.py
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8118"
        return None
#### Test procedure
##### Linux
    scrapy crawl quote -a url='https://check.torproject.org'
##### Windows
    scrapy crawl quote -a url="https://check.torproject.org"
##### Check resulting file quotes-.html
    <h1 class="not">
	Congratulations. This browser is configured to use Tor.
    </h1>
    <p>Your IP address appears to be:  <strong>81.6.43.167</strong></p>
      <p class="security">
	However, it does not appear to be Tor Browser.<br />
	<a href="https://www.torproject.org/download/">Click here to go to the download page</a>
    </p>
### [Tor ControlPort](https://stem.torproject.org/tutorials/the_little_relay_that_could.html)
#### torrc
    ControlPort 9051
    HashedControlPassword 16:D536B2E43265F0E660376B92BC8BF056D6DD4A390D3ACB4C311A41E1C9
#### Reload torrc
    pkill -sighup tor
#### [Request new identity](https://stem.torproject.org/faq.html#how-do-i-request-a-new-identity-from-tor)
    from stem import Signal
    from stem.control import Controller

    with Controller.from_port(port = 9051) as controller:
      controller.authenticate([password in quotes])
      controller.signal(Signal.NEWNYM)
### [Parsing JavaScript code](https://docs.scrapy.org/en/latest/topics/dynamic-content.html?highlight=re_first#parsing-javascript-code)
#### [regex test online](https://regex101.com)
#### Select json content
    \{(?:[^{}]|(?R))*\}
#### Select between `>{` and `}<`
    pat = '>\{.*?\}\<'
    js = response.xpath('//body').re_first(pat)[1:-1]
    jsp = json.loads(js)
####   [Search for keys in nested compound data structures](https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists)
    def find_key(self, keys, targ):
        """ Search JSON string `targ` for `keys`, return path and value """
        if isinstance(targ, dict):
            for k, v in targ.items():
                for key in keys:
                    if k == key:
                        yield [[k], v]
                for path, vn in find_key(keys, v):
                    yield [[k, *path], vn]
        if isinstance(targ, list):
            for i, v in enumerate(targ):
                for path, vn in find_key(keys, v):
                    yield [[i, *path], vn]
##### Examples
    listings = jsp['props']['pageProps']['searchRequestAndResponse']['listings']
    list(find_key(['itemId', 'title'], listings))
#### [How to convert string representation of list to a list](https://stackoverflow.com/questions/1894269/how-to-convert-string-representation-of-list-to-a-list)

    import ast
    npm = []
    for m in mp:
        for k, v in m.items():
            kl = ast.literal_eval(k)
            kl.append(v)
            npm.append(kl)

