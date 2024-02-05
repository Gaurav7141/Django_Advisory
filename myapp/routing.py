# your_app/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from .consumers import SubmitFormConsumer

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             [
#                 re_path("ws/submit_form/", SubmitFormConsumer.as_asgi()),
#             ]
#         )
#     ),
# })


# # routing.py

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from myapp import consumers

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             consumers.WebsocketConsumer,
#         )
#     ),
# })

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('submit_form', consumers.SubmitFormConsumer),
]
