from .creds import REDIRECT_URI,ClIENT_ID,ClIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from django.shortcuts import redirect
from api.models import Room

# from our frontend we can call this api endpoint
class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        # here we are just prepare a url to send to Auth
        url = Request('GET', 'https://accounts.spotify.com/authorize' , params={
            'response_type': 'code', #code and state - An authorization code that can be exchanged for an Access Token.
            'scope': scopes,
            'client_id': ClIENT_ID,
            'redirect_uri': REDIRECT_URI,
        }).prepare().url

        return Response({'url': url} , status=status.HTTP_200_OK)

# after authorization we will redirect to here, we request the token -> save it in the model->then redirect back
def spotify_callback(request,format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': ClIENT_ID,
        'client_secret': ClIENT_SECRET,
    }).json()

    access_token= response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_token(request.session.session_key , access_token , expires_in , refresh_token ,token_type)

    # if we wanna redirect to a different app we redirect to name of application:page_name_or_url_name
    # here page_name is empty as the homepage_url_name in frontend app
    return redirect('frontend:')
        

class IsAuth(APIView):
    def get(self,request,format=None):
        is_Authenticated = is_Auth(self.request.session.session_key)
        return Response({"status" : is_Authenticated}, status=status.HTTP_200_OK)
    

class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code = room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({} , status=status.HTTP_404_NOT_FOUND)
        host = room.host
        # request loaction to get currently playing song
        endpoint = "player/currently-playing"
        response = spotify_api_calls(host , endpoint)

        if 'error' in response or 'item' not in response:
            return Response({} , status=status.HTTP_204_NO_CONTENT)
        
        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url') #640*640
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ''
        for i , artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ', '
            name = artist.get('name')
            artist_string += name

        song = {
            'title' : item.get('name'),
            'artist' : artist_string,
            'duration' : duration,
            'time' : progress,
            'cover_url' : album_cover,
            'is_playing' : is_playing,
            'votes' : 0,
            'id' : song_id
        }
        return Response(song , status=status.HTTP_200_OK)


class playSong(APIView):
    def put(self , request , format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
            host = self.request.session.session_key
            if host == room.host or room.guest_can_pause:
                playSongrequest(host)
                return Response({} , status=status.HTTP_200_OK)
            return Response({} , status=status.HTTP_403_FORBIDDEN)
        return Response({} , status=status.HTTP_404_NOT_FOUND)



class pauseSong(APIView):
    def put(self , request , format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
            host = self.request.session.session_key
            if host == room.host or room.guest_can_pause:
                pauseSongrequest(host)
                return Response({} , status=status.HTTP_200_OK)
            return Response({} , status=status.HTTP_403_FORBIDDEN)
        return Response({} , status=status.HTTP_404_NOT_FOUND)


