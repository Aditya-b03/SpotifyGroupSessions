from django.urls import path
from .views import RoomView,CreateRoomView,GetRoom,JoinRoom,UserInRoom,LeaveRoom,UpadateRoom

urlpatterns = [
    # can have multiple paths endpoint
    # path('part of url' , name of veiw function)
    path('Room' ,RoomView.as_view()),
    path('create-room' , CreateRoomView.as_view()),
    path('get-room' , GetRoom.as_view()),
    path('join-room' , JoinRoom.as_view()),
    path('user-in-room' , UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpadateRoom.as_view()),
]
