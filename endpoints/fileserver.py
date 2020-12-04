import uuid
from hashlib import sha256

from flask import send_from_directory

from app import app
from db import DB_TABLE_FILES
from flask_restful import Resource, abort


def verify_file_hash(h: str):
    from utils import escape_special_chars
    escape_special_chars(h)
    if len(h) != 64:
        abort(400)


class UUIDFileServerEndpoint(Resource):
    def get(self, file_id: str):
        verify_file_hash(file_id)
        res = DB_TABLE_FILES.find_one({"hash": file_id})
        if res is None:
            abort(404)

        try:
            file_path = res["file_path"]
        except KeyError:
            abort(404)

        return send_from_directory(app.config["UPLOAD_DIR"], file_path, as_attachment=True)


# TODO: https://phil.tech/2016/http-rest-api-file-uploads/
# https://flask.palletsprojects.com/en/1.1.x/api/?highlight=send_file#flask.send_file
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
class UploadFileEndpoint(Resource):
    def post(self):
        abort(501)
