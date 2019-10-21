import logging
import logging.config
import os
import yaml


class DebugFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.DEBUG


class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.ERROR


def ini_logger(name):
    yaml_dir = f"{os.path.dirname(__file__)}{os.sep}logging.yaml"
    with open(yaml_dir, 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    return logging.getLogger(name)
