from lxml import html
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'https://proxy-daily.com/'


class ProxydailyCrawler(BaseCrawler):
    urls = [BASE_URL]
    def parse(self, html_content):
        i = html.fromstring(html_content).xpath('//div[@class="centeredProxyList freeProxyStyle"]')[0]
        ip_list = i.xpath('string()').split('\n')
        print('第一个')
        for j in ip_list:
            if len(j) > 4:
                ip = j.split(':')[0]
                port = j.split(':')[1]
                yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    crawler = ProxydailyCrawler()
    for proxy in crawler.crawl(data=crawler.data):
        print(proxy)
