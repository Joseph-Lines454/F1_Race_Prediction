import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect } from 'react';



let Response = undefined;

let ValidPrint = false;
let Teams = undefined;
let Drivers = undefined;
 var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200)
    {
      console.log(this.responseText)
      Response = this.responseText
      Response = JSON.parse(Response)
      Teams = Response[1]
      Drivers = Response[0]
     
      
      
      Drivers.sort(function(a,b){
        return b.points - a.points
      })
      console.log(Teams)
      ValidPrint = true;
    }
    


  }
  
  xhttp.open("GET","http://127.0.0.1:8001/F1_Statistics",true)
  xhttp.send();



const websocket = new WebSocket("ws://127.0.0.1:8001/ws")

websocket.addEventListener("open", event => {
  websocket.send("Connection established")
});

websocket.addEventListener("message", event=> {
  console.log("Message Recived From Server: ", event.data)
});



function F1_DriverStandings() {
  //websocket.send("HelloooooAhhhhh")
  return (
    (Drivers != undefined) && (
      <div>
        <h1>Driver Standings</h1>
        <table>
          <tbody>
          <tr>
            <th>Driver Name</th>
            <th>Driver Position</th>
            <th>Driver Points</th>
          </tr>
          
            {Drivers.map((Drivers, index) => (
              
                <tr key = {index}>
                  
                  <th>{Drivers.name}</th>
                  <th>{Drivers.position}</th>
                  <th>{Drivers.points}</th>
                  
                </tr>
            
            ))}
          

        </tbody>
        </table>

        <h1>Team Standings</h1>
        <table>
          <tbody>
          <tr>
            <th>Team Name</th>
            <th>Team Points</th>
            
          </tr>
          
            {Teams.map((Teams, index) => (
              
                <tr key = {index}>
                  
                  <th>{Teams.name}</th>
                  <th>{Teams.team_points}</th>
                
                  
                </tr>
            
            ))}
          

        </tbody>
        </table>
        
        
        
      </div>
    )
    
  
    )
 
}


export default F1_DriverStandings