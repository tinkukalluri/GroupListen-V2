from django.urls import path ,include
from . import views

app_name="frontend"

urlpatterns = [
    path('' , views.index ,name=""),
    path('join' , views.index , name="join"),
    path('create' , views.index),
    path('room/<str:roomcode>', views.index),
    path('info' , views.index),
    path('home' , views.index , name="homepage"),
    path('terms-conditions' , views.index , name="homepage"),
]