from pymongo import MongoClient

from app import app_cfg

DB_CLIENT: MongoClient = MongoClient(app_cfg["db_url"])
DB_ROOT = DB_CLIENT["restful_switch"]
DB_TABLE_USERS = DB_ROOT["users"]
DB_TABLE_POLLS = DB_ROOT["polls"]

DOCUMENT_POLL = "{" \
                "'title': {title}," \
                "'description': {desc}," \
                "'publish_date': {publish_date}," \
                "'create_date': {create_date}," \
    "}"
