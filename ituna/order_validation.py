#!/usr/bin/env python3

import json
import time

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

import config
import log
import tracer


class OrderValidation:
    """
    OrderValidation service checks for necessary
    data to be present in the received orders,
    checks inventory etc. and republishes the order
    for the kitchen service.
    """
    config = config.get_config()

    def __init__(self):
        self.log = log.get_logger("order-validation")
        self.tracer = tracer.get_tracer("order-validation")
        self.kafka_host = self.config.get("queue", "host")
        self.kafka_server_port = self.config.get("queue", "port")
        self.kafka_topic_initial = self.config.get("initial-order", "queue-topic")
        self.kafka_topic_kitchen = self.config.get("kitchen-queue", "queue-topic")
        self.simulated_delay_addr_val = int(self.config.get("simulated-delays", "order-validation-address")) / 1000
        self.simulated_delay_name_val = int(self.config.get("simulated-delays", "order-validation-name")) / 1000
        self.simulated_delay_invent_val = int(self.config.get("simulated-delays", "order-validation-inventory")) / 1000
        self.simulated_delay_pub = int(self.config.get("simulated-delays", "order-validation-pub")) / 1000
        self._kafka_producer = None
        self._kafka_consumer = None

    @property
    def kafka_producer(self):
        if self._kafka_producer is None:
            self._kafka_producer = KafkaProducer(
                bootstrap_servers=f"{self.kafka_host}:{self.kafka_server_port}")
        return self._kafka_producer

    @property
    def kafka_consumer(self):
        if self._kafka_consumer is None:
            self._kafka_consumer = KafkaConsumer(self.kafka_topic_initial,
                                                 group_id="ituna",
                                                 value_deserializer=lambda x: json.loads(x.decode("ascii")),
                                                 bootstrap_servers=[f"{self.kafka_host}:{self.kafka_server_port}"])
        return self._kafka_consumer

    def validate_address(self, order):
        with self.tracer.start_span(name="address_validation") as span:
            span.set_attribute("zip", 90901)
            time.sleep(self.simulated_delay_addr_val)

    def validate_name(self, order):
        with self.tracer.start_as_current_span(name="name_validation"):
            time.sleep(self.simulated_delay_name_val)

    def validate_inventory(self, order):
        with self.tracer.start_as_current_span(name="inventory_validation"):
            time.sleep(self.simulated_delay_invent_val)

    def validate_order(self, order):
        """
        Validates that the order can be fulfilled.
        :param order: An order received from an ordering service
        :return: Boolean indicating whether the order is valid
        """
        self.validate_address(order)
        self.validate_name(order)
        self.validate_inventory(order)

        return True

    def place_an_order_for_kitchen(self, order):
        """
        Places an order on the queue for further processing.
        :param order: Order to publish on the queue
        :return: None
        """
        time.sleep(self.simulated_delay_pub)

        # Update message with some validation data
        order.update({"validated": True})

        future = self.kafka_producer.send(self.kafka_topic_kitchen, json.dumps(order).encode("ascii"))

        try:
            future.get(timeout=10)
        except KafkaError as ke:
            self.log.error(ke)
            pass


if __name__ == "__main__":
    order_validation = OrderValidation()
    order_validation.log.info("Starting Order Validation Service")
    for message in order_validation.kafka_consumer:
        order = message.value
        carrier = json.loads(order["carrier"])
        ctx = TraceContextTextMapPropagator().extract(carrier=carrier)

        with order_validation.tracer.start_as_current_span(name="main-order-validation", context=ctx):
            order_id = order["order_id"]
            order_validation.log.info(f"Received order {order_id} for validation")
            validated_order = order_validation.validate_order(order)
            if validated_order:
                order_validation.place_an_order_for_kitchen(order)
                order_validation.log.info(f"Validated and republished order for kitchen: {order['order_id']}")
