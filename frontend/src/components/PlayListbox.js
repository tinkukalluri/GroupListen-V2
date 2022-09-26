import React, { useEffect, useState } from 'react'



// importing css
import './css/PlaylistBox.css'
import PlaylistTracks from './PlaylistTracks'


export default function PlayListbox(props) {

    const [playlists, setPlaylists] = useState({})
    const [playListsJSX, setPlaylistsJSX] = useState([])
    const [playlistsId, setPlaylistId] = useState(-1)

    function getPlayLists(offset = 0, limit = 20) {
        const path = `/spotify/get-playlists?offset=${offset}&limit=${limit}`
        fetch(path, { method: 'GET' }).then(response => response.json()).then(data => {
            console.log(data.tinku)
            console.log(data)
            if (data.Error == undefined && data.error == undefined && data.playlists != undefined) {
                setPlaylists(data)
            }
        })
    }

    useEffect(
        () => {
            getPlayLists()
        }
        , [])


    useEffect(() => {
        const jsx = getPlayListsJSX()
        setPlaylistsJSX(jsx)
    }, [playlists])


    function getPlayListsJSX() {
        if (playlists.Error == undefined && playlists.playlists != undefined) {
            const l1 = []
            var arr_list = playlists.playlists
            arr_list.forEach((v, i) => {
                l1.push(
                    <a class="playlist-item" onClick={(e) => {
                        handleListClick(e, v.id)
                    }}>
                        {v.name}
                    </a>
                )
            })
            l1.splice(0, 0, <h3 style={{ 'text-align': 'center' }}>Your Playlists</h3>)
            return l1
        }
    }

    function getMeBack() {
        setPlaylistId(-1)
    }



    function handleListClick(e, id) {
        setPlaylistId(id)
        console.log(id)
    }



    return (
        <div class='playlist-box-container'>
            <div className='playlist-box-flex'>
                {playlistsId == -1 ? playListsJSX : <PlaylistTracks id={playlistsId} back={getMeBack} playtrack={props.playtrack} />}
            </div>
        </div>
    )
}
