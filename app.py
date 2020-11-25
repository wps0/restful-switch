from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app, "/v1")


class Homepage(Resource):
    def get(self):
        return 'Hello World!'


api.add_resource(Homepage, "/")


if __name__ == '__main__':
    app.run()
