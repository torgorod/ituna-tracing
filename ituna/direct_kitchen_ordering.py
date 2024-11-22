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


class DirectKitchenOrdering:
    """
    DirectKitchenOrdering service allows
    direct publishing of orders for the kitchen service.
    """
    config = config.get_config()

    def __init__(self):
        self.log = log.get_logger("direct-kitchen-ordering")
        self.tracer = tracer.get_tracer("direct-kitchen-ordering")
        self.kafka_host = self.config.get("queue", "host")
        self.kafka_server_port = self.config.get("queue", "port")
        self.kafka_topic_kitchen = self.config.get("kitchen-queue", "queue-topic")
        self.simulated_delay = int(self.config.get("simulated-delays", "direct-kitchen-ordering")) / 1000
        self._kafka_producer = None

    @property
    def kafka_producer(self):
        if self._kafka_producer is None:
            self._kafka_producer = KafkaProducer(
                bootstrap_servers=f"{self.kafka_host}:{self.kafka_server_port}")
        return self._kafka_producer

    def place_an_order_for_kitchen(self, order):
        """
        Places an order on the queue for further processing.
        :param order: Order to publish on the queue
        :return: None
        """
        time.sleep(self.simulated_delay)

        # Update message with some validation data
        order.update({"validated": False})

        future = self.kafka_producer.send(self.kafka_topic_kitchen, json.dumps(order).encode("ascii"))

        try:
            future.get(timeout=10)
        except KafkaError as ke:
            self.log.error(ke)
            pass


if __name__ == "__main__":
    direct_kitchen_ordering = DirectKitchenOrdering()
    direct_kitchen_ordering.log.info("Starting Direct Kitchen Ordering Service")
    while True:
        with direct_kitchen_ordering.tracer.start_as_current_span(name="main-direct-order") as span:
            carrier = {}
            TraceContextTextMapPropagator().inject(carrier)
            order = make_random_order(order_type="on-site")
            order.update({"carrier": json.dumps(carrier)})
            direct_kitchen_ordering.log.info(f"Placing a direct order for the kitchen: {order['order_id']}")
            direct_kitchen_ordering.place_an_order_for_kitchen(order)
        direct_kitchen_ordering.log.info("The direct kitchen order has been placed successfully!")
        time.sleep(5)
