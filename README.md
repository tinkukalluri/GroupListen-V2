# GroupListen-V2

# Note

1.To unlock the full functionality of the application you need to have spotify premium

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

## Starting the Server

1.assuming you have python Installed in you system
  run `python manage.py runserver 333` !it is important to run the server in portno. 333
  
2.That's it you have started your server at localhost 333

## Opening the web app in the browser

1.In the browser url go to `localhost:333`
![image](https://user-images.githubusercontent.com/75239213/192569675-155c4bfd-4d86-442b-9a75-f237dd205e31.png)
2.that's it your in the GroupListen application, enjoy.
![image](https://user-images.githubusercontent.com/75239213/192569803-58798434-6887-4f6a-a9d7-36e8494ee77d.png)


