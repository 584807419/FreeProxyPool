import time
import multiprocessing
from proxypool.processors.server import app
from proxypool.processors.getter import Getter
from proxypool.processors.tester import Tester
from proxypool.setting import CYCLE_GETTER, CYCLE_TESTER, API_HOST, API_THREADED, API_PORT, ENABLE_SERVER, \
    ENABLE_GETTER, ENABLE_TESTER, IS_WINDOWS
from loguru import logger


if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class Scheduler():
    """
    scheduler
    """
    
    def run_tester(self, cycle=CYCLE_TESTER):  # 每隔CYCLE_TESTER秒跑下一轮
        """
        run tester
        """
        if not ENABLE_TESTER:
            logger.info('tester not enabled, exit')
            return
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)
    
    def run_getter(self, cycle=CYCLE_GETTER):
        """
        run getter
        """
        if not ENABLE_GETTER:
            logger.info('getter not enabled, exit')
            return
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)
    
    def run_server(self):
        """
        run server for api
        """
        if not ENABLE_SERVER:
            logger.info('server not enabled, exit')
            return
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
    
    def run(self):
        global tester_process, getter_process, server_process
        try:
            logger.info('starting proxypool...')
            if ENABLE_TESTER:
                # 创建一个 Process 对象然后调用它的 start () 方法来生成进程
                tester_process = multiprocessing.Process(target=self.run_tester)  # 检测代理可用性
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if ENABLE_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)  # 调用接口获取代理IP数据
                logger.info(f'starting getter, pid{getter_process.pid}...')
                getter_process.start()
            
            if ENABLE_SERVER:
                server_process = multiprocessing.Process(target=self.run_server)  # 提供http服务
                logger.info(f'starting server, pid{server_process.pid}...')
                server_process.start()

            tester_process.join()  # 一般都先让子线程调用start() ，然后再去调用join()，让主进程等待子进程结束才继续走后续的逻辑。
            getter_process.join()
            server_process.join()
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            tester_process.terminate()  # 杀死子进程
            getter_process.terminate()
            server_process.terminate()
        finally:
            # must call join method before calling is_alive
            tester_process.join()
            getter_process.join()
            server_process.join()
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')  # 查看的子进程结果 是否存活
            logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            logger.info(f'server is {"alive" if server_process.is_alive() else "dead"}')
            logger.info('proxy terminated')


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
