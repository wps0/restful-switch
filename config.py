import sys
import yaml

# in seconds
MAX_DB_RESPONSE_TIME = 5


def load_config():
    with open("res/config.yml", "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(-1)
