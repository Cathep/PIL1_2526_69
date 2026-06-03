from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/conversation/(?P<conv_id>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
