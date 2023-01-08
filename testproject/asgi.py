from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from strawberry.channels import GraphQLHTTPConsumer, GraphQLWSConsumer

from gqlauth.core.token_to_user import GqlAuthMiddleWare
from testproject.schema import arg_schema as schema

websocket_urlpatterns = [
    re_path("^graphql", GqlAuthMiddleWare(GraphQLWSConsumer.as_asgi(schema=schema))),
]
gql_http_consumer = AuthMiddlewareStack(GraphQLHTTPConsumer.as_asgi(schema=schema))
application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                re_path("^graphql", gql_http_consumer),
            ]
        ),
        "websocket": GqlAuthMiddleWare(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
    }
)
