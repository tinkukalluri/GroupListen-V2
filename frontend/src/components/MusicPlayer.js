import React, { Component } from "react";
import {
    Grid,
    Typography,
    Card,
    IconButton,
    LinearProgress,
} from "@material-ui/core";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import PauseIcon from "@material-ui/icons/Pause";
import SkipNextIcon from "@material-ui/icons/SkipNext";



// importing css
import './css/MusicPlayer.css'



export default class MusicPlayer extends Component {
    static defaultProps = {
        image_url: "https://www.gstatic.com/webp/gallery/5.jpg"
    };

    constructor(props) {
        super(props);
        this.pauseSong = this.pauseSong.bind(this);
        this.playSong = this.playSong.bind(this);
        this.skipSong = this.skipSong.bind(this);
    }

    pauseSong() {
        const requestOptions = {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
        };
        fetch("/spotify/pause", requestOptions);
    }

    playSong() {
        const requestOptions = {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
        };
        fetch("/spotify/play", requestOptions);
    }

    skipSong() {
        fetch('/spotify/skip-song', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        })
    }

    render() {
        const songProgress = (parseInt(this.props.time) / parseInt(this.props.duration)) * 100;
        // console.log(songProgress + "%");
        return (
            <Card style={{ "background": "#8C8C8C", "border-radius": "28px" }}>
                <Grid style={{ "background": "#8C8C8C" }} container alignItems="center">
                    <Grid item align="center" xs={4}>
                        <img src={this.props.image_url} alternate="no_image" height="100%" width="100%" />
                    </Grid>
                    <Grid item align="center" xs={8}>
                        <Typography style={{ "inline-size": "max-content" }} component="h5" variant="h5">
                            {this.props.title}
                        </Typography>
                        <Typography style={{ "inline-size": "max-content" }} color="textSecondary" variant="subtitle1">
                            {this.props.artist}
                        </Typography>
                        <div className="pause-skip-container">
                            <IconButton onClick={() => {
                                this.props.is_playing ? this.pauseSong() : this.playSong()
                            }}>
                                {this.props.is_playing ? <PauseIcon /> : <PlayArrowIcon />}
                            </IconButton>
                            <IconButton onClick={this.skipSong}>
                                <SkipNextIcon />
                            </IconButton>
                            <h5>{this.props.votes} / {this.props.votes_required} </h5>

                        </div>
                    </Grid>
                </Grid>
                <LinearProgress variant="determinate" value={songProgress} />
            </Card>
        );
    }
}
