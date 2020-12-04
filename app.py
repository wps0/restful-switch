import uuid

from flask import Flask, make_response
from flask_restful import Api, Resource, marshal_with, fields, abort

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
config.init_config(app)
print(app.config)

from endpoints.polls import PollEndpoint, SinglePollEndpoint, PollVoteEndpoint
from endpoints.fileserver import UUIDFileServerEndpoint, UploadFileEndpoint

api.add_resource(PollEndpoint, "/poll")
api.add_resource(SinglePollEndpoint, "/poll/<string:poll_id>")
api.add_resource(PollVoteEndpoint, "/poll/<string:poll_id>/vote")
api.add_resource(UploadFileEndpoint, "/file")
api.add_resource(UUIDFileServerEndpoint, "/file/<string:file_id>")

if __name__ == '__main__':
    app.run(debug=True)
