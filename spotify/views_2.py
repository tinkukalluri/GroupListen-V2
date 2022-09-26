from audioop import reverse
import json
from unittest import result
from django.shortcuts import render, redirect
from spotify import views

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
from django.utils import timezone

# new api requests like playlists tracks etc


def getPlaylist_href(data):
    return data['href']

def getImages(imgs):
    l1=[]
    for img in imgs:
        return l1.append(img['url'])
    return l1

def getPlaylists_items(data):
    ##print(type(data))
    ##print(data)
    l1=[]
    for item in data['items']:
        dic1={}
        dic1['name']=item['name']
        dic1['description']=item['description']
        dic1['spotify']=item['external_urls']['spotify']
        dic1['href']=item['href']
        dic1['id']=item['id']
        dic1['images']=getImages(item['images'])
        dic1['owner']=item['owner']
        dic1['display_name']=item['owner']['display_name']
        dic1['tracks_href']=item['tracks']['href']
        dic1['tot_tracks']=item['tracks']['total']
        dic1['uri']=item['uri']
        l1.append(dic1)
    return l1

# https://api.spotify.com/v1/me/playlists?offset=0&limit=50

class GetPlaylists(APIView):
    def get(self, request, format=None):
        # self.user_id=8
        self.user_id=self.request.session['user_id']
        self.offset=int(request.GET.get('offset')) if request.GET.get('offset')!=None else 0
        self.limit=int(request.GET.get('limit')) if request.GET.get('limit')!=None else 30
        ##print("from getPlaylist" , self.offset , self.limit)
        ##print(type(self.limit) , type(self.offset))
        result = execute_spotify_api_request(self.user_id , '/me/playlists' , params={"offset":self.offset,"limit":self.limit},get_=True)
        if result.get('Error')!=None or result.get('error')!=None:
            return Response(result , status=status.HTTP_200_OK)
        l1=getPlaylists_items(result)
        # ##print("playlist data !!!!!!!!!!!!!!!!!!!!!!!!!")
        # ##print(l1)
        return Response({
            'playlists':l1
        } ,status=status.HTTP_200_OK)



class GetPlaylistsTracks(APIView):

    def playlist_track(items):
        l1=[]
        for i in range(len(items)):
            dic={}
            dic['added_at']= items[i]['added_at']
            dic['artist_list']=items[i]['track']['artists']
            # albums
            dic['album_id']=items[i]['track']['album']['id']
            dic['img_list']=items[i]['track']['album']['images']
            dic['album_name']=items[i]['track']['album']['name']
            dic['album_uri']=items[i]['track']['album']['uri']
            dic['album_tot_tracks']=items[i]['track']['album']['total_tracks']
            # track
            dic['track_name']=items[i]['track']['name']
            dic['track_id']=items[i]['track']['id']
            dic['track_uri']=items[i]['track']['uri']
            dic['track_no']=items[i]['track']['track_number']
            dic['duration_ms']=items[i]['track']['duration_ms']
            l1.append(dic)
        return l1

    def get(self, request):
        self.playlist_id = str(request.GET.get('id'))
        self.user_id=self.request.session['user_id']
        self.offset=int(request.GET.get('offset')) if request.GET.get('offset')!=None else 0
        self.limit=int(request.GET.get('limit')) if request.GET.get('limit')!=None else 100
        ##print(self.playlist_id , self.user_id ,self.offset ,self.limit)
        endpoint='/playlists/{playlist_id}/tracks'.format(playlist_id=self.playlist_id)
        result = execute_spotify_api_request(self.user_id ,endpoint  , params={"offset":self.offset,"limit":self.limit},get_=True)
        ##print(result)
        if result.get('error')!=None:
            return Response(result , status=status.HTTP_200_OK)
        l1=GetPlaylistsTracks.playlist_track(result['items'])
        return Response({
            'tracks':l1
        } ,status=status.HTTP_200_OK)

