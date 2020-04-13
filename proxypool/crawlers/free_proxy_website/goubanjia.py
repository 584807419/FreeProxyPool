from lxml import html
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://www.goubanjia.com/'
val = 'ABCDEFGHIZ'


class GouBanJiaCrawler(BaseCrawler):
    urls = [BASE_URL]

    def parse(self, html_content):
        doc = html.fromstring(html_content)
        node = doc.xpath('//div[@class="container-fluid"]/div/div/table/tbody/tr/td[@class="ip"]')
        for i in node:
            for j in i.xpath('*[contains(@style, "none")]'):
                i.remove(j)
            tr_list = i.xpath('string()').split(':')
            port = int("".join([str(val.find(letter)) for letter in
                                i.xpath('*[contains(@class, "port")]/@class')[0].split(' ')[1]])) >> 0x3
            yield Proxy(host=tr_list[0], port=port)


if __name__ == '__main__':
    crawler = GouBanJiaCrawler()
    for proxy in crawler.crawl():
        print(proxy)
