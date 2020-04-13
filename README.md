# FreeProxyPool

![](https://img.shields.io/badge/python-3.6%2B-brightgreen)

简易高效的代理池，提供如下功能：

* 定时抓取免费代理网站，简易可扩展。
* 使用 Redis 对代理进行存储并对代理可用性进行排序。
* 定时测试和筛选，剔除不可用代理，留下可用代理。
* 提供代理 API，随机取用测试通过的可用代理。

代理池原理解析可见「[如何搭建一个高效的代理池](https://cuiqingcai.com/7048.html)」，建议使用之前阅读。


### 运行代理池
1. 配置好redis

2. 两种方式运行代理池，一种是 Tester、Getter、Server 全部运行，另一种是按需分别运行。

一般来说可以选择全部运行，命令如下：

```shell script
python3 run.py
```

运行之后会启动 Tester、Getter、Server，这时访问 [http://localhost:8000/random](http://localhost:8000/random) 即可获取一个随机可用代理。

或者如果你弄清楚了代理池的架构，可以按需分别运行，命令如下：

```shell script
python3 run.py --processor getter
python3 run.py --processor tester
python3 run.py --processor server
```

这里 processor 可以指定运行 Tester、Getter 还是 Server。

## 使用

成功运行之后可以通过 [http://localhost:8000/random](http://localhost:8000/random) 获取一个随机可用代理。


## LICENSE

MIT
