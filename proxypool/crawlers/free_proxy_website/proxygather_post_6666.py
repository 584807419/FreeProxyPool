from lxml import html
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://proxygather.com/zh/proxylist/port/6666'


class Proxygather6666Crawler(BaseCrawler):
    urls = [BASE_URL]
    data = {
        'Filter': '',
        'Uptime': '99',
        'Port': '6666',
    }

    def parse(self, html_content):
        for i in html.fromstring(html_content).xpath('//div[@class="proxy-list"]/table/tr/td/script/text()'):
            ip = i.split("')")[0].split("\'")[1]
            if len(ip) > 4:
                yield Proxy(host=ip, port='6666')


if __name__ == '__main__':
    crawler = Proxygather6666Crawler()
    for proxy in crawler.crawl(data=crawler.data):
        print(proxy)
