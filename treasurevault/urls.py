from django.urls import path
from .views import *

urlpatterns = [
    #path("", treasureView, name="treasures"),
    path("", treasure_view, name="treasures"),
]
