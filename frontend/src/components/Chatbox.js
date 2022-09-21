import React, { useEffect, useState } from 'react'
import { IoIosSend } from 'react-icons/io'
import { Grid, Button, Typography, IconButton, TextField } from "@material-ui/core";


// importing jsx component
import MsgBox from './MsgBox'

// importing css
import './css/Chatbox.css'


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Global variables
var csrftoken = ""
var _contact_id = -1;
var chatSocket = null;

chatSocket = new WebSocket(
    'ws://'
    + window.location.host + '/'
);

export default function Chatbox(props) {
    const [msg, setMsg] = useState('')
    const [user_id, setUser_id] = useState(0)
    const [input, setInput] = useState('')
    const [scrolled, setScrolled] = useState(0)
    const [roomCode, setRoomCode] = useState(props.room_code)

    useEffect(() => {
        console.log("innnnnnnnnnnnnnnnnn")
        var element = document.getElementById("scrollBottom");
        element.scrollTop = element.scrollHeight;
    }, [msg])

    // websocket implementaion

    useEffect(() => {
        if (chatSocket != null) {
            console.log("in not null")
        }
        setRoomCode(props.room_code)
        fetchMsgs()
    }, [])


    useEffect(() => {
        _send({
            "user_id": user_id,
            'room_code': props.room_code,
        })
    }, [user_id, roomCode])

    let _send = function (message) {
        message = JSON.stringify(message)
        console.log(message)
        _waitForConnection(function () {
            chatSocket.send(message);
        }, 1000);
    };

    let _waitForConnection = function (callback, interval) {
        if (chatSocket.readyState === 1) {
            callback();
        } else {
            var that = this;
            // optional: implement backoff for interval here
            setTimeout(function () {
                _waitForConnection(callback, interval);
            }, interval);
        }
    };


    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log("message recieved", data);
        if (typeof data['conn_status'] !== 'undefined') {
            console.log("inside conn_status", data.conn_status);
        } else {
            console.log(data)
            delete data['type']
            let tempMsg = { ...msg, ...data }
            //console.log("tempMsg", tempMsg);
            console.log("after mssg received and conncatenated::", tempMsg)
            setMsg(tempMsg)
        }
    };


    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };




    function fetchMsgs() {
        fetch('/api/fetchmessages', {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        }).then(response => response.json()).then((data) => {
            console.log(data)
            setUser_id(data[-1])
            delete data[-1]
            setMsg(data)
        })
    }

    function handleInputChange(e) {
        var val = e.target.value
        setInput(val)
    }

    function inputSearchClick(e) {
        console.log('clicked', e)
    }

    function handleSend() {
        console.log("clicked on send")
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: input
            })
        };
        fetch('/api/inputtext', requestOptions).then((response) => response.json()).
            then((data) => {
                console.log(data)
                if (data.msg_id != undefined) {
                    setMsg({ ...msg, ...data.msg_data })
                }
                setInput("")
                setScrolled(scrolled + 1)
                _send({ ...data.msg_data })
            })
    }

    function onkeyup(e) {
        if (e.keyCode === 13) {
            handleSend();
        }
    }

    return (
        <div className="chatbox-container">
            <div className="msgbox" id="scrollBottom">
                <MsgBox myid={user_id} msgs={msg} />
            </div>
            <div className="text-send">
                <input
                    className="input-msg"
                    type="text"
                    placeholder="message"
                    value={input}
                    onChange={handleInputChange}
                    onClick={inputSearchClick}
                    onKeyUp={onkeyup}
                />
                <IconButton style={{ "border": "4px solid black" }} onClick={handleSend}>
                    <IoIosSend />
                </IconButton>
            </div>
        </div>
    )
}
