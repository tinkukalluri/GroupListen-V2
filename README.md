# GroupListen-V2

# Note

1.To unlock the full functionality of the application you need to have spotify premium account

2.[link to AWS EC2 instance running application](http://3.14.245.28/)()(Web socket protocol may not work)(Do not use https protocol use only http)

# GroupListen Features

## Login page
- Used firebase authorization(google's OAuth) to log user's in.
![image](https://user-images.githubusercontent.com/75239213/193472120-048da497-07f9-4bbd-aec6-0c5bbb1520c2.png)
- User's can login using there gmail
---
<img alt="google-login" src="https://user-images.githubusercontent.com/75239213/193474113-43fda0d0-7b54-4f42-93f2-5d1f7f1de6f0.png" width="36%">

---

## Home page
  ![image](https://user-images.githubusercontent.com/75239213/193472148-ef5930de-dda1-4147-b2c8-1c8758e4d9ed.png)

## Create-room page
- Here you can create a room and be the host of the party share the url/room-code with friends and family to invite them into the party
![image](https://user-images.githubusercontent.com/75239213/193472211-122a85ca-6f46-4e1d-9d8a-4186798790d1.png)

## Join-room page
- Use 6 digit unique code to enter into your friends room and have blast
![image](https://user-images.githubusercontent.com/75239213/193472204-4c46e3f3-6a53-49ce-a003-a9e769a5e014.png)

## Room page
- This is the console where you can see the currently playing music, tracks next in the queue, your platlists and chat with mate's in the room
![image](https://user-images.githubusercontent.com/75239213/193473733-3b880e97-52b8-485a-8c30-41d0e6d62dd1.png)

---

### User's Spotify Playlist's
- Here you can find all the playlist's create by you in the spotigy application of your's
- you can add tracks from your playlist to queue
<br/>
  <img alt="playlist/search" src="https://user-images.githubusercontent.com/75239213/193472372-cbc16703-8eee-466f-9c32-a58c5e7c711a.png" width="36%">

### Room Queue
- here you will find the songs in the queue the track with the most votes will be the next track that's going to play
<br/>
  <img alt="queue" src="https://user-images.githubusercontent.com/75239213/193472389-774947e9-08a6-476b-a4c7-82d37fc5a06d.png" width="36%">

### Chat implemented using Web Socket protocol
- You can interact with your room mate's here
<br/>
  <img alt="messages" src="https://user-images.githubusercontent.com/75239213/193472405-3b996a97-e3d4-4326-99dc-755a76f679f5.png" width="36%">

## Track Search
- you can search for the track and add it to the queue
<img alt='track-search' src='https://user-images.githubusercontent.com/75239213/193475776-1a7de0fe-8b0b-4286-9599-1365d68fe5f0.png' width="36%" />

## Album Search
- search for the album and add it to the queue
<img alt='album-search' src='https://user-images.githubusercontent.com/75239213/193475784-0093792c-23aa-4855-a8aa-b1c318b28a14.png' width="36%"/>

## Room Setting's
- If your the host then you can update the room settings or leave the room
- if your guest you can only leave the room
![image](https://user-images.githubusercontent.com/75239213/193473233-0aeee728-dec6-43be-8bb2-35410ee8251c.png)


# Installation Guid

Download the source code Zip file and and unzip it.

## Pip Installation 
1. Go inside the root directory of the project  where you can find the requirements.txt file
![image](https://user-images.githubusercontent.com/75239213/192565589-0180c8f7-c1b4-4c8d-8680-2083647d7edb.png)

2. copy the path of the root directory
![image](https://user-images.githubusercontent.com/75239213/192565852-a467e99f-ba5a-4d1b-93a5-008f1fb5f2f2.png)

3.Open cmd and cd to root directory
  `cd <path to root directory>` 

4.run `pip install -r requirements.txt`



## Getting Spotify Credentials

1. go to [spotify-dashboard](https://developer.spotify.com/dashboard/login) and login with your spotify account, create one if doesn't exists

2.click on create an app and follow the instruction to create an app in spotify dashboard

3.open the App just create you will find your client ID

4.click on `show client secret` to get the client secret ID

5.go to `spotify\credentials.py` and paste the Client Id and client secret ID

6.click on `Users and Access` and add your spotify account email address

7.That's it your done with spotify

## Setting mysql

1.go to mysql website and follow the installation instruction in official mysql site

2.open mysql terminal and run `create database grouplisten`

3.go `Grouplisten\settings.py`

4.update the fields like password with your mysql server
`
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'grouplisten',  
        'USER': 'root',  
        'PASSWORD': 'your password',  
        'HOST': 'localhost',  
        'PORT': '3306',  
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }  
    }  
}  
`

## Starting the Server

1.assuming you have python Installed in you system
  run `python manage.py runserver 333` !it is important to run the server in portno. 333
  
2.That's it you have started your server at localhost 333

## Opening the web app in the browser

1.In the browser url go to `localhost:333`
![image](https://user-images.githubusercontent.com/75239213/192569675-155c4bfd-4d86-442b-9a75-f237dd205e31.png)
---
2.that's it your in the GroupListen application, enjoy.
![image](https://user-images.githubusercontent.com/75239213/193472120-048da497-07f9-4bbd-aec6-0c5bbb1520c2.png)


