from datetime import datetime

from flask_restful import Resource

from db import DB_TABLE_POLLS


class PollEndpoint(Resource):
    def get(self):
        for poll in DB_TABLE_POLLS.find({"publish_date": {"$lt": datetime.utcnow()}}):
            print(poll.name)
        return "POST"

    def put(self):
        