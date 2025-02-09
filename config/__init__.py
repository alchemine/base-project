"""Configuration constants for the project."""

from os import environ
from os.path import join, exists

import yaml
from easydict import EasyDict


def load_yaml(path: str) -> EasyDict:
    """Load yaml file."""
    with open(path, "r", encoding="utf8") as f:
        config = yaml.safe_load(f)
    return EasyDict(config)


##################################################
# Environments
##################################################
DEBUG = False
ENV = environ.get("ENV", "dev")


##################################################
# PATH
##################################################
CONFIG_DIR = "config"
SERVICE_CONFIG_PATH = join(CONFIG_DIR, "service.yaml")
if not exists(SERVICE_CONFIG_PATH):
    SERVICE_CONFIG_PATH = join(CONFIG_DIR, "service.dev.yaml")
ENGINE_CONFIG_PATH = join(CONFIG_DIR, "engine.yaml")


##################################################
# Configurations
##################################################
CFG_SERVICE = load_yaml(SERVICE_CONFIG_PATH)
CFG_ENGINE = load_yaml(ENGINE_CONFIG_PATH)


if __name__ == "__main__":
    print(ENV)
    print(CFG_SERVICE)
    print(CFG_ENGINE)
