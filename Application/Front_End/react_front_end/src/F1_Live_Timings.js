import { useState, useEffect } from 'react'
import './App.css'
import ReactDOM from "react-dom/client"

var xhttp = new XMLHttpRequest();
 
//xhttp.open("GET","http://127.0.0.1:8001/testaba",true)
//xhttp.send();
function F1_Live_Timings() {
  const [data, assigndata] = useState(undefined)

  const websocket = new WebSocket("ws://127.0.0.1:8001/ws")
  websocket.onopen = () => console.log("Connected!!")
  websocket.onmessage = (event) => {console.log(event.data)}
  /*Object.values(assigndata(event.data))*/
 
   return (
    <div className='MainBody'>
      <h1>We are using console.log for now</h1>
    </div>
    
    
  
    )
}

export default F1_Live_Timings
