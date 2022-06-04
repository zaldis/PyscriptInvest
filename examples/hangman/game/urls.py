from django.urls import path

from . import views
from . import consumers


websocket_urlpatterns = [
    path('ws/hangman/', consumers.GameConsumer.as_asgi())
]

urlpatterns = [
    path('', views.index, name='index'),
]

