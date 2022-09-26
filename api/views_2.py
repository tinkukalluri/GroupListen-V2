from django.shortcuts import render
from rest_framework import generics, status  
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect

from .models import Messages,Room,Users


# all chat support urls functions in this views_2.py

def loggedIn(request):
    # return True
    if request.session.get('user_id'):
        return True
    else:
        return False

def push_to_msgs(row ,msgs ):
    msgs[row.id]={}
    msgs[row.id]['text']=row.text
    msgs[row.id]['msg_from']=row.msg_from.id
    msgs[row.id]['room_id']=row.room_id.id
    msgs[row.id]['delivered']=row.delivered
    msgs[row.id]['seen']=row.seen
    msgs[row.id]['send_on']=row.send_on
    msgs[row.id]['photoURL']=row.msg_from.photoURL



class FetchMessages(APIView):
    def get(self, request , format=None):
        msgs={}
        if loggedIn(request):
            ##print("user_logged_in")
            post_data = dict(request.data)
            ##print(post_data)
            room_code = self.request.session.get('room_code')
            msgs[-1]=self.request.session.get('user_id')
            ##print("user authenticated by session")
            user_obj=Users.objects.filter(id=msgs[-1])[0]
            room_obj=Room.objects.filter(code=room_code)[0]
            querySet=Messages.objects.filter(room_id=room_obj.id)
            if querySet.exists():
                for row in querySet:
                    push_to_msgs(row , msgs)
            ##print(msgs)
            return Response(msgs , status=status.HTTP_200_OK)
        else:
            ##print("user not logged")
            return Response({"user_not_logged_in":False }, status=status.HTTP_204_NO_CONTENT)


def getPhotoURL(user_obj):
    return user_obj.photoURL


class InputText(APIView):
    def post(self, request, format=None):
        if loggedIn(request):
            post_data = request.data
            self.user_id=self.request.session['user_id']
            self.room_code=self.request.session['room_code']
            self.text=post_data["text"]
            ##print("inputtext")
            ##print(self.user_id , self.room_code , self.text)
            self.user_obj=Users.objects.filter(id=self.user_id)[0]
            self.photoURL=self.user_obj.photoURL
            getPhotoURL(self.user_obj)
            self.room_obj=Room.objects.filter(code=self.room_code)[0]
            msg_obj=Messages(msg_from=self.user_obj ,room_id=self.room_obj,
                text=self.text
            )
            self.msg={}
            msg_obj.save(msg_obj)
            push_to_msgs(msg_obj , self.msg)
            return Response({
                "lets_go":"yooy",
                "msg_id":msg_obj.id,
                "msg_data":self.msg
            } , status=status.HTTP_200_OK)
        else:
            ##print("user not logged")
            return Response({"something went wrong":False }, status=status.HTTP_204_NO_CONTENT)