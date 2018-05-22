FROM python

RUN apt-get update


#安装flask prometheus_client 库
RUN pip install flask prometheus_client

# Install source files
COPY /start.py /start.py
WORKDIR /
EXPOSE 5000

ENTRYPOINT []
CMD ["python", "start.py"]

