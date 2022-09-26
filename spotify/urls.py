from django.urls import path 
from . import views
from . import views_2

urlpatterns = [
    # path('spotify-view' , views.spotifyView),
    path('get-auth-url' , views.AuthURL.as_view()),
    path('redirect' , views.spotify_callback.as_view()),
    path('is-authenticated' , views.IsAuthenticated.as_view()),
    path('current-song' , views.CurrentSong.as_view()),
    path('pause' , views.PauseSong.as_view()),
    path('play' , views.PlaySong.as_view()),
    path('skip-song' , views.SkipSong.as_view()),
    path('get-playlists' , views_2.GetPlaylists.as_view()),
    path('playlists-tracks' , views_2.GetPlaylistsTracks.as_view()),
    path('get-queue' , views_2.GetQueue.as_view()),
    path('play-track' , views_2.PlayTrack.as_view()),
    path('add-to-queue' , views_2.AddToQueue.as_view()),
    path('get-room-queue' , views_2.GetRoomQueue.as_view()),
    path('up-down-vote' , views_2.UpDownVotes.as_view()),
    path('sync-track' , views_2.Sync_track.as_view()),
    path('search' , views_2.Search.as_view()),
    path('album-tracks', views_2.AlbumTracks.as_view()),
]