import logging
import yaml
import os

# Load Config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "connections.yaml")
try:
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    logging.error("Config file not found")
    raise