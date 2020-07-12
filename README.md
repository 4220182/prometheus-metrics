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
http://127.0.0.1:8080/test1


访问metrics：
http://127.0.0.1:9100/metrics

返回 metrics：
```
# HELP request_count Total request cout of the host
# TYPE request_count counter
request_count 34.0
```
