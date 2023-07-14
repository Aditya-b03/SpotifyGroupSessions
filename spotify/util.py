from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .creds import ClIENT_ID, ClIENT_SECRET
from requests import post,put,get

BASE_URL = 'https://api.spotify.com/v1/me/'

def get_user_token(session_id):
    user_token= SpotifyToken.objects.filter(user=session_id)
    if user_token.exists():
        return user_token[0]
    return None

def update_or_create_user_token(session_id, access_token,expires_in , refresh_token , token_type):
    user_token = get_user_token(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if user_token:
        user_token.access_token = access_token
        user_token.refresh_token = refresh_token
        user_token.expires_in = expires_in
        user_token.token_type = token_type
        user_token.save(update_fields=['access_token' , 'refresh_token', 'expires_in','token_type'])
    else:
        user_token = SpotifyToken(
            user = session_id,
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = expires_in,
        )
        user_token.save()


def is_Auth(session_id):
    user_token = get_user_token(session_id)
    if user_token:
        expiry = user_token.expires_in
        if expiry <= timezone.now():
            renew_user_token(session_id)
        return True
    return False

def renew_user_token(session_id):
    refresh_token = get_user_token(session_id).refresh_token
    print("Refresh token : " , refresh_token)

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': ClIENT_ID,
        'client_secret': ClIENT_SECRET,
    }).json()

    access_token= response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    print(response)
    update_or_create_user_token(session_id, access_token,expires_in , refresh_token , token_type)



def spotify_api_calls(session_id, endpoint , put_=False, post_ = False):
    user_token = get_user_token(session_id)
    header = {'Content-Type': 'application/json' , 'Authorization': "Bearer " + user_token.access_token}
    if post_:
        post(BASE_URL + endpoint , headers=header)
    elif put_:
        put(BASE_URL + endpoint , headers=header)
    else:
        response = get(BASE_URL + endpoint , {} , headers=header)
        try:
            return response.json()
        except:
            return {'Error' : "ISSUE WITH REQUEST"}
        

def playSongrequest(session_id):
    spotify_api_calls(session_id , "player/play" , put_=True)

def pauseSongrequest(session_id):
    spotify_api_calls(session_id , "player/pause" , put_=True)
