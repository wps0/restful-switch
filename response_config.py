from flask_restful import fields

API_RESPONSE_ENVELOPE = "data"
API_RESPONSE_MARSHAL_FIELDS = {"data": fields.Raw, "code": fields.Integer, "message": fields.String}

