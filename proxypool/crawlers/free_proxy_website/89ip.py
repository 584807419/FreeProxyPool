from lxml import html
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://www.89ip.cn/tqdl.html?api=1&num=100&port=&address=&isp='


class Ip89Crawler(BaseCrawler):
    urls = [BASE_URL]

    def parse(self, html_content):
        doc = html.fromstring(html_content)
        node = doc.xpath('//text()')
        for i in node:
            ii = i.strip().replace('\n', '')
            if ii and len(ii) < 23:
                tr_list = ii.split(':')
                host = tr_list[0]
                port = tr_list[1]
                yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = Ip89Crawler()
    for proxy in crawler.crawl():
        print(proxy)
