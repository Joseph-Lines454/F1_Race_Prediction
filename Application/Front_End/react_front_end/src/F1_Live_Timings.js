import { useState, useEffect } from 'react'
import './App.css'
import ReactDOM from "react-dom/client"

var xhttp = new XMLHttpRequest();
 
//xhttp.open("GET","http://127.0.0.1:8001/testaba",true)
//xhttp.send();
function F1_Live_Timings() {
  const [data, assigndata] = useState(undefined)


  const websocket = new WebSocket("ws://127.0.0.1:8001/ws")
  websocket.onopen = () => console.log("Connected???!!")
  websocket.onmessage = (event) => {console.log(event.data)
    let message = JSON.parse(event.data)
    
    //if the driver has already posted a laptime, replace this laptime.
    if (message.data.lap_duration != null)
    {
      assigndata(data + message.data)
      //we need to check
    }

  }
  /*Object.values(assigndata(event.data))*/
 

  //we need to make a function that checks weather that lap time is currently within th

   return (
     (data != undefined) && (
      <div className='MainBody'>
        <h1>We are using console.log for now</h1>
        <p> {data.driver_number} + {data.lap_duration}</p>        
        

      </div>
      


      )
   
    
    
  
    )
}

export default F1_Live_Timings
