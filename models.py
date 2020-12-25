import datetime as dt
import mongoengine as me

from auth.client_mixins import OAuth2MongoClientMixin
from auth.tokens_mixins import OAuth2TMongoTokenMixin


class User(me.Document):
    id = me.ObjectIdField(primary_key=True)
    username = me.StringField(required=True, unique=True, max_length=24, min_length=3)
    create_date = me.DateTimeField(default=dt.datetime.utcnow)
    last_login = me.DateTimeField(default=0)

    def get_user_id(self):
        return str(self.id)


class Client(me.Document, OAuth2MongoClientMixin):
    id = me.ObjectIdField(primary_key=True)
    registrar = me.ReferenceField(User)

    meta = {
        'collection': 'oauth_clients'
    }


class Token(me.Document, OAuth2TMongoTokenMixin):
    id = me.ObjectIdField(primary_key=True)
    user = me.ReferenceField(User)


class UserInteraction(me.EmbeddedDocument):
    ip_addr = me.StringField(max_length=64, required=True)
    conn_details = me.StringField(max_length=8192)
    create_date = me.DateTimeField(default=dt.datetime.utcnow)


class Poll(me.Document):
    id = me.ObjectIdField(primary_key=True)
    title = me.StringField(max_length=96)
    desc = me.StringField(max_length=512)
    options = me.ListField(me.StringField(max_length=128), required=True)
    creator_interaction = me.EmbeddedDocumentField(UserInteraction, required=True)
    creator = me.ReferenceField(User, required=True)
    publish_date = me.DateTimeField(default=3406320000, required=True)


class Vote(me.Document):
    id = me.ObjectIdField(primary_key=True)
    poll_id = me.ReferenceField(Poll)
    option_id = me.IntField(min_value=0, max_value=32)
    voter = me.ReferenceField(User)
    voter_interaction = me.EmbeddedDocumentField(UserInteraction, required=True)


class File(me.Document):
    hash = me.StringField(primary_key=True)
    file_path = me.StringField(required=True, unique=True)
    uploader = me.ReferenceField(User, required=True)
    uploader_interaction = me.EmbeddedDocumentField(UserInteraction, required=True)
