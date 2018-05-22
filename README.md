 # 输出指标(prometheus metrics)

build 
```
docker build --tag koza/prometheus-metrics:latest .
```
docker方式运行：
```
docker run --rm -p 5000:5000  -it koza/prometheus-metrics:latest
```

访问：
http://127.0.0.1:5000/metrics

返回 metrics：
```
# HELP request_count Total request cout of the host
# TYPE request_count counter
request_count 34.0
```
