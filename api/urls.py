from django.urls import path ,include
from api import views
from . import views
from . import views_2

app_name="api"

urlpatterns = [
    path('room', views.RoomView.as_view()),
    path('create-room' ,views.CreateRoomView.as_view() ),
    path('get-room',views.GetRoom.as_view()),
    path('join-room',views.JoinRoom.as_view()),
    path('user-in-room', views.UserInRoom.as_view()),
    path('leave-room', views.LeaveRoom.as_view()),
    path('update-room', views.UpdateRoom.as_view()),
    path('login', views.Login.as_view()),
    path('loginwithgoogle' , views.LoginWithGoogle.as_view()),
    path('authenticate',views.Authenticate.as_view()),
    path('logout', views.Logout.as_view()),
    path('fetchmessages',views_2.FetchMessages.as_view()),
    path('inputtext' , views_2.InputText.as_view()),
]