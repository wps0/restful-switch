from datetime import datetime

from flask_restful import Resource

from db import DB_TABLE_POLLS


class PollEndpoint(Resource):
    def get(self):
        DB_TABLE_POLLS.find_many({"publish_date": {$lt: datetime.utcnow()}})
        return "POST"
