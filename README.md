 # 输出指标(prometheus metrics)

build 
```
docker build --tag koza/prometheus-metrics:latest .
```
docker方式运行：
```
docker run --rm -p 8080:8080 -p 9100:9100  -it koza/prometheus-metrics:latest
```

访问页面，让计数器+1：
http://127.0.0.1:8080/


访问metrics：
http://127.0.0.1:9100/metrics

返回 metrics：
```
# HELP http_requests_total Total request count of the host
# TYPE http_requests_total counter
http_requests_total{endpoint="/",method="get"} 2.0
# HELP http_requests_created Total request count of the host
# TYPE http_requests_created gauge
http_requests_created{endpoint="/",method="get"} 1.594648377703228e+09
# HELP request_processing_seconds Time spent processing request
# TYPE request_processing_seconds summary
request_processing_seconds_count 2.0
request_processing_seconds_sum 0.7703039780000003
# HELP request_processing_seconds_created Time spent processing request
# TYPE request_processing_seconds_created gauge
request_processing_seconds_created 1.594648370075318e+09
```
