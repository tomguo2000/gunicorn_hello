import os
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

# debug = True
loglevel = 'debug'
bind = "0.0.0.0:7788"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
daemon = False   # 重要！ 如果要打docker，一定要False，否则docker run后立即退出

# 启动的进程数
# workers = multiprocessing.cpu_count() * 1
workers = 3
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
