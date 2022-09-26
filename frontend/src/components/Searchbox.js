import React from 'react'
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { useState, useEffect } from 'react';

// importing user defined components
import AlbumTracks from './PlaylistTracks';



export default function Searchbox(props) {

    // qTrack will give the info on what to querey the seach on is it tracks or albums
    const [qTrack, setqTrack] = useState(true)
    const [searchResult, setSearchResult] = useState('')
    const [searchResultJSX, setSearchResultJSX] = useState('')
    const [albumId, setAlbumId] = useState(-1)

    var q = props.search_q

    function q_fun() {
        fetch(`/spotify/search?q=${q}&type=${qTrack ? 'tracks' : 'albums'}`).then(response => response.json()).then(data => {
            console.log(data)
            if (data.Error == undefined && data.error == undefined && data.result != undefined) {
                setSearchResult(data.result)
            }
        })
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

    useEffect(() => {
        q_fun()
    }, [qTrack, q])

    function handleListClick(e, track_id) {
        console.log(track_id, ' from handleClick')
        addToQueue(e, track_id)
    }

    function handleAlbumClick(e, album_id) {
        setAlbumId(album_id)
    }

    function getJSX() {
        if (searchResult != '') {
            if (qTrack) {
                // we are showing 
                var t = searchResult.map((v, i, items) => {
                    return (
                        <a class="playlist-item" onClick={(e) => { handleListClick(e, v.track_id) }} >
                            {v.track_name}
                        </a>
                    )
                })
                setSearchResultJSX(t)
            } else {
                // it a album we are showing to the user
                var t = searchResult.map((v, i, items) => {
                    return (
                        <a class="playlist-item" onClick={(e) => { handleAlbumClick(e, v.album_id) }} >
                            {v.album_name}
                        </a>
                    )
                })
                setSearchResultJSX(t)
            }
        }
    }

    useEffect(() => {
        getJSX();
    }, [searchResult])

    function getMeBack() {
        setAlbumId(-1)
    }


    function handleQChange(e) {
        const val = e.target.value === "true" ? true : false
        console.log('handleQChagehandleQChagehandleQChagehandleQChagehandleQChage')
        console.log(val)
        setqTrack(val)
    }

    return (
        <div>
            <RadioGroup
                style={{ 'justify-content': 'center' }}
                row
                defaultValue={qTrack.toString()}
                onChange={(e) => { handleQChange(e) }}
            >
                <FormControlLabel
                    value="false"
                    control={<Radio color="primary" />}
                    label="albums"
                    labelPlacement="bottom"
                />
                <FormControlLabel
                    value="true"
                    control={<Radio color="secondary" />}
                    label="tracks"
                    labelPlacement="bottom"
                />
            </RadioGroup>
            {albumId == -1 ? searchResultJSX : <AlbumTracks id={albumId} back={getMeBack} album={true} />}
        </div >
    )
}
