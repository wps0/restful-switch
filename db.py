from pymongo import MongoClient

from app import app_cfg

DB_CLIENT: MongoClient = MongoClient(app_cfg["db_url"])
DB_ROOT = DB_CLIENT["restful_switch"]
DB_TABLE_USERS = DB_ROOT["users"]
DB_TABLE_POLLS = DB_ROOT["polls"]
DB_TABLE_VOTES = DB_ROOT["votes"]

DOCUMENT_POLL = '{' \
                '"title": "%title%",' \
                '"desc": "%desc%",' \
                '"publish_date": %publish_date%,' \
                '"create_date": %create_date%,' \
                '"options": %options%' \
                "}"

DOCUMENT_VOTE_OPTION = '{' \
                       '"content": "%content%"' \
                       "}"
DOCUMENT_VOTER = '{' \
                 '"user_id": "%user_id%",' \
                 '"create_date": %create_date%,' \
                 '"ip_addr": "%ip_addr%",' \
                 '"conn_details": "%conn_details%"' \
                 "}"

DOCUMENT_VOTE = '{' \
                '"poll_id": "%poll_id%",' \
                '"vote_option": "%option_nr%",' \
                '"voter": %voter%}'
