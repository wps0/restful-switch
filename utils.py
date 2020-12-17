from bson import ObjectId


def escape_special_chars(string: str):
    for c in string:
        if c < '0' or '9' < c < 'A' or 'Z' < c < 'a' or c > 'z':
            from flask_restful import abort
            abort(400)


def is_present_in_db(query: dict, table) -> bool:
    return table.count(query) != 0


def get_user_id(token: str):
    return "000000000000000000000000"
