#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用python内置WSGI server: wsgiref ,考虑性能问题你也可以使用其他WSGI server
WSGI server用了gevent, eventlet等 green thread技术，就可以支持更多并发。
"""
from prometheus_client import start_http_server, Summary, Counter
import random
import time
from flask import Flask, jsonify
from wsgiref.simple_server import make_server

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
Counter_TIME = Counter('My_Counter', 'My Counter Desc')

app = Flask(__name__)


# Decorate function with metric.
@app.route("/test1")
@REQUEST_TIME.time()
def process_request():
    """A dummy function that takes some time."""
    time.sleep(random.random())
    Counter_TIME.inc()
    return jsonify({"return": "success OK!"})


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9100)
    # Generate some requests.

    httpd = make_server(
        '0.0.0.0',  # The host name.
        8080,  # A port number where to wait for the request.
        app  # Our application object name, in this case a function.
    )
    print("started. url: 0.0.0.0:8080/test1, metrics: 0.0.0.0:9100/metrics")
    httpd.serve_forever()