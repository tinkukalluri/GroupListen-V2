import React, { useEffect, useState } from 'react'

export default function PlaylistTracks(props) {
    const [playlistTracks, setPlaylistTracks] = useState(-1)
    const [playlistTracksJSX, setPlaylistTracksJSX] = useState(-1)


    useEffect(() => {
        getPlaylistTracks()
    }, [])

    function getPlaylistTracks(offset = 0, limit = 100) {
        if (props.album) {
            var endpoint = `/spotify/album-tracks?id=${props.id}&offset=${offset}&limit=${limit}`
            fetch(endpoint).then(response => response.json()).then(data => {
                console.log(data)
                setPlaylistTracks(data.result)
                getPlaylistTracksJSX(data.result)
            })
        } else {
            var path = `/spotify/playlists-tracks?id=${props.id}&offset=${offset}&limit=${limit}`
            fetch(path, { method: 'GET' }).then(response => response.json()).then(data => {
                console.log(data.tinku)
                console.log(data)
                if (data.Error == undefined && data.error == undefined && data.tracks != undefined) {
                    setPlaylistTracks(data.tracks)
                    getPlaylistTracksJSX(data.tracks)
                }
            })
        }
    }

    function handleListClick(e, track_id) {
        // props.playtrack(track_id)
        addToQueue(e, track_id)
        console.log(track_id)
    }

    function addToQueue(e, track_id) {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                'track_id': track_id
            })
        }

        fetch('/spotify/add-to-queue', requestOptions).then(response => response.json())
            .then(data => {
                console.log(data)
            })
    }

    function getPlaylistTracksJSX(tracks) {
        var t = tracks.map((v, i, items) => {
            return (
                <a class="playlist-item" onClick={(e) => { handleListClick(e, v.track_id) }} >
                    {v.track_name}
                </a>
            )
        }
        )
        console.log(t)
        setPlaylistTracksJSX(t)
    }



    return (
        <>
            <a class="playlist-item" onClick={(e) => { props.back() }} >
                back
            </a>
            {playlistTracksJSX == -1 ? <h4>Loading</h4> : playlistTracksJSX}
        </>
    )
}

