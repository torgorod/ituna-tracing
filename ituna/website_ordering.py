#!/usr/bin/env python3

import json
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

import config
import log
import tracer
from random_values import make_random_order


class WebsiteOrdering:
    """
    Website Ordering service allows customers
    to review menu and place orders from a convenience
    of their homes.
    """
    config = config.get_config()

    def __init__(self):
        self.log = log.get_logger("website-ordering")
        self.tracer = tracer.get_tracer("website-ordering")
        self.kafka_host = self.config.get("queue", "host")
        self.kafka_server_port = self.config.get("queue", "port")
        self.kafka_topic = self.config.get("initial-order", "queue-topic")
        self.simulated_delay = int(self.config.get("simulated-delays", "website-ordering")) / 1000
        self._kafka_producer = None

    @property
    def kafka_producer(self):
        if self._kafka_producer is None:
            self._kafka_producer = KafkaProducer(
                bootstrap_servers=f"{self.kafka_host}:{self.kafka_server_port}")
        return self._kafka_producer

    def place_an_order(self, order):
        """
        Places an order on the queue for further processing.
        :param order: Order to publish on the queue
        :return: None
        """
        time.sleep(self.simulated_delay)

        future = self.kafka_producer.send(self.kafka_topic, json.dumps(order).encode("ascii"))

        try:
            future.get(timeout=10)
        except KafkaError as ke:
            self.log.error(ke)
            pass


if __name__ == "__main__":
    website_ordering = WebsiteOrdering()
    website_ordering.log.info("Starting Website Ordering Service")
    while True:
        with website_ordering.tracer.start_as_current_span(name="main-website-order") as span:
            carrier = {}
            TraceContextTextMapPropagator().inject(carrier)
            order = make_random_order(order_type="website")
            order.update({"carrier": json.dumps(carrier)})
            website_ordering.log.info(f"Placing an online order with id {order['order_id']}")
            website_ordering.place_an_order(order)
        website_ordering.log.info("The online order has been placed successfully!")
        time.sleep(5)
