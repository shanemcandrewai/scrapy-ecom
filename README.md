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
###  [test](https://sylvaindurand.org/use-tor-with-python)
    import requests
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    requests.get('https://ident.me', proxies=proxies).text
    requests.get('https://check.torproject.org', proxies=proxies).text

