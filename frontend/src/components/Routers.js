import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import HomePage from "./HomePage"
import FirebaseLogin from "./FirebaseLogin"
import Room from "./Room";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";

import { withRouter } from 'react-router-dom';


export default class Routers extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/" component={FirebaseLogin} />
                    <Route path="/join" component={RoomJoinPage} />
                    <Route path="/create" component={CreateRoomPage} />
                    <Route
                        path="/room/:roomCode"
                        render={(props) => {
                            return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
                        }}
                    />
                </Switch>
            </Router>
        );
    }
}