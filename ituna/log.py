import logging

logging.basicConfig(filename="ituna.log", level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def get_logger(name):
    logger = logging.getLogger(name)

    logging.getLogger("kafka.conn").setLevel(logging.ERROR)
    logging.getLogger("kafka.producer.kafka").setLevel(logging.ERROR)
    logging.getLogger("kafka.coordinator").setLevel(logging.ERROR)
    logging.getLogger("kafka.coordinator.consumer").setLevel(logging.ERROR)
    logging.getLogger("kafka.consumer.subscription_state").setLevel(logging.ERROR)
    logging.getLogger("kafka.cluster").setLevel(logging.ERROR)

    return logger
