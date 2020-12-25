from authlib.integrations.flask_oauth2 import AuthorizationServer

import app
from models import Client, Token


def query_client(client_id):
    return Client.objects(client_id=client_id)  # TODO: ObjectId?


def save_token(token_data, request):
    if request.user:
        user_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
        # or, depending on how you treat client_credentials
        user_id = None
    token = Token(
        client_id=request.client.client_id,
        user_id=user_id,
        **token_data
    )
    token.save(force_insert=True)


# OAUTH2_TOKEN_EXPIRES_IN = {  # TODO: use config!
#     'authorization_code': 864000,
#     'implicit': 3600,
#     'password': 864000,
#     'client_credentials': 864000
# }

server = AuthorizationServer(
    app.app, query_client=query_client, save_token=save_token
)
