import re
import requests
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import IhuanBaseCrawler

BASE_URL = 'https://ip.ihuan.me/mouse.do'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Referer': 'https://ip.ihuan.me/ti.html'}
cookies = {'statistics': 'db1fd09d3852aaa0ada1a473309c178d',
           'Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829': '1569338278,1569338412,1569338416',
           'Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829': '1569375327'}


class IhuanCrawler(IhuanBaseCrawler):
    urls = [BASE_URL]
    cookies = cookies
    headers = headers

    def parse(self, html_content):
        key = re.match(r'.*val\("(.*?)".*', html_content).group(1)
        data = {"num": 100, "sort": 1, "key": key}
        response = requests.post('https://ip.ihuan.me/tqdl.html', data, headers=IhuanCrawler.headers, cookies=IhuanCrawler.cookies, verify=False)
        ips = re.match(r'.*</div><div class="panel-body">(.*?)</div>.*', response.text).group(1).split('<br>')
        print(ips)
        for proxy in ips:
            if len(proxy) < 22 and len(proxy) > 0:
                _iplist = proxy.split(':')
                print(_iplist)
                yield Proxy(host=_iplist[0], port=_iplist[1])


if __name__ == '__main__':
    crawler = IhuanCrawler()
    for proxy in crawler.crawl(crawler.data, crawler.headers, crawler.cookies):
        print(proxy)
