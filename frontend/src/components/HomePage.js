import React, { Component, useState, useEffect } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import Info from "./Info"
import FirebaseLogin from "./FirebaseLogin"
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";

// importing css
import './css/Homepage.css'




export default function HomePage(props) {

    function authenticateUser() {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({

            }),
        }
        fetch('/api/authenticate', requestOptions).then(function (response) {
            return response.json()
        }).then((data) => {
            if (data.result) {
                console.log("user successfully authenticated", data.result);
            } else {
                window.location.replace('/')
                console.log("user not authenticated")
            }
        })
    };


    function logoutPressed(e) {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({})
        }
        fetch("/api/logout", requestOptions).then((response) => {
            return response.json()
        }).then(data => {
            if (data.status) {
                console.log("logged out", data)
                // window.location.replace('/')
            } else {
                console.log("looks like something went wrong")
            }
            authenticateUser()
        })
    }



    // component did mount
    useEffect(() => {
        authenticateUser()
    }, [])

    function renderHomePage() {
        return (
            <div className="homepage-container">
                <Grid container spacing={3}>
                    <Grid item xs={12} align="center">
                        <Typography variant="h3" compact="h3">
                            Group Listen-V2
                        </Typography>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <ButtonGroup disableElevation variant="contained" color="primary">
                            <Button color="primary" to="/join" component={Link}>
                                Join a Room
                            </Button>
                            <Button color="default" to="/info" component={Link}>
                                Info
                            </Button>
                            <Button color="secondary" to="/create" component={Link}>
                                Create a Room
                            </Button>
                        </ButtonGroup>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Button color="default" to="/" component={Link} onClick={logoutPressed} >
                            Logout
                        </Button>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <h6 className="portfolio-link">Application Build by <a style={{
                            'text-decoration': 'underline',
                            'color': 'var(--sp-green)'
                        }} href="https://kalluriabhinandan.web.app/" target="_blank"> Abhinandan Kalluri.</a></h6>
                    </Grid>
                </Grid>
            </div>
        );
    }



    return (
        <>
            < Router >
                <Switch>
                    <Route exact path="/info" component={Info} />z
                    <Route
                        exact
                        path="/home"
                        render={(props) => {
                            return renderHomePage()
                        }}
                    />
                    {/* <Route
                        exact
                        path="/"
                        render={(props) => {
                            return <FirebaseLogin />
                        }}
                    /> */}
                    <Route
                        path="/join"
                        render={(props) => {
                            return <RoomJoinPage {...props} />
                        }} />
                    <Route path="/create"
                        render={
                            (props) => {
                                return (<CreateRoomPage {...props} />)
                            }
                        } />
                    <Route
                        path="/room/:roomCode"
                        render={(props) => {
                            return <Room {...props} />;
                        }}
                    />
                </Switch>
            </Router >
        </>
    )
}
