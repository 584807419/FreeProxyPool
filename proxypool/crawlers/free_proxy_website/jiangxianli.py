import json
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'https://ip.jiangxianli.com/api/proxy_ips'


class jiangxianliCrawler(BaseCrawler):
    urls = [BASE_URL]

    def parse(self, html_content):
        i_list = json.loads(html_content).get('data').get('data')
        for i in i_list:
            if i and len(i) < 23:
                host = i.get('ip')
                port = i.get('port')
                yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = jiangxianliCrawler()
    for proxy in crawler.crawl():
        print(proxy)
