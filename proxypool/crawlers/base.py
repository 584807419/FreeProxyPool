import requests
from loguru import logger

import random

headers = {
    # 'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Pragma': "no-cache",
}

agents_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
]


class BaseCrawler(object):
    urls = []
    data = None

    def fetch(self, url, data=None, **kwargs):
        try:
            headers['User-Agent'] = random.choice(agents_list)
            kwargs["headers"] = headers
            if data:
                response = requests.post(url, data=data, verify=False, timeout=60, **kwargs)
            else:
                response = requests.get(url, verify=False, timeout=60, **kwargs)
            if response.status_code == 200:
                return response.text
            logger.info(f'fetch-status_code：{response.status_code} response.text {response.text}')
        except Exception as e:
            logger.error(f'fetch-error-occur：url {url} e {e}')
            return

    @logger.catch
    def crawl(self, data=None):
        """
        crawl main method
        """
        for url in self.urls:
            logger.info(f'获取代理中 {url}')
            html = self.fetch(url, data=data)
            if html:
                for proxy in self.parse(html):
                    logger.info(f'fetched proxy {proxy.string()} from {url}')
                    yield proxy
