import re
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler


class xilaCrawler(BaseCrawler):
    urls = ['http://www.xiladaili.com/http/', 'http://www.xiladaili.com/http/2/', 'http://www.xiladaili.com/http/3/',
            'http://www.xiladaili.com/http/4/', 'http://www.xiladaili.com/http/5/', 'http://www.xiladaili.com/http/6/']

    def parse(self, html_content):
        ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html_content)
        for i in ips:
            ip_temp = i.split(':')
            host = ip_temp[0]
            port = ip_temp[1]
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = xilaCrawler()
    for proxy in crawler.crawl():
        print(proxy)
