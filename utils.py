
def escape_special_chars(string: str):
    for c in string:
        if c < '0' or '9' < c < 'A' or 'Z' < c < 'a' or c > 'z':
            from flask_restful import abort
            abort(400)
