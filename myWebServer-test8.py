#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用python内置WSGI server: wsgiref ,考虑性能问题你也可以使用其他WSGI server
WSGI server用了gevent, eventlet等 green thread技术，就可以支持更多并发。
"""
from prometheus_client import start_http_server, Counter, Summary
import random
import time
from flask import Flask, jsonify
from wsgiref.simple_server import make_server

# 定义一个Counter类型的变量，这个变量不是指标名称，这种Counter类型只增加
# 不减少，程序重启的时候会被重新设置为0，构造函数第一个参数是定义 指标名称，
# 第二个是定义HELP中显示的内容，都属于文本
# 第三个参数是标签列表，也就是给这个指标加labels，这个也可以不设置
http_requests_total = Counter("http_requests", "Total request count of the host", ['code', 'method', 'endpoint'])

# Summary类型，它可以统计2个时间
# request_processing_seconds_count 该函数被调用的数量
# request_processing_seconds_sum  该函数执行所花的时长
request_time = Summary('request_processing_seconds', 'Time spent processing request')

app = Flask(__name__)

# Decorate function with metric.
@app.route("/")
@request_time.time() # 这个必须要放在app.route的下面
def process_request():

    # 这里设置0-1之间随机数用于模拟页面响应时长
    time.sleep(random.random())

    # .inc()表示增加，默认是加1，你可以设置为加1.5，比如.inc(1.5)
    # http_requests_total.inc()
    # 下面这种写法就是为这个指标加上标签，但是这里的method和endpoint
    # 都在Counter初始化的时候放进去的。
    # 你想统计那个ULR的访问量就把这个放在哪里
    http_requests_total.labels(code="200", method="get", endpoint="/").inc()
    return jsonify({"return": "success OK!"})


@app.route("/301")
def process_request_301():
    time.sleep(random.random())
    http_requests_total.labels(code="301", method="get", endpoint="/301").inc()
    return jsonify({"return": "response 301!"}), 301, {"Content-Type":"application/text"}

@app.route("/429")
def process_request_429():
    time.sleep(random.random())
    http_requests_total.labels(code="429", method="get", endpoint="/429").inc()
    return jsonify({"return": "response 429!"}), 429, {"Content-Type":"application/text"}

@app.route("/503")
def process_request_503():
    time.sleep(random.random())
    http_requests_total.labels(code="503", method="get", endpoint="/503").inc()
    return jsonify({"return": "response 503!"}), 503, {"Content-Type":"application/text"}

# 这个是健康检查用的
@app.route('/healthy')
def healthy():
    return "healthy"

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9108)
    # Generate some requests.

    httpd = make_server(
        '0.0.0.0',  # The host name.
        8088,  # A port number where to wait for the request.
        app  # Our application object name, in this case a function.
    )
    print("started.\n"
          "url: 0.0.0.0:8080/\n"
          "response 301: 0.0.0.0:8080/301\n"
          "response 429: 0.0.0.0:8080/429\n"
          "response 503: 0.0.0.0:8080/503\n"
          "metrics: 0.0.0.0:9100/metrics\n"
          "healthy: 0.0.0.0:9100/healthy")
    httpd.serve_forever()