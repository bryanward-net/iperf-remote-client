# syntax=docker/dockerfile:1
FROM python:3.8

LABEL Maintainer="Bryan Ward"

#ENV GRAFANA_TOKEN=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6
#ENV GRAFANA_SERVER=grafana.example.com
#ENV GRAFANA_PORT=3000
#ENV IPERF3_SERVER=iperf.example.com
#ENV IPERF3_PORT=5201
#ENV IPERF3_OMIT=1
#ENV IPERF3_DURATION=5
#ENV INTERVAL=10

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && apt install -y \
    iperf3 \
&& rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5201

CMD ["python3", "/app/iperf_remote_client.py"]