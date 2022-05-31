from django.urls import path
from .views import *

urlpatterns = [
    #path("", treasureView, name="treasures"),
    path("", test_json, name="test_json"),
]
