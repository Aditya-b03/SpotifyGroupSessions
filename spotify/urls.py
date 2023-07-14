from django.urls import path
from .views import AuthURL,spotify_callback,IsAuth,CurrentSong,pauseSong,playSong

urlpatterns = [
    path('get-auth-url' , AuthURL.as_view()),
    path('redirect' , spotify_callback),
    path('is-auth', IsAuth.as_view()),
    path('current-song' , CurrentSong.as_view()),
    path('play', playSong.as_view()),
    path('pause' , pauseSong.as_view()),
]
