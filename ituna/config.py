import configparser

config = configparser.ConfigParser()
config.read("ituna/ituna-config.ini")


def get_config():
    return config
