import json



def getPlaylist_href(data):
    return data['href']

def getImages(imgs):
    l1=[]
    for img in imgs:
        return l1.append(img['url'])
    return l1

def getPlaylists_items(data):
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



path='C:\\Users\\sintin\\Desktop\\Projects_3\\GroupListen-V2\\GroupListen-V2\\GroupListen-V2\\spotify\\example_jsons\\playlists.json'
# path=patWSh.replace('\\' , '/')
l1=[]
with open(path) as json_file:
    data = json.load(json_file)
    d=getPlaylists_items(data)
    #print(d[0])


