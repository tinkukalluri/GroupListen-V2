
from django.shortcuts import render , redirect
from rest_framework import generics, status

from spotify.models import SpotifyToken
from .serializers import RoomSerializer, CreateRoomSerializer , UpdateRoomSerializer
from .models import Room, Users    
from rest_framework.views import APIView
from rest_framework.response import Response    
from django.conf import settings
import datetime
from spotify.models import *
# Create your views here.
# generics.createAPIView

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    return response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )



class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.get('user_id')
            user=Users.objects.filter(id=host)[0]
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = RoomSerializer(room).data.get("code")
                #print("room code update:"+RoomSerializer(room).data.get("code"))
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=user, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip )
                room.save()
                # creating a queue
                queue_obj=Queue(user_id=user, room_id=room , guests={
                    'guests':[host]
                })
                queue_obj.save()
                self.request.session['room_code'] = RoomSerializer(room).data.get("code")
                self.request.session['room_id'] = RoomSerializer(room).data.get("id")
                #print("room code new host:"+RoomSerializer(room).data.get("code"))
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


def addGuests(user_id , room_code):
    room_obj=Room.objects.filter(code=room_code)
    if room_obj.exists():
        room_obj=room_obj[0]
        room_guests=room_obj.guests
        room_guest_list=room_guests['guests']
        try:
            room_guest_list.index(user_id)
        except ValueError:
            room_guest_list.append(user_id)
            room_obj.save(update_fields=['guests'])
        return True
    return False


def removeGuests(user_id , room_code):
    room_obj=Room.objects.filter(code=room_code)
    if room_obj.exists():
        room_obj=room_obj[0]
        room_guests=room_obj.guests
        room_guest_list=room_guests['guests']
        try:
            room_guest_list.index(user_id)
        except ValueError:
            room_guest_list.remove(user_id)
            room_obj.save(update_fields=['guests'])
        return True
    return False





class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if room.exists():
                #print("the room[].host:"+room[0].code)
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session['user_id'] == room[0].host.id
                self.request.session['room_code'] = room[0].code
                self.request.session['room_id']=room[0].id
                if addGuests( self.request.session['user_id'] ,room[0].code ):
                #print("session data in GetRoom:"+self.request.session['room_code'])
                    return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Code paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)



class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if room_result.exists():
                room = room_result[0]
                self.request.session['room_code'] = code
                res= addGuests( self.request.session['user_id'] ,room.code )
                if res:
                    return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_205_RESET_CONTENT)

        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


class UserInRoom(APIView):
    def get(self, request,format=None):
        #print("user in room:"+str((self.request.session.get('room_code')!=None)))
        if(self.request.session.get('room_code')):
            return Response({"code":self.request.session['room_code']},status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)


class LeaveRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            code=self.request.session.pop("room_code")
            user_id=self.request.session['user_id']
            # room_result= Room.objects.filter(host=user_id)
            room_result= Room.objects.filter(code= code)
            if room_result.exists():
                room=room_result[0]
                if room.host.id==user_id:
                    room.delete()
                else:
                    if removeGuests(user_id , code):
                        return Response({"message":"sucesss"} , status=status.HTTP_200_OK)
            return Response({"message":"something went wrong"} , status=status.HTTP_400_BAD_REQUEST)



class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session['user_id']
            if room.host.id != user_id:
                return Response({'msg': 'You are not the host of this room.'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)


# not using this way of logingin
class Login(APIView):
    def post(self, request, format=None):
        post_data = request.data
        self.username = post_data.get('username')
        self.password =  post_data.get('password')
        user=Users.objects.filter(username=self.username, password=self.password)
        if user.exists():
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
                self.request.session["key"]=self.request.session.session_key
                self.request.session["user_id"]=user[0].id

class LoginWithGoogle(APIView):
    def post(self, request, format=None):
        post_data = dict(request.data)
        #print("type" , type(post_data))
        #print("post_data====" , post_data)
        # user.multiFactor.user.uid
        uid=post_data['authResult']['uid']
        accessToken=post_data['authResult']['accessToken']
        refreshToken=post_data['authResult']['refreshToken']
        photoURL=post_data['authResult']['photoURL']
        phoneNumber=post_data['authResult']['phoneNumber']
        providerId=post_data['authResult']['providerId']
        displayName=post_data['authResult']['displayName']
        email=post_data['authResult']['email']
        emailVerified=post_data['authResult']['emailVerified']
        #print(uid,accessToken , refreshToken)
        queryset=Users.objects.filter(google_uid=uid)
        if queryset.exists():
            self.user=queryset[0]
            self.request.session.create()
            self.request.session["key"]=self.request.session.session_key
            self.request.session["user_id"]=self.user.id
            return Response({"result":True} , status=status.HTTP_200_OK)
            # return redirect('frontend:homepage')
        else:
            self.user=Users(google_uid=uid , email_uid=email , username="" , password="" , photoURL=photoURL)
            self.user.save()
            self.request.session.create()
            self.request.session["key"]=self.request.session.session_key
            self.request.session["user_id"]=self.user.id
            return Response({"result":True} , status=status.HTTP_200_OK )
            # return redirect('frontend:homepage')
            # return Response({"result":False} , status=status.HTTP_400_BAD_REQUEST)
        

class Authenticate(APIView):
    def post(self, request, format=None):
        post_data=dict(request.data)
        #print("from authenticate" , dict(self.request.session))
        if self.request.session.get('user_id')!= None:
        # if self.request.session.exists(self.request.session.get('user_id'):
            return Response({"result":self.request.session['user_id']} , status=status.HTTP_200_OK)
        else:
            return Response({"result":False} , status=status.HTTP_200_OK)




class Logout(APIView):
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            return Response({"status": True} , status=status.HTTP_200_OK)
        if "user_id" in self.request.session:
            tk=SpotifyToken.objects.filter(user=self.request.session['user_id'])
            if tk.exists():
                tk=tk[0]
                tk.delete()
            s_id= self.request.session.pop("user_id" , None)
            return Response({"status": True} , status=status.HTTP_200_OK)
        return Response({"status": True} , status=status.HTTP_200_OK)
