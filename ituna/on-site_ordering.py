#!/usr/bin/env python3

import json
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError

import config
import log
from random_values import make_random_order


class OnSiteOrdering:
    """
    On-site (a.k.a. in-person) Ordering service
    manages orders made inside the restaurant.
    """
    config = config.get_config()

    def __init__(self):
        self.log = log.get_logger("onsite-ordering")
        self.kafka_host = self.config.get("queue", "host")
        self.kafka_server_port = self.config.get("queue", "port")
        self.kafka_topic = self.config.get("initial-order", "queue-topic")
        self.simulated_delay = int(self.config.get("simulated-delays", "on-site-ordering")) / 1000
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
    onsite_ordering = OnSiteOrdering()
    onsite_ordering.log.info("Starting On-Site Ordering Service")
    while True:
        order = make_random_order(order_type="on-site")
        onsite_ordering.log.info(f"Placing an on-site order with id {order['order_id']}")
        onsite_ordering.place_an_order(order)
        onsite_ordering.log.info("The on-site order has been placed successfully!")
        time.sleep(5)
