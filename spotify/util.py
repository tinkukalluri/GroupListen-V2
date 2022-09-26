from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1"


def get_user_tokens(user_id):
    user_tokens = SpotifyToken.objects.filter(user=user_id)
    # #print(user_tokens)
    if user_tokens.exists():
        # #print("refresh_token::"+user_tokens[0].refresh_token)
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(user_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(user_id)
    #print(expires_in)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=user_id, access_token=access_token,
                            refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_spotify_authenticated(user_id):
    tokens = get_user_tokens(user_id)
    if tokens:
        expiry = tokens.expires_in
        #print("refresh_token::"+tokens.refresh_token)
        if expiry <= timezone.now():
            # return False
            refresh_spotify_token(user_id)
        return True

    return False


def refresh_spotify_token(user_id):
    refresh_token = get_user_tokens(user_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(
        user_id, access_token, token_type, expires_in, refresh_token)

def user_info(user_id):
    return execute_spotify_api_request(user_id, '/me' , _get=True)

def execute_spotify_api_request(user_id, endpoint,params={} , body={}, post_=False, put_=False , delete_=False , get_=False):
    print('executing spotify api request on user:', user_id)
    is_spotify_authenticated(user_id)
    tokens = get_user_tokens(user_id)
    headers = {'Content-Type': 'application/json',
                'Authorization': "Bearer " + tokens.access_token}
    url1=BASE_URL + endpoint
    #print("from execute_spotify_api_request(user_id)",url1 , get_)
    if post_:
        response=post(url1,data=body, params=params ,  headers=headers)
    if put_:
        response=put(url1,params=params,data=body ,headers=headers)
    if get_:
        response = get(url1, params, headers=headers)
        #print(response)
        try:
            return response.json()
        except:
            return {'Error': 'Issue with GET request'}
    if delete_:
        pass


def play_song(user_id):
    return execute_spotify_api_request(user_id, "/me/player/play", put_=True)


def pause_song(user_id):
    return execute_spotify_api_request(user_id, "/me/player/pause", put_=True)


def skip_song(user_id):
    return execute_spotify_api_request(user_id, "/me/player/next", post_=True)