# Important!!!!!!!!!
# this get queue if to for getting the spotify user queue
# but i'm not using this queue
class GetQueue(APIView):
    def get_queue_tracks(queue):
        l1 = []
        for i in range(len(queue)):
            dic={}
            # album:
            dic['album_artists_list']= queue[i]['album']['artists']
            dic['album_id']=queue[i]['album']['id']
            dic['album_img_list']=queue[i]['album']['images']
            dic['album_name']=queue[i]['album']['name']
            dic['album_uri']=queue[i]['album']['uri']
            dic['album_tot_tracks']=queue[i]['album']['total_tracks']
            dic['album_external_url']= queue[i]['album']['external_urls']['spotify']
            dic['album_href']=queue[i]['album']['href']

            # artists
            dic['track_artist_list']= queue[i]['artists']

            # track:
            dic['track_name']= queue[i]['name']
            dic['track_href']= queue[i]['href']
            dic['track_id']= queue[i]['id']
            dic['track_no']= queue[i]['track_number']
            dic['track_uri']= queue[i]['uri']
            dic['track_duration_ms']= queue[i]['duration_ms']
            dic['track_external_url']= queue[i]['external_urls']['spotify']

            l1.append(dic)
        return l1

    def get(self , request , format=None):
        # https://api.spotify.com/v1/me/player/queue
        endpoint='/me/player/queue'
        self.user_id=self.request.session['user_id']
        result=execute_spotify_api_request(self.user_id , endpoint , {} ,get_=True )
        ##print(result)
        if result.get('error')!=None:
            return Response(result , status=status.HTTP_200_OK)
        l1=GetQueue.get_queue_tracks(result['queue'])
        return Response({
            'queue':l1
        } ,status=status.HTTP_200_OK)


class PlayTrack(APIView):
    def post(self, request):
        post_data=request.data
        self.track_id=post_data['track_id']
        self.user_id=self.request.session['user_id']
        self.room_id=self.request.session['room_id']
        room_obj=Room.objects.filter(id=self.room_id)[0]

        if self.user_id==int(room_obj.host.id):
            self.room_id=self.request.session.get('room_id')
            queryset=Queue.objects.filter(room_id=self.room_id)
            if queryset.exists():
                self.queue=queryset[0]
                # self.queue=self.queue.tracks
                self.track_list=self.queue.tracks['tracks']
                self.track_list.sort(key=lambda v : v['tot_votes'], reverse=True)
                track_temp=self.track_list.pop(0)
                self.queue.save()
                #print(track_temp)
            # 
            # https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A4h4QlmocP3IuwYEj2j14p8
            endpoint='/me/player/queue?uri=spotify:track:{track_id}'.format(track_id=self.track_id)
            guest_list=room_obj.guests['guests']
            print('playtrackplaytrackplaytrackplaytrackplaytrackplaytrackplaytrackplaytrack')
            for i , user in enumerate(guest_list):
                result=execute_spotify_api_request(user , endpoint , {} ,post_=True )
                print('result::' , result)
                if result!=None:
                    return Response(result , status=status.HTTP_200_OK)
                else:
                    skip_song(user)
            return Response({
                'result':True
            } ,status=status.HTTP_200_OK)
        else:
            return Response({
                        'result':'not the host'
                    } ,status=status.HTTP_200_OK)

class AddToQueue(APIView):
    def get_tracks_info(queue):
        l1 = []
        for i in range(len(queue)):
            dic={}
            # album:
            dic['album_artists_list']= queue[i]['album']['artists']
            dic['album_id']=queue[i]['album']['id']
            dic['album_img_list']=queue[i]['album']['images']
            dic['album_name']=queue[i]['album']['name']
            dic['album_uri']=queue[i]['album']['uri']
            dic['album_tot_tracks']=queue[i]['album']['total_tracks']
            dic['album_external_url']= queue[i]['album']['external_urls']['spotify']
            dic['album_href']=queue[i]['album']['href']

            # artists
            dic['track_artist_list']= queue[i]['artists']

            # track:
            dic['track_name']= queue[i]['name']
            dic['track_href']= queue[i]['href']
            dic['track_id']= queue[i]['id']
            dic['track_no']= queue[i]['track_number']
            dic['track_uri']= queue[i]['uri']
            dic['track_duration_ms']= queue[i]['duration_ms']
            dic['track_external_url']= queue[i]['external_urls']['spotify']

            l1.append(dic)
        return l1

    

    def post(self, request , format=None):
        post_data = request.data
        self.user_id=self.request.session['user_id']
        self.room_id=self.request.session['room_id']
        self.track_id=post_data['track_id']
        user_obj= Users.objects.filter(id=self.user_id)[0]
        room_obj= Room.objects.filter(id=self.room_id)[0]
        quere_obj=Queue.objects.filter(room_id=self.room_id)
        # track info from spotify api
        # https://api.spotify.com/v1/tracks/6I3mqTwhRpn34SLVafSH7G
        endpoint='/tracks/{track_id}'.format(track_id=self.track_id)
        result=execute_spotify_api_request(self.user_id , endpoint , {} ,get_=True )
        l1=AddToQueue.get_tracks_info([result])
        self.t_obj={
            "track":l1[0],
            'added_on':str(timezone.now() + timezone.timedelta(hours=5.5)),
            'tot_votes':1,
            'users_votes':[self.user_id]
        }
        if quere_obj.exists():
            quere_obj=quere_obj[0]
            tracks=quere_obj.tracks
            track_list= tracks['tracks']
            #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            #print(tracks)
            #print(type(track_list),track_list )
            # checking if the track already exists in the queue if yes incrementing votes:
            track_exists=False
            for track in track_list:
                #print('---------------------------------------------------------------')
                #print(track)
                #print(type(track['track']) , track['track'])
                if track['track']['track_id']==self.track_id :
                    track_exists=True
                    if self.user_id not in track['users_votes']:
                        track['tot_votes']=track['tot_votes']+1
                        track['users_votes'].append(self.user_id)
                        quere_obj.save(update_fields=['tracks'])
                    
                # adding the track if doesnt exists
            if not track_exists:
                #print('tracksssssssssssssssssssssssssssssssssssssssss')
                #print(type(tracks), tracks)
                track_list.append(self.t_obj)
                # quere_obj.tracks={
                #     'tracks':tracks,
                #     }
                quere_obj.save(update_fields=['tracks'])
                #print("====================================")
                #print(len(track_list))
        else:
            quere_obj=Queue(user_id=user_obj , room_id=room_obj , tracks={
                'tracks':[self.t_obj],
            })
            quere_obj.save()

        return Response({
            'added':quere_obj.tracks['tracks']
        } , status=status.HTTP_200_OK)


