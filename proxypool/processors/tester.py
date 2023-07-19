import asyncio
import aiohttp
import random
from loguru import logger
from proxypool.schemas import Proxy
from proxypool.storages.redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError, ClientResponseError
from asyncio import TimeoutError


EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    ClientResponseError
)


class Tester(object):
    """
    tester for testing proxies in queue
    """
    
    def __init__(self):
        """
        init redis
        """
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()
    
    async def test(self, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        headers = {
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        }
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                # logger.debug(f'testing {proxy.string()}')
                # async with session.get(f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                #                       allow_redirects=False) as response:
                async with session.get(random.choice(TEST_URL), proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,  # 随机选择url去访问
                                      allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:  # 请求正常分数加满
                        self.redis.max(proxy)
                        #logger.debug(f'proxy {proxy.string()} is valid, set max score')
                    else:
                        self.redis.decrease(proxy)  # 请求不正常 zrem 从有序集合中移除
                        #logger.debug(f'proxy {proxy.string()} is invalid, decrease score')
            except EXCEPTIONS:
                self.redis.decrease(proxy)
                #logger.debug(f'proxy {proxy.string()} is invalid, decrease score')
    
    @logger.catch
    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info('stating tester...')
        count = self.redis.count()  # 看看 有序集合中还剩下多少个代理
        # logger.debug(f'{count} proxies to test')
        for i in range(0, count, TEST_BATCH):  # 从0到count分批取出来，每批次TEST_BATCH个
            # start end end offset
            start, end = i, min(i + TEST_BATCH, count)
            logger.debug(f'testing proxies from {start} to {end} indices')
            proxies = self.redis.batch(start, end)  # 返回有序集中指定区间内的代理，通过索引，分数从高到低
            if proxies:
                tasks = [self.test(proxy) for proxy in proxies]  # 挨个代理去做测试
                # run tasks using event loop
                self.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    tester.run()
