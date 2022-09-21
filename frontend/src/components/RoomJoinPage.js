import React, { Component } from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import { Redirect } from "react-router-dom";
import { useHistory } from "react-router-dom"
import { Navigate } from "react-router-dom";

export default class RoomJoinPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            roomCode: "",
            error: "",
        };
        this.get_user_in_room();
        this.get_user_in_room = this.get_user_in_room.bind(this);
        this.handleTextFieldChange = this.handleTextFieldChange.bind(this);
        this.roomButtonPressed = this.roomButtonPressed.bind(this);
        this.clearRoomCode = this.clearRoomCode.bind(this);
    }

    render() {
        return (
            < Grid container spacing={1} >
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4">
                        Join a Room
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error}
                        label="Code"
                        placeholder="Enter a Room Code"
                        value={this.state.roomCode}
                        helperText={this.state.error}
                        variant="outlined"
                        onChange={this.handleTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={this.roomButtonPressed}
                    >
                        Enter Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" to="/home" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid >
        );
    }

    async get_user_in_room() {
        fetch("/api/user-in-room")
            .then((response) => {
                if (response.ok) {
                    return response.json()
                } else {
                    return { "error": "no user" }
                }
            }).then((data) => {
                if (!data.error) {
                    console.log("session response", data)
                    this.setState({
                        roomCode: data.code,
                    })
                    this.props.history.push(`/room/${this.state.roomCode}`);
                }
            });
    }

    clearRoomCode() {
        this.setState({
            roomCode: null,
        });
    }


    handleTextFieldChange(e) {
        this.setState({
            roomCode: e.target.value,
        });
    }

    roomButtonPressed() {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code: this.state.roomCode,
            }),
        };
        fetch("/api/join-room", requestOptions)
            .then((response) => {
                if (response.ok) {
                    // console.log(response.json());
                    // console.log(this.props.tinku)
                    // console.log(this.props)
                    console.log(this.props.history)
                    // this.props.url1 = `/room/${this.state.roomCode}`
                    // { console.log(this.props.url1) }
                    // console.log(this.props.location.pathname)
                    this.props.history.push(`/room/${this.state.roomCode}`);
                    // useHistory().history.push(`/room/${this.state.roomCode}`)
                    // console.log(this.props.his)
                    // this.setRedirect()
                } else {
                    this.setState({ error: "Room not found." });
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }
}