class GetRoomQueue(APIView):
    def get(self, request, format=None):
        self.room_id=self.request.session.get('room_id')
        queryset=Queue.objects.filter(room_id=self.room_id)
        if queryset.exists():
            self.queue=queryset[0]
            # self.queue=self.queue.tracks
            self.track_list=self.queue.tracks['tracks']
            self.track_list.sort(key=lambda v : v['tot_votes'], reverse=True)
        return Response({
            'queue': self.queue.tracks['tracks']
        }, status=status.HTTP_200_OK)



class UpDownVotes(APIView):
    def post(self, request):
        post_data=request.data
        self.user_id=self.request.session['user_id']
        self.room_id=self.request.session['room_id']
        self.track_id=post_data['track_id']

        quere_obj=Queue.objects.filter(room_id=self.room_id)[0]
        tracks=quere_obj.tracks
        tracks_list=tracks['tracks']
        for track in tracks_list:
            tr_id= track['track']['track_id']
            if tr_id==self.track_id:
                if self.user_id in track['users_votes']:
                    #print("down votedddddddddddddddddd")
                    # the used already upvoted the track and now down voting it:
                    track['users_votes'].remove(self.user_id)
                    track['tot_votes']=track['tot_votes']-1
                    quere_obj.save(update_fields=['tracks'])
                    return Response({
                        'upvoted':False
                    }, status=status.HTTP_200_OK)
                else:
                    #print('up votedddddddddddddddddddddddddddd')
                    # the user is upvoting the track
                    track['users_votes'].append(self.user_id)
                    track['tot_votes']=track['tot_votes']+1
                    quere_obj.save(update_fields=['tracks'])
                    return Response({
                        'upvoted':True
                    }, status=status.HTTP_200_OK)


def play_track_fun(track_id , user_id):
    endpoint='/me/player/queue?uri=spotify:track:{track_id}'.format(track_id=track_id)
    result=execute_spotify_api_request(user_id , endpoint , {} ,post_=True )
    if result!=None:
        return False
    else:
        skip_song(user_id)
        return True


class Sync_track(APIView):
    def get(self, request, format=None):
        room_id= self.request.session.get('room_id')
        user_id=self.request.session.get('user_id')
        room_obj=Room.objects.filter(id=room_id)[0]
        user_obj=Users.objects.filter(id=user_id)[0]
        room_host=room_obj.host.id
        room_cur_song=room_obj.current_song

        # getting host current playing track and duration
        endpoint = "/me/player/currently-playing"
        response = execute_spotify_api_request(room_host, endpoint , get_=True)
        if 'error' in response :
            return Response({
            'result':False
            }, status=status.HTTP_200_OK)
        else:
            item = response.get('item')
            duration = item.get('duration_ms')
            progress = response.get('progress_ms')
            is_playing = response.get('is_playing')
            song_id = item.get('id')
            # /v1/me/player/seek?position_ms=10
            play_track_fun(song_id , user_id)
            endpoint="/me/player/seek"
            result=execute_spotify_api_request(user_id, endpoint ,params={'position_ms':progress+3} ,put_=True)
            print("seekkkkkkkkkkkkkkkkkkkkkkkkk result" , result)
            return Response({
                'result':True,
            } , status=status.HTTP_200_OK)


