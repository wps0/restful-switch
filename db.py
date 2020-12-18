from pymongo import MongoClient

from app import app

DB_CLIENT: MongoClient = MongoClient(app.config["DB_URL"])
DB_ROOT = DB_CLIENT["restful_switch"]
DB_TABLE_USERS = DB_ROOT["users"]
DB_TABLE_POLLS = DB_ROOT["polls"]
DB_TABLE_VOTES = DB_ROOT["votes"]
DB_TABLE_FILES = DB_ROOT["files"]
DB_TABLE_FILE_INT = DB_ROOT["file_interactions"]

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
DOCUMENT_USER_INTERACTION = '{' \
                            '"user_id": "%user_id%",' \
                            '"create_date": %create_date%,' \
                            '"ip_addr": "%ip_addr%",' \
                            '"conn_details": "%conn_details%"' \
                            "}"

DOCUMENT_VOTE = '{' \
                '"poll_id": "%poll_id%",' \
                '"vote_option": "%option_nr%",' \
                '"voter": %voter%}'

DOCUMENT_FILE = '{' \
                '"file_path": "%file_path%",' \
                '"hash": "%hash%",' \
                '"uploader": %uploader%,' \
                '"create_date": %create_date%' \
                "}"
