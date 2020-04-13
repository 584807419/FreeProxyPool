import json
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://proxy.1again.cc:35050/api/v1/proxy/'


class again1Crawler(BaseCrawler):
    urls = [BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL,
            BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL,
            BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL,
            BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL,
            BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL, BASE_URL,
            ]

    def parse(self, html_content):
        i = json.loads(html_content).get('data').get('proxy')
        if i and len(i) < 23:
            tr_list = i.split(':')
            host = tr_list[0]
            port = tr_list[1]
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = again1Crawler()
    for proxy in crawler.crawl():
        print(proxy)
