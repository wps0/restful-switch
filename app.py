from flask import Flask, make_response
from flask_restful import Api, Resource, marshal_with, fields

import config


def json_response_formatter(data, code, headers=None):
    import json
    resp = make_response(json.dumps({"code": code, "data": data}), code)
    resp.headers.extend(headers or {})
    return resp


class RestfulApi(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.representations = {
            'application/json': json_response_formatter
        }


app = Flask(__name__)
api = RestfulApi(app, prefix="/v1")
app_cfg = config.load_config()
print(app_cfg)


class Homepage(Resource):
    # @marshal_with(API_RESPONSE_MARSHAL_FIELDS, "data")
    def get(self):
        code: int = 200

        return {"task": 'Hello World!', "code": code}, 200, {"asd": "ds"}  # content, response code, headers


api.add_resource(Homepage, "/")
from endpoints.polls import PollEndpoint, SinglePollEndpoint, PollVoteEndpoint

api.add_resource(PollEndpoint, "/poll")
api.add_resource(SinglePollEndpoint, "/poll/<string:poll_id>")
api.add_resource(PollVoteEndpoint, "/poll/<string:poll_id>/vote")

if __name__ == '__main__':
    app.run(debug=True)
