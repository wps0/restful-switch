import time
from mongoengine import StringField, IntField, ReferenceField, BooleanField
from authlib.oauth2.rfc6749 import (
    TokenMixin,
    AuthorizationCodeMixin,
)
from models import Client


class OAuth2MongoAuthorizationCodeMixin(AuthorizationCodeMixin):
    code = StringField(max_length=120, unique=True, null=False)
    client_id = ReferenceField(Client)
    redirect_uri = StringField(default='')
    response_type = StringField(default='')
    scope = StringField(default='')
    nonce = StringField()
    auth_time = IntField(null=False, default=time.time)  # TODO: czy tutaj powinna być method pointer czy method
    # call? Raczej pointer

    code_challenge = StringField()
    code_challenge_method = StringField(max_length=48)

    def is_expired(self):
        return self.auth_time + 300 < time.time()

    def get_redirect_uri(self):
        return self.redirect_uri

    def get_scope(self):
        return self.scope

    def get_auth_time(self):
        return self.auth_time

    def get_nonce(self):
        return self.nonce


class OAuth2TMongoTokenMixin(TokenMixin):
    client_id = ReferenceField(Client)
    token_type = StringField(max_length=40)
    access_token = StringField(unique=True, null=False)
    refresh_token = StringField(max_length=255, index=True)
    scope = StringField(default='')
    revoked = BooleanField(default=False)
    issued_at = IntField(null=False, default=time.time)
    expires_in = IntField(null=False, default=0)

    def get_client_id(self):
        return self.client_id

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def get_expires_at(self):
        return self.issued_at + self.expires_in
