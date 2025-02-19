# ituna-tracing

Simple demo project showcasing usage of opentelemetry tracing inside a distributed system

## Running with docker compose
```shell
docker-compose up
```
Once all three containers (ituna, kafka, jaeger) are started, the logs can be reviewed on the ituna host as follows:
```shell
docker ps
```
Locate the container that starts with "ituna-tracing-ituna", and then execute /bin/bash in it, e.g.:
```shell
docker exec -it ituna-tracing-ituna-1 /bin/bash
```
Review the logs in the log file:
```shell
cat ituna.log
```

## Local debugging
If you want to play more with the ituna code and do not want to rebuild docker image each time you update the code,
feel free to comment out the ituna service from the [compose.yaml](compose.yaml) file, and rerun docker-compose.
This will give you easy access to kafka and jaeger, but your code will be executed
directly from your host.
Some config modifications might be necessary to correctly specify kafka broker details.

* configure virtual environment
```shell
python3 -m venv venv
```
* activate it
```shell
source venv/bin/activate
```
* install dependencies
```shell
pip install -r requirements.txt
pip install git+https://github.com/dpkp/kafka-python.git
```
