from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy


class KuaidailiCrawler(BaseCrawler):
    # urls = ['http://ent.kdlapi.com/api/getproxy/?orderid=950753676261960&num=100&protocol=2&method=2&an_an=1&an_ha=1&sp1=1&quality=2&sort=2&sep=1']
    urls = ['http://ent.kdlapi.com/api/getproxy/?orderid=950753676261960&num=200&sort=2&sep=1']

    def parse(self, html):
        proxies_list = html.split("\r\n")
        for item in proxies_list:
            td_ip = item.split(':')[0]
            td_port = item.split(':')[1]
            yield Proxy(host=td_ip, port=td_port)


if __name__ == '__main__':
    crawler = KuaidailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
