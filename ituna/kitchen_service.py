#!/usr/bin/env python3

import json
import time

from kafka import KafkaConsumer

import config
import log


class KitchenService:
    """
    Kitchen Service is the final stage of the pipeline -
    this is where the food is prepared!
    """
    config = config.get_config()

    def __init__(self):
        self.log = log.get_logger("kitchen-service")
        self.kafka_host = self.config.get("queue", "host")
        self.kafka_server_port = self.config.get("queue", "port")
        self.kafka_topic_kitchen = self.config.get("kitchen-queue", "queue-topic")
        self.simulated_delay = int(self.config.get("simulated-delays", "kitchen-service")) / 1000
        self._kafka_consumer = None

    @property
    def kafka_consumer(self):
        if self._kafka_consumer is None:
            self._kafka_consumer = KafkaConsumer(self.kafka_topic_kitchen,
                                                 group_id="ituna",
                                                 value_deserializer=lambda x: json.loads(x.decode("ascii")),
                                                 bootstrap_servers=[f"{self.kafka_host}:{self.kafka_server_port}"])
        return self._kafka_consumer

    def prepare_order(self, order):
        """
        Prepares the order for the customer
        :param order: An order received from the kitchen queue
        :return: Str Prepared sushi order
        """
        time.sleep(self.simulated_delay)

        return f"Your order is ready. Please enjoy your {list(order['order_details'])[0]} and other food!"


if __name__ == "__main__":
    kitchen_service = KitchenService()
    kitchen_service.log.info("Starting Kitchen Service")
    for message in kitchen_service.kafka_consumer:
        order = message.value
        order_id = order["order_id"]
        kitchen_service.log.info(f"Received order {order_id} for processing")
        prepared_order = kitchen_service.prepare_order(order)
        kitchen_service.log.info(f"{prepared_order} - Order id = {order_id}" )
