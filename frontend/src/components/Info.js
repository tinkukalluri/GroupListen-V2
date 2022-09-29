import React, { useState, useEffect } from "react";
import { Grid, Button, Typography, IconButton } from "@material-ui/core";
import NavigateBeforeIcon from "@material-ui/icons/NavigateBefore";
import NavigateNextIcon from "@material-ui/icons/NavigateNext";
import { Link } from "react-router-dom";


// importing css
import './css/Info.css'

const pages = {
    JOIN: "pages.join",
    CREATE: "pages.create",
};

export default function Info(props) {
    const [page, setPage] = useState(pages.JOIN);

    function joinInfo() {
        return (
            <>
                <p>
                    Click on the "Join" button and enter the unique six digit code you have
                    to join into your friends group, if you don't have one create a room.
                </p>
            </>
        )
    }

    function createInfo() {
        return (
            <>
                <p>
                    Click on the "create" button to create a room and be the host and share the url to friends
                    and family to invite them to join the group.
                </p>
            </>
        )
    }


    useEffect(() => {
        console.log("ran");
        return () => console.log("cleanup");
    });

    if (props.home != undefined && props.home == true) {
        return (
            <>
                <div className="info-container">
                    <Grid container spacing={1}>
                        <Grid item xs={12} align="center">
                            <ol>
                                <li>
                                    <p>Open the offical spotify applicatioin in a different tab or windows application and play any music
                                        and let the music play in the background
                                        <br />
                                        By doing so u can see that the music playing in the offical spotify is being showed
                                        in the music player of GroupListen app
                                    </p>
                                </li>
                                <li>
                                    <p>Make sure you have cleared the Queue in the offical spotify
                                        applicatioin for the first time</p>
                                </li>
                                <li>
                                    <p>If your not able to play/pause or skip or your queue is not
                                        being played as expected means your using a free account of
                                        spotify to unlock the full potential of our app make sure you
                                        purchase the premium account of spotify</p>
                                </li>
                            </ol>
                        </Grid>
                        <Grid item xs={12} align="center">
                            <Button color="secondary" variant="contained" onClick={(e) => {
                                props.handleInfoButtonClick(e)
                            }} >
                                Back
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
            </>
        )
    }
    else {
        return (
            <div className="info-container">
                <Grid container spacing={1}>
                    <Grid item xs={12} align="center">
                        <Typography component="h4" variant="h4">
                        </Typography>
                        <p>
                            What is House Party?<br />
                            It is a new way for people to play music together in real time <br />
                            Members in the group can send and receive messages<br />
                            Members can upvote or downvote a song, the one with the highest number of
                            votes will be the next track to play<br />
                            You can add songs from your playlist and also from search into queue
                        </p>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Typography variant="body1">
                            {page === pages.JOIN ? joinInfo() : createInfo()}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <IconButton
                            onClick={() => {
                                page === pages.CREATE ? setPage(pages.JOIN) : setPage(pages.CREATE);
                            }}
                        >
                            {page === pages.CREATE ? (
                                <NavigateBeforeIcon />
                            ) : (
                                <NavigateNextIcon />
                            )}
                        </IconButton>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Button color="secondary" variant="contained" to="/home" component={Link} onClick={(e) => {
                            // catch (TypeError) {
                            //     window.location.replace('/home')
                            // }
                        }} >
                            Back
                        </Button>
                    </Grid>
                    <Grid item xs={12}>
                        <h6 className="portfolio-link" >Application Build by <a style={{
                            'text-decoration': 'underline',
                            'color': 'var(--sp-green)'
                        }} href="https://kalluriabhinandan.web.app/" target="_blank"> Abhinandan Kalluri.</a></h6>
                        <p style={{ 'margin': '0' }}>
                            The github repository of GroupListen-V2 project is private.<br />
                            The github repository of GroupListen is public.<br />
                        </p>
                    </Grid>
                </Grid>
            </div >
        );
    }
}