def get_tracks(obj):
        l1 = []
        for i in range(len(obj)):
            dic={}
            # album:
            dic['album_artists_list']= obj[i]['album']['artists']
            dic['album_id']=obj[i]['album']['id']
            dic['album_img_list']=obj[i]['album']['images']
            dic['album_name']=obj[i]['album']['name']
            dic['album_uri']=obj[i]['album']['uri']
            dic['album_tot_tracks']=obj[i]['album']['total_tracks']
            dic['album_external_url']= obj[i]['album']['external_urls']['spotify']
            dic['album_href']=obj[i]['album']['href']

            # artists
            dic['track_artist_list']= obj[i]['artists']

            # track:
            dic['track_name']= obj[i]['name']
            dic['track_href']= obj[i]['href']
            dic['track_id']= obj[i]['id']
            dic['track_no']= obj[i]['track_number']
            dic['track_uri']= obj[i]['uri']
            dic['track_duration_ms']= obj[i]['duration_ms']
            dic['track_external_url']= obj[i]['external_urls']['spotify']
            dic['type']=obj[i]['type']
            l1.append(dic)
        return l1


def get_albums(obj):
    l1 = []
    for i in range(len(obj)):
        dic={}
        # album:
        dic['album_artists_list']= obj[i]['artists']
        dic['album_id']=obj[i]['id']
        dic['album_img_list']=obj[i]['images']
        dic['album_name']=obj[i]['name']
        dic['album_uri']=obj[i]['uri']
        dic['album_tot_tracks']=obj[i]['total_tracks']
        dic['album_external_url']= obj[i]['external_urls']['spotify']
        dic['album_href']=obj[i]['href']
        l1.append(dic)
    return l1


def get_only_tracks(obj):
    l1 = []
    for i in range(len(obj)):
        dic={}
        # artists
        dic['track_artist_list']= obj[i]['artists']

        # track:
        dic['track_name']= obj[i]['name']
        dic['track_href']= obj[i]['href']
        dic['track_id']= obj[i]['id']
        dic['track_no']= obj[i]['track_number']
        dic['track_uri']= obj[i]['uri']
        dic['track_duration_ms']= obj[i]['duration_ms']
        dic['track_external_url']= obj[i]['external_urls']['spotify']
        dic['type']=obj[i]['type']
        l1.append(dic)
    return l1


class Search(APIView):
    def get(self, request, format=None):
        s_query=request.GET.get('q')
        type=request.GET.get('type')
        offset=request.GET.get('offset') if request.GET.get('offset')!=None else 0
        limit=request.GET.get('limit') if request.GET.get('limit')!=None else 20
        # https://api.spotify.com/v1/search?type=track,album&q=chitti
        endpoint='/search'
        # ?type=track,album&q={q}'.format(q=s_query)
        user_id=self.request.session.get('user_id')
        response = execute_spotify_api_request(user_id, endpoint ,params={
            'type':'track,album',
            'q':s_query,
            'offset':offset,
            'limit':limit
        }, get_=True)
        if 'error' in response or 'Error' in response:
            return Response({
            'result':False
            }, status=status.HTTP_200_OK)
        if type=='tracks':
            result=get_tracks(response[type]['items'])
        else:
            result=get_albums(response[type]['items'])
        return Response({
            'result':result
        }, status=status.HTTP_200_OK)
        
        

class AlbumTracks(APIView):
    def get(self, request, format=None):
        album_id = request.GET.get('id')
        offset=request.GET.get('offset')
        limit=request.GET.get('limit')
        # /v1/albums/id/tracks
        endpoint='/albums/{id}/tracks'.format(id=album_id)
        user_id=self.request.session.get('user_id')
        response=execute_spotify_api_request(user_id , endpoint , get_=True)
        if 'error' in response or 'Error' in response:
            return Response({
            'result':False
            }, status=status.HTTP_200_OK)
        result=get_only_tracks(response['items'])
        return Response({
        'result':result
        }, status=status.HTTP_200_OK)

