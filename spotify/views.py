import json
from django.shortcuts import render, redirect

from spotify.models import SpotifyToken
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room
from rest_framework import generics, status
from spotify.models import *
from .views_2 import *

# def spotifyView(request):
#     ##print(SpotifyToken.objects.all()[0].refresh_token)
#     return Response({"data":SpotifyToken.objects.all()[0].refresh_token} , status=status.HTTP_200_OK)
    


class AuthURL(APIView):
    def get(self, request, format=None):
        # scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        scopes='ugc-image-upload user-modify-playback-state user-follow-modify user-read-recently-played user-read-playback-position playlist-read-collaborative app-remote-control user-read-playback-state user-read-email streaming user-top-read playlist-modify-public user-library-modify user-follow-read user-read-currently-playing user-library-read playlist-read-private user-read-private playlist-modify-private'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        # url="https://accounts.spotify.com/authorize?scope="+scopes+"&response_type=code&redirect_uri=http://127.0.0.1:333/spotify/redirect&client_id="+CLIENT_ID
        # ##print("url::"+url)

        return Response({'url': url}, status=status.HTTP_200_OK)


class spotify_callback(APIView):
    def get(self, request, format=None):
        code = request.GET.get('code')
        error = request.GET.get('error')
        ##print('code===========================================================' , code)
        response = post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }).json()
        ##print("================================================================================",response)
        access_token = response.get('access_token')
        token_type = response.get('token_type')
        refresh_token = response.get('refresh_token')
        expires_in = response.get('expires_in')
        error = response.get('error')
        ##print('=====================' , dict(self.request.session))
        update_or_create_user_tokens(
            self.request.session['user_id'], access_token, token_type, expires_in, refresh_token)
        return redirect('frontend:join')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session['user_id'])
        return Response({'status': is_authenticated if is_authenticated else False}, status=status.HTTP_200_OK)




def check_sync(room_curr_song , user_curr_song):
    print('check_synccheck_synccheck_synccheck_synccheck_synccheck_synccheck_synccheck_synccheck_sync')
    if room_curr_song==user_curr_song:
        return True
    return False
    



class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        ##print("currentSong::room_code:"+room_code)
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        user_id = self.request.session.get('user_id')
        #comment this because we want non-user_id to watch there current_song playing
        # if user_id != self.request.session.session_key:
        #     return Response({}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        endpoint = "/me/player/currently-playing"
        response = execute_spotify_api_request(user_id, endpoint , get_=True)

        if 'error' in response or 'item' not in response:
            return Response({'nope':"if 'error' in response or 'item' not in response:"}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')
        artist_string = ""


        

        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name

            

        update_room_song(room , song_id , user_id)

        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': len(Vote.objects.filter(room=room, song_id=song_id)),
            'id': song_id,
            'votes_required':room.votes_to_skip,
            'in_sync':check_sync( room_curr_song=room.current_song ,user_curr_song=song_id )
        }
        # return Response(response, status=status.HTTP_200_OK) // this response will give all the data about currently playing audio...
        return Response(song, status=status.HTTP_200_OK)

def update_room_song( room, song_id , user_id):
        current_song = room.current_song

        if current_song != song_id and room.host.id==user_id:
            room.current_song = song_id
            votes = Vote.objects.filter(room=room).delete()
            room.save(update_fields=['current_song'])

class PauseSong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session['user_id'] == room.host.id or room.guest_can_pause:
            guest_list=room.guests['guests']
            print('pausepausepausepausepausepausepausepausepausepausepausepausepause')
            for i , user in enumerate(guest_list):
                pause_song(user)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class PlaySong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session['user_id'] == room.host.id or room.guest_can_pause:
            guest_list=room.guests['guests']
            print('playplayplayplayplayplayplayplayplayplayplayplayplayplayplayplayplay')
            for i , user in enumerate(guest_list):
                play_song(user)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.votes_to_skip
        if self.request.session['user_id'] == room.host.id or len(votes) + 1 >= votes_needed:
            votes.delete()
            self.room_id=self.request.session.get('room_id')
            queryset=Queue.objects.filter(room_id=self.room_id)
            if queryset.exists():
                self.queue=queryset[0]
            # self.queue=self.queue.tracks
            self.track_list=self.queue.tracks['tracks']
            self.track_list.sort(key=lambda v : v['tot_votes'], reverse=True)
            track_temp=self.track_list.pop(0)
            ##print(track_temp)
            # 
            self.track_id=track_temp['track']['track_id']
            # https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A4h4QlmocP3IuwYEj2j14p8
            endpoint='/me/player/queue?uri=spotify:track:{track_id}'.format(track_id=self.track_id)
            guest_list=room.guests['guests']
            print('4444444444444444444444444444444444444444444444444444444444444444444444444444')
            for i , user in enumerate(guest_list):
                result=execute_spotify_api_request(user , endpoint , {} ,post_=True )
                print('result::' , result)
                if result!=None:
                    return Response(result , status=status.HTTP_200_OK)
                else:
                    skip_song(user)

            # saving the poped queue
            self.queue.save(update_fields=['tracks'])
            return Response({
                'result':True
            } ,status=status.HTTP_200_OK)
            # 
        else:
            vote = Vote(user=self.request.session['user_id'],
                        room=room, song_id=room.current_song)
            vote.save()

        return Response({}, status.HTTP_204_NO_CONTENT)