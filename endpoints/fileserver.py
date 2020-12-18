import json
import os
from hashlib import sha256

from flask import send_from_directory, request, jsonify
from flask_restful import Resource, abort
from pymongo.errors import DuplicateKeyError

from app import app
from db import DB_TABLE_FILES
from models import File
from utils import get_user_id, get_user_info


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


# https://phil.tech/2016/http-rest-api-file-uploads/
class UploadFileEndpoint(Resource):
    def post(self):
        if request.content_length is None:
            abort(411, message="Required Content-Length header is missing")
        # Data length doesn't have to be checked as it seems the framework ignores data longer than
        #  specified in the content-header field of a request.
        if request.data is None or request.content_length == 1:
            abort(400)
        if request.content_length > app.config["UPLOAD_MAX_SIZE"]:
            abort(413, message="Request body too large")
        data_hash = sha256(request.data)
        uploaded_file = File(
            str("uploaded_" + get_user_id("asdf") + "_" + data_hash.hexdigest()),
            get_user_info(request),
            data_hash.hexdigest()
        )
        try:
            res = DB_TABLE_FILES.insert_one(json.loads(str(uploaded_file)))
        except DuplicateKeyError:
            abort(409, message="File already exists")

        if res.acknowledged and res.inserted_id is not None:
            with open(app.config["UPLOAD_DIR"] + os.path.sep + uploaded_file.file_path, "wb") as f:
                f.write(request.data)
            return jsonify(code=200, messsage="OK")
        abort(500)
