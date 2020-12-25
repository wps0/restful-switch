from flask import request
from flask_restful import Resource

from auth.auth_server import server


class AuthEndpoint(Resource):
    def get(self):
        pass


class TokenEndpoint(Resource):
    pass
