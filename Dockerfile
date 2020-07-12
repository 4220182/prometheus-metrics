FROM python:3.7-alpine

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt && rm -rf .cache/pip

ENV app /app
WORKDIR ${app}
ADD ./myWebServer.py $app

EXPOSE 8080
EXPOSE 9100

CMD ["python3", "myWebServer.py"]
