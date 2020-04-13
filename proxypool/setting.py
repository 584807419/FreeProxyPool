import platform
from os.path import dirname, abspath, join
from environs import Env
from loguru import logger
from proxypool.utils.parse import parse_redis_connection_string

env = Env()
env.read_env()

# definition of flags
IS_WINDOWS = platform.system().lower() == 'windows'

# definition of dirs
ROOT_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# definition of environments
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE

# redis host
REDIS_HOST = env.str('REDIS_HOST', '154.8.219.34')
# redis port
REDIS_PORT = env.int('REDIS_PORT', 6379)
DB = env.int('DB', 0)
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', 'zhangkun_redis')
# redis connection string, like redis://[password]@host:port or rediss://[password]@host:port
REDIS_CONNECTION_STRING = env.str('REDIS_CONNECTION_STRING', None)

if REDIS_CONNECTION_STRING:
    REDIS_HOST, REDIS_PORT, REDIS_PASSWORD = parse_redis_connection_string(REDIS_CONNECTION_STRING)

# redis hash table key name
# REDIS_KEY = env.str('REDIS_KEY', 'valid_proxiy_pool')
REDIS_KEY = env.str('REDIS_KEY', 'proxies_for_gsxt_gov_cn')

# definition of proxy scores
PROXY_SCORE_MAX = 10
PROXY_SCORE_MIN = 0
PROXY_SCORE_INIT = 5

# definition of proxy number
PROXY_NUMBER_MAX = 5000
PROXY_NUMBER_MIN = 0

# definition of tester cycle, it will test every CYCLE_TESTER second
CYCLE_TESTER = env.int('CYCLE_TESTER', 2)
# definition of getter cycle, it will get proxy every CYCLE_GETTER second
CYCLE_GETTER = env.int('CYCLE_GETTER', 500)

# definition of tester
TEST_URL = [
    # 百度
    'http://www.baidu.com',
    'http://www.iqiyi.com/',
    'http://www.hao123.com/',
    'http://news.baidu.com/',
    'http://map.baidu.com',
    # 360
    'http://www.360.cn',
    'http://www.so.com',
    'http://hao.360.com/'
    # 腾讯系
    'http://www.tencent.com/',
    'http://cloud.tencent.com',
    'http://www.qq.com/?fromdefault',
    'http://weixin.qq.com/',
    'http://im.qq.com/',
    'http://game.qq.com',
    'http://lol.qq.com',
    'http://map.qq.com',
    'http://qian.qq.com',
    'http://v.qq.com/',
    'http://news.qq.com/',
    # 阿里系
    'http://www.taobao.com',
    'http://www.aliyun.com',
    'http://www.dingtalk.com',
    'http://www.alipay.com/',
    'http://www.antfin.com/',
    'http://www.youku.com/',
    'http://amap.com/',
    # 美团点评
    'http://www.dianping.com/',
    'http://www.meituan.com/',
    # 京东
    'http://www.jd.com/',
    'http://www.jdcloud.com',
    'http://jr.jd.com/',
    # 网易
    'http://www.163.com/',
    'http://music.163.com/',
    'http://news.163.com/',
    'http://game.163.com/',
    # 金山
    'http://www.ijinshan.com/',
    'http://www.kingsoft.com/',
    'http://www.wps.cn/',
    'http://www.cmcm.com',
    # 头条
    'http://www.bytedance.com/zh',
    'http://www.toutiao.com/',
    'http://www.douyin.com/',
    'http://www.ixigua.com',
    # 华为
    'http://www.huawei.com/',
    'http://www.huaweicloud.com',
    'http://developer.huawei.com/',
    # 其他
    'http://www.kuaishou.com/',
    'http://www.mi.com/',
    'http://58.com',
    'http://www.2345.com/',
    'http://www.suning.com',
    'http://www.people.com.cn/',
    'http://www.pinduoduo.com',
    'http://www.sina.com.cn/',
    'http://www.ctrip.com/',
    'http://www.bilibili.com/',
    'http://www.sogou.com',
]
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
TEST_BATCH = env.int('TEST_BATCH', 500)
# TEST_HEADERS = env.json('TEST_HEADERS', {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
# })
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302, 301, 307])

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 8000)
API_THREADED = env.bool('API_THREADED', True)

# flags of enable
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GETTER = env.bool('ENABLE_GETTER', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)

logger.add(env.str('LOG_RUNTIME_FILE', 'runtime.log'), level='DEBUG', rotation='100 MB', retention='1 days')
logger.add(env.str('LOG_ERROR_FILE', 'error.log'), level='ERROR', rotation='100 MB', retention='2 days')
