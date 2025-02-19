#!/bin/bash

sleep 15 # let Kafka server get up and running

# Start consumers, then producers in the background
# (keep the last one in foreground for docker not to exit)
python ituna/kitchen_service.py & \
python ituna/order_validation.py & \
python ituna/on-site_ordering.py & \
python ituna/website_ordering.py & \
python ituna/direct_kitchen_ordering.py
