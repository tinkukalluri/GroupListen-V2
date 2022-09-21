import React, { useState, useEffect } from "react";
// import Form from "react-bootstrap/Form";
// import Button from "react-bootstrap/Button";
import { TextField, Grid, Button, ButtonGroup, Typography, FormControlLabel, Checkbox } from "@material-ui/core";
import { Link } from "react-router-dom";


// importing css
import './css/msgbox.css'

// importing statics/images/icon
import default_img from '../../static/images/no_image.jpg'



export default function MsgBox(props) {

    const [msgs, setMsgs] = useState(props.msgs)

    // useEffect(() => {
    //     //console.log(msgs)
    // }, [msgs])
    //console.log(props.msgs)



    function renderMsgs() {
        let list = []
        var entries = Object.entries(props.msgs)
        entries = _sort(entries)
        console.log("sorted entries: ", entries)
        //console.log("entries from Msgbox", entries)
        for (let msg in entries) {
            //console.log("renderMsg()")
            //console.log(msg)
            list.push(
                // <Typography variant="h6" compact="h6">
                //     {"id" + entries[msg][0] + "   msg_from" + entries[msg][1].msg_from + "   msg_to" + entries[msg][1].msg_to + "  " + entries[msg][1].text + "   " + entries[msg][1].send_on}

                // </Typography>
                classPlacer(entries, msg)
            )
        }
        //console.log("list from MsgBox ", list);
        return list;
    }



    function _sort(arr) {
        arr.sort((a, b) => {
            var t1 = date_timeParser(a[1].send_on)
            var t2 = date_timeParser(b[1].send_on)
            if (t1.date.y < t2.date.y) {
                return -3;
            } else if (t1.date.y > t2.date.y) {
                return 3
            } else if (t1.date.y == t2.date.y) {
                if (t1.date.m < t2.date.m) {
                    return -3;
                } else if (t1.date.m > t2.date.m) {
                    return 3
                } else if (t1.date.m == t2.date.m) {
                    if (t1.date.d < t2.date.d) {
                        return -3;
                    } else if (t1.date.d > t2.date.d) {
                        return 3
                    } else if (t1.date.d == t2.date.d) {
                        if (t1.time.h < t2.time.h) {
                            return -4;
                        } else if (t1.time.h > t2.time.h) {
                            return 3;
                        } else if (t1.time.h == t2.time.h) {
                            if (t1.time.m < t2.time.m) {
                                return -4;
                            } else if (t1.time.m > t2.time.m) {
                                return 3;
                            } else if (t1.time.m == t2.time.m) {
                                if (t1.time.s < t2.time.s) {
                                    return -4;
                                } else if (t1.time.s > t2.time.s) {
                                    return 3;
                                } else if (t1.time.s == t2.time.s) {
                                    if (t1.time.ns < t2.time.ns) {
                                        return -4;
                                    } else if (t1.time.ns > t2.time.ns) {
                                        return 3;
                                    } else if (t1.time.ns == t2.time.ns) {
                                        return 0
                                    }
                                }
                            }
                        }
                    }
                }
            }
        })
        return arr;
    }

    function date_timeParser(str) {
        let l1 = str.split('T')
        let date = l1[0].split('-')
        let date_year = date[0].trim()
        let date_month = date[1].trim()
        let date_date = date[2].trim()

        let t = l1[1].split('.')
        let t_ns = t[1]
        t = t[0].split(':')
        let t_h = t[0]
        let t_m = t[1]
        let t_s = t[2]
        return {
            date: {
                d: parseInt(date_date),
                m: parseInt(date_month),
                y: parseInt(date_year)
            },
            time: {
                h: parseInt(t_h),
                m: parseInt(t_m),
                s: parseInt(t_s),
                ns: parseInt(t_ns)
            }
        }
    }


    function data_time(str) {
        let l1 = str.split('T')
        let t = l1[1].split('.')
        t = t[0]
        return t
    }


    function classPlacer(entries, msg) {
        let myid = props.myid;
        if (myid === entries[msg][1].msg_from) {
            return (
                <div class="_container sender">
                    <span class="time-left onhover-show-js">{data_time(entries[msg][1].send_on)}</span>
                    <div class="user-sender">
                        {entries[msg][1].text}
                    </div>
                    <img class="right onhover-show" src={entries[msg][1].photoURL == null ? default_img : entries[msg][1].photoURL} alt="sender" />
                </div>
            )
        } else {
            return (
                <div class="_container receiver">
                    <img class="left onhover-show" src={entries[msg][1].photoURL == null ? default_img : entries[msg][1].photoURL} alt="reciver" />
                    <div class="contact-sender">
                        {entries[msg][1].text}
                    </div>
                    <span class="time-right ">{data_time(entries[msg][1].send_on)}</span>
                </div>
            )
        }
    }


    return (
        <>
            <div className="msgbox-container">
                <Grid container spacing={1} >
                    <Grid item xs={12}>
                        {renderMsgs()}
                    </Grid>
                </Grid>
            </div>
        </>
    )

}