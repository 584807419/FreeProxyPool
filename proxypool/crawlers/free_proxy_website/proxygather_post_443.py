from lxml import html
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://proxygather.com/zh/proxylist/port/443'


class Proxygather443Crawler(BaseCrawler):
    urls = [BASE_URL]
    data = {
        'Filter': '',
        'Uptime': '50',
        'Port': '443',
    }

    def parse(self, html_content):
        for i in html.fromstring(html_content).xpath('//div[@class="proxy-list"]/table/tr/td/script/text()'):
            ip = i.split("')")[0].split("\'")[1]
            if len(ip) > 4:
                yield Proxy(host=ip, port='443')


if __name__ == '__main__':
    crawler = Proxygather443Crawler()
    for proxy in crawler.crawl(data=crawler.data):
        print(proxy)
