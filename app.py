from flask import Flask
from flask_restful import Api, Resource, marshal_with, fields

import config
from endpoints.polls import PollEndpoint

app = Flask(__name__)
api = Api(app, "/v1")
app_cfg = config.load_config()


class Homepage(Resource):
    # @marshal_with(API_RESPONSE_MARSHAL_FIELDS, "data")
    def get(self):
        code: int = 200

        return {"task": 'Hello World!', "code": code}, 200, {"asd": "ds"}  # content, response code, headers


api.add_resource(Homepage, "/")
api.add_resource(PollEndpoint, "/poll")

if __name__ == '__main__':
    app.run()
