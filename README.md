# scrapy ecom 
    scrapy startproject ecom
    cd ecom
    scrapy crawl ecom
    scrapy crawl ecom -a url='http://quotes.toscrape.com'
    scrapy crawl ecom -a url="http://quotes.toscrape.com"
## tor
### Linux
[install tor service](https://2019.www.torproject.org/docs/debian.html.en)
#### To use source lines with https:// in /etc/apt/sources.list
    sudo apt install apt-transport-https
#### Add to /etc/apt/sources.list
    deb https://deb.torproject.org/torproject.org bionic main
    deb-src https://deb.torproject.org/torproject.org bionic main
#### Install tor
    apt install tor
### Windows
#### [download Expert Bundle](http://expyuzz4wqqyqhjn.onion/download/tor/index.html)
#### execute [unzipped bundle location]\Tor\tor.exe
###  [test](https://sylvaindurand.org/use-tor-with-python)
    import requests
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    requests.get('https://ident.me', proxies=proxies).text
    requests.get('https://check.torproject.org', proxies=proxies).text
## [Scrapy over tor](https://blog.michaelyin.info/scrapy-socket-proxy/)
### [Install Privoxy](https://www.privoxy.org/sf-download-mirror/)
### configure privoxy/config, restart
    forward-socks4a / 127.0.0.1:9050 .
### configure scrapy project settings.py
    DOWNLOADER_MIDDLEWARES = {
	'ecom.middlewares.EcomDownloaderMiddleware': 543,
    }
### configure scrapy project middlewares.py
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8118"
        return None
#### test
    scrapy crawl ecom -a url="https://check.torproject.org"
##### check resulting file quotes-.html
    <h1 class="not">
	Congratulations. This browser is configured to use Tor.
    </h1>
    <p>Your IP address appears to be:  <strong>81.6.43.167</strong></p>
      <p class="security">
	However, it does not appear to be Tor Browser.<br />
	<a href="https://www.torproject.org/download/">Click here to go to the download page</a>
    </p>

