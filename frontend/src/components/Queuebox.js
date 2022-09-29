import React, { useEffect, useState } from 'react'

export default function Queuebox(props) {

    const [queue, setQueue] = useState(-1)
    const [queueJSX, setQueueJSX] = useState(-1)
    const [prevQueueTrack, setprevQueueTrack] = useState(-1)

    useEffect(() => {
        const q_intervel = setInterval(() => {
            getQueue()
        }, 10000)

        return () => {
            clearInterval(q_intervel)
        }
    }, [])


    function getQueue() {
        fetch('/spotify/get-room-queue', { method: "GET" }).then(response => response.json()).then(data => {
            console.log(data)
            if (data.Error == undefined && data.error == undefined && data.queue != undefined) {
                setQueue(data.queue)
            }

        })
    }

    const songProgress = (parseInt(props.time) / parseInt(props.duration)) * 100;
    if (songProgress >= 99 && songProgress <= 100 && props.id != prevQueueTrack) {
        if (queue.length > 0 && props.title) {
            setprevQueueTrack(props.id)
            props.playtrack(queue[0].track.track_id)
        }
    }


    function up_down_vote(track_id) {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                'track_id': track_id
            })
        }
        fetch('/spotify/up-down-vote', requestOptions).then(response => response.json())
            .then(data => {
                console.log(data)
            })
    }

    function handleListClick(e, track_id) {
        // props.playtrack(track_id)
        up_down_vote(track_id)

    }

    function getQueueJSX() {
        if (queue != -1) {
            var t = queue.map((v, i, items) => {
                return (
                    <div className="playlist-item-container" style={v.tot_votes <= 0 ? { 'display': 'none' } : {}}>
                        <a class="playlist-item" onClick={(e) => { handleListClick(e, v.track.track_id) }} >
                            {v.track.track_name}
                        </a>
                        <div className='tot_votes'>{v.tot_votes}</div>
                    </div>
                    // <a class="playlist-item" href={v.track_uri} onClick={(e) => { handleListClick(e, v.track_id) }} >
                    //     {v.track_name}
                    // </a>
                )
            }
            )
            // checking if we reached the end of the song so as to play next song in the queue
            t.splice(0, 0, <h3>Your Queue</h3>)
            console.log(t)
            setQueueJSX(t)
        }
    }

    useEffect(() => {
        getQueueJSX()
    }, [queue])

    return (
        <div>
            {queueJSX == -1 ? <h4>Loading</h4> : queueJSX}
        </div>
    )
}
