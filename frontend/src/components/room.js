import React, { Component } from "react";
import { Grid, Button, Typography, IconButton, TextField } from "@material-ui/core";
import { AiFillSetting } from "react-icons/ai";


import Queuebox from "./Queuebox";
import Chatbox from "./Chatbox"
import Searchbox from "./Searchbox"
import PlayListbox from "./PlayListbox";
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./MusicPlayer";


// importing css
import './css/room.css'



export default class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            showSettings: false,
            spotifyAuthenticated: false,
            song: {},
            search_q: "",
            error: "",
            show_playlist: true,
        };
        this.roomCode = this.getroomcode()
        this.updateShowSettings = this.updateShowSettings.bind(this);
        this.leaveButtonPressed = this.leaveButtonPressed.bind(this);
        this.getRoomDetails = this.getRoomDetails.bind(this);
        this.getCurrentSong = this.getCurrentSong.bind(this);
        this.handleTextFieldChange = this.handleTextFieldChange.bind(this);
        this.getRoomDetails();
        this.getCurrentSong();
    }





    getroomcode() {
        return window.location.pathname.split('/')[2].trim();
    }


    componentDidMount() {
        this.interval = setInterval(this.getCurrentSong, 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }


    getRoomDetails() {
        return fetch("/api/get-room" + "?code=" + this.roomCode)
            .then((response) => {
                if (!response.ok) {
                    // this.props.leaveRoomCallback();
                    this.leaveButtonPressed()
                    this.props.history.push("/")
                    // //console.log("get-room 404 response", response.status)
                }
                return response.json();
            })
            .then((data) => {
                this.setState({
                    votesToSkip: data.votes_to_skip,
                    guestCanPause: data.guest_can_pause,
                    isHost: data.is_host,
                });
                this.authenticateSpotify();
            });
    }

    authenticateSpotify() {
        fetch('/spotify/is-authenticated', { method: 'GET' }).then((response) => {
            if (response.ok) {
                return response.json()
            }
        }).then((data) => {
            this.setState({ spotifyAuthenticated: data.status })
            //console.log("authenticated status:" + data.status)
            if (data.status) {
            } else {
                fetch('/spotify/get-auth-url').then((response) => {
                    if (response.ok) {
                        return response.json()
                    } else {

                    }
                }).then((data) => {
                    //console.log("auth-url: " + data.url)
                    //console.log(window.location)
                    window.location.replace(data.url);
                });
            }
        });
    }

    playtrack(track_id) {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                'track_id': track_id
            })
        }
        fetch('/spotify/play-track', requestOptions).then(response => response.data()).then((data) => {
            console.log(data)
        })
    }

    leaveButtonPressed() {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        };
        fetch("/api/leave-room", requestOptions).then((response) => {
            //console.log(response.status)
            // this.props.leaveRoomCallback();
            window.location.replace('/home')
        });
    }

    renderSettingsButton() {
        return (
            <>
                <IconButton onClick={() => this.updateShowSettings(true)}>
                    <AiFillSetting style={{ "color": "black" }} />
                </IconButton>

                {/* <Button
                    variant="contained"
                    color="primary"
                    onClick={() => this.updateShowSettings(true)}
                >
                    Settings
                </Button> */}
            </>
        );
    }

    updateShowSettings(value) {
        this.setState({
            showSettings: value,
        });
    }

    renderSettings() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <CreateRoomPage
                        update={true}
                        votesToSkip={this.state.votesToSkip}
                        guestCanPause={this.state.guestCanPause}
                        roomCode={this.roomCode}
                        updateCallback={this.getRoomDetails}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={this.leaveButtonPressed}
                    >
                        Leave Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={() => this.updateShowSettings(false)}
                    >
                        Close
                    </Button>
                </Grid>
            </Grid>
        );
    }

    getCurrentSong() {
        fetch("/spotify/current-song")
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    //console.log(response)
                    //console.log("getCurrentSong::response.status:" + response.status)
                    return { "nope": "nope", }
                }
            })
            .then((data) => {
                this.setState({ song: data });
                // //console.log(data);
            });
    }

    handleTextFieldChange(e) {
        var val = e.target.value
        if (val.length > 0) {
            this.setState({
                show_playlist: false
            })
        } else {
            this.setState({
                show_playlist: true
            })
        }
        this.setState({
            search_q: val
        })
    }

    inputSearchClick(e) {
        // console.log(e)
        // this.setState({
        //     show_playlist: false
        // })
    }


    render() {
        if (this.state.showSettings) {
            return this.renderSettings();
        }
        return (
            <>
                {/* <h6>Code: {this.roomCode}
                    Votes: {this.state.votesToSkip}
                    ||Guest Can Pause: {this.state.guestCanPause.toString()}
                    ||Host: {this.state.isHost.toString()}
                    ||spotify-authorized:{this.state.spotifyAuthenticated.toString()}</h6> */}
                <div className="room-container">
                    <div className="room-left">
                        <div className="room-room-container">
                            <div className="room-search-bar">
                                <input
                                    className="input-search"
                                    type="search"
                                    placeholder="search"
                                    value={this.state.search_q}
                                    onChange={this.handleTextFieldChange}
                                    onClick={(e) => { this.inputSearchClick(e) }}
                                />
                            </div>
                            {this.state.show_playlist ? null : <div className="search-container">
                                <Searchbox />
                            </div>}
                            <div className="playlist-container">
                                <PlayListbox playtrack={this.playtrack} />
                            </div>
                        </div>
                    </div>
                    <div className="room-middle">
                        <div className="room-room-container">
                            <div className="queue-container">
                                <Queuebox playtrack={this.playtrack}  {...this.state.song} />
                            </div>
                            <div className="music-player">
                                <MusicPlayer  {...this.state.song} playtrack={this.playtrack} />
                                <div className="room-setting">
                                    {this.state.isHost ? this.renderSettingsButton() : null}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="room-right">
                        <div className="chat-container">
                            <Chatbox room_code={this.roomCode} />
                        </div>
                    </div>
                </div>
            </>
        );
    }
}
