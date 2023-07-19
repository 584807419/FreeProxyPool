from proxypool.scheduler import Scheduler
import argparse

parser = argparse.ArgumentParser(description='ProxyPool')
parser.add_argument('--processor', type=str, help='processor to run')  # 可以命令行指定参数：server getter  tester
args = parser.parse_args()

if __name__ == '__main__':
    # if processor set, just run it
    if args.processor:
        getattr(Scheduler(), f'run_{args.processor}')()  # 执行命令行指定的processor(server getter  tester)
    else:
        Scheduler().run()  # 多进程执行所有的processor(server getter  tester)


# 核心：维护一个有序集合
# 弃用之前的加减分方案，改用是否留存方案，避免分数低的无法使用却被调用