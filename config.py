import sys
import yaml

from flask import Flask


def init_config(app: Flask):
    loaded_cfg = load_config()
    insert_into_app_config(app, loaded_cfg)


def load_config():
    with open("res/config.yml", "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(-1)


def insert_into_app_config(app: Flask, cfg):
    app.config["DB_URL"] = cfg.get("db_url")
    app.config['SECRET_KEY'] = cfg.get("secret_key")
    app.config["FILE_SECRET_KEY"] = cfg.get("file_hash_secret")
    app.config["UPLOAD_DIR"] = cfg.get("upload_dir")
    app.config["UPLOAD_MAX_SIZE"] = cfg.get("upload_max_size")
