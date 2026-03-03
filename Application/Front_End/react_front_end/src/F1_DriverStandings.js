import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect, useState } from 'react';

//This function gets the year that the usser selected, then we query the API for that year and return a new result 
let Seasons = null;


//Might need to use useeffect here...
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
       Drivers = Response[0]
      Teams = Response[1]
     
      
      
      Drivers.sort(function(a,b){
        return b.points - a.points
      })
      console.log(Drivers)
      ValidPrint = true;

     
    }
    
    


  }
  
  xhttp.open("GET","http://127.0.0.1:8001/F1_Statistics",true)
  xhttp.send();




//const websocket = new WebSocket("ws://127.0.0.1:8001/ws")

//websocket.addEventListener("open", event => {
//  websocket.send("Connection established")
//});

//websocket.addEventListener("message", event=> {
//  console.log("Message Recived From Server: ", event.data)
//});


//We can have a historical Data section
//2026 infromation
//Live timings

//We can make charts showing the changes in the championship



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
          
            {Teams != undefined && Teams.map((Teams, index) => (
              
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