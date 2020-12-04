import json
import time
from typing import List

from bson import ObjectId
from flask import request, jsonify
from flask_restful import Resource, abort
from pymongo.results import InsertOneResult

from config import MAX_DB_RESPONSE_TIME
from db import DB_TABLE_POLLS, DOCUMENT_POLL, DB_TABLE_VOTES


def wait_for_acknowledgement(res: InsertOneResult):
    pass
    # resp_time = MAX_DB_RESPONSE_TIME
    # print(res.acknowledged)
    # while not res.acknowledged and resp_time > 0:
    #     time.sleep(0.2)
    #     resp_time -= 0.2
    # if not res.acknowledged and resp_time <= 0:
    #     abort(504)  # gateway timed out


class PollEndpoint(Resource):
    def get(self):
        resp = []
        for poll in DB_TABLE_POLLS.find({"publish_date": {"$lt": time.time()}}):
            poll["_id"] = str(poll["_id"])
            resp.append(poll)

        return resp

    def put(self):
        args = request.json

        from models import Option, Poll
        options_list: List[Option] = []
        # try:
        for opt in args["options"]:
            options_list.append(Option(opt["content"]))

        js_replaced = str(Poll(args["title"], time.time(), options_list, args["desc"], time.time()))
        # except (KeyError, TypeError):
        #     abort(400)

        js_replaced = json.loads(js_replaced)
        res = DB_TABLE_POLLS.insert_one(js_replaced)

        js_replaced["_id"] = str(js_replaced["_id"])
        return jsonify(code=200, data=js_replaced, messsage="OK")


def escape_special_chars(string: str):
    for c in string:
        if c < '0' or '9' < c < 'A' or 'Z' < c < 'a' or c > 'z':
            print(c)


def poll_verification(poll_id: str):
    escape_special_chars(poll_id)
    if len(poll_id) != 24 or not ObjectId.is_valid(poll_id):
        abort(400)


class SinglePollEndpoint(Resource):
    def get(self, poll_id: str):
        poll_verification(poll_id)

        resp = DB_TABLE_POLLS.find_one({"_id": ObjectId(poll_id)})
        if resp is None:
            abort(404)
        resp["_id"] = str(resp["_id"])
        return jsonify(resp)

    def delete(self, poll_id: str):
        poll_verification(poll_id)

        cnt = DB_TABLE_POLLS.count({"_id": ObjectId(poll_id)})
        if cnt != 1:
            abort(404)

        res = DB_TABLE_POLLS.delete_one({"_id": ObjectId(poll_id)})
        if res is None:
            abort(404)

        wait_for_acknowledgement(res)
        if res.deleted_count != 1:
            abort(500)
        return "", 204


class PollVoteEndpoint(Resource):
    def post(self, poll_id: str):
        poll_verification(poll_id)
        nr: int = 0
        try:
            print(request.json["option_nr"])
            nr = request.json["option_nr"]
        except (TypeError, KeyError):
            abort(400)

        res = DB_TABLE_POLLS.find_one({"_id": ObjectId(poll_id)})
        if res is None:
            abort(404)

        if 0 > nr or nr >= len(res["options"]):
            abort(400)

        from models import Vote, Voter
        to_be_inserted = str(Vote(
            ObjectId(poll_id), nr, Voter(request.remote_addr, str(request.user_agent))
        ))
        to_be_inserted = json.loads(to_be_inserted)
        print(to_be_inserted)

        res = DB_TABLE_VOTES.insert_one(to_be_inserted)
        wait_for_acknowledgement(res)
        res = DB_TABLE_VOTES.find_one({"_id": ObjectId(res.inserted_id)})
        wait_for_acknowledgement(res)
        res["_id"] = str(res["_id"])
        return res

    def get(self, poll_id: str):
        poll_verification(poll_id)
        vote_amount = {}
        for vote in DB_TABLE_VOTES.find({"poll_id": poll_id}):
            vopt = int(vote["vote_option"])
            if vopt in vote_amount:
                vote_amount[vopt] += 1
            else:
                vote_amount[vopt] = 1
        return vote_amount
