FROM python:latest

COPY requirements.txt .
COPY ituna ituna
COPY start-ituna-service.sh .

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/dpkp/kafka-python.git
RUN chmod +x start-ituna-service.sh
