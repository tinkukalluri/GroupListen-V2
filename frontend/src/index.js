// import { render } from "react-dom";
import { render } from "react-dom";
import App from "./components/App";

import React from 'react';
import ReactDOM from 'react-dom';
import { Component } from "react";


// export default class Index extends Component {
//     constructor(props) {
//         super(props);
//         this.state = { "tinku": "tinku" }
//     }
//     render() {
//         setTimeout(() => {
//             this.setState({ "sindhu": "sindhu" })
//         }, 3000);
//         return (
//             <div>
//                 lets goo
//                 {this.state.tinku}
//                 {this.state.sindhu}
//             </div>
//         );
//     }
// }


const appDiv = document.getElementById("app");
ReactDOM.render(<App />, appDiv);