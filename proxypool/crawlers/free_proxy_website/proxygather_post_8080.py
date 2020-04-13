from lxml import html
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://proxygather.com/zh/proxylist/port/8080'



class Proxygather8080Crawler(BaseCrawler):
    urls = [BASE_URL]
    data = {
        'Filter': '',
        'Uptime': '99',
        'Port': '8080',
    }

    def parse(self, html_content):
        for i in html.fromstring(html_content).xpath('//div[@class="proxy-list"]/table/tr/td/script/text()'):
            ip = i.split("')")[0].split("\'")[1]
            if len(ip) > 4:
                yield Proxy(host=ip, port='8080')


if __name__ == '__main__':
    crawler = Proxygather8080Crawler()
    for proxy in crawler.crawl(data=crawler.data):
        print(proxy)
