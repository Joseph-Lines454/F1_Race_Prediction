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
  websocket.onmessage = (event) => {Object.values(assigndata(event.data))}
  
 
   return (
    
    (data != undefined) && (
        <div>
          <h1>Live F1 Telematry Test - Qualifying</h1>
         {data[1].map((data, index) => (
                  
                    <tr key = {index}>
                      
                      <th>{data.lap_duration}</th>
                      
                      
                    </tr>
                
                ))}
        
            
      </div>
    
      
    )
    
  
    )
}

export default F1_Live_Timings
