import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect, useState } from 'react';
import { CartesianGrid, Line, LineChart, BarChart, Bar, XAxis, YAxis, Legend,Tooltip  } from 'recharts';
import { RechartsDevtools} from '@recharts/devtools';
//This function gets the year that the usser selected, then we query the API for that year and return a new result 
let Seasons = null;


//Might need to use useeffect here...
let Response = undefined;

let ValidPrint = false;
let Teams = undefined;
let Drivers = undefined;
let Drivers_Over_Season = undefined;
let Teams_Over_Season = undefined;
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {

  if (this.readyState == 4 && this.status == 200)
  {
   
    Response = this.responseText
    Response = JSON.parse(Response)
    Drivers = Response[0]
    Teams = Response[1]
     
    Drivers.sort(function(a,b){
      return b.points - a.points
    })
   
    ValidPrint = true;

  }
    
    


}
  
xhttp.open("GET","http://127.0.0.1:8001/F1_Statistics",true)
xhttp.send();

var GetSeasonData = new XMLHttpRequest();
GetSeasonData.onreadystatechange = function()
{
  if (this.readyState == 4 && this.status == 200)
  {
    
    Response = JSON.parse(this.responseText)
    Drivers_Over_Season = Response[0]
    Teams_Over_Season = Response[1]
    console.log(Teams_Over_Season)
    //We need to change the shape of the data, so we need to concatinate it all together
    Drivers_Over_Season = SortDataForGraph(Drivers_Over_Season)
    Teams_Over_Season = SortDataForGraph(Teams_Over_Season)
    
  }
}
GetSeasonData.open("GET","http://127.0.0.1:8001/F1_Standings_Over_Time",true)
GetSeasonData.send();

function SortDataForGraph(Data)
{
  let newRows = {}
  
  //we need to sort the data so its in individual rows for each date
  //Get all of the dates then just add all values that match that date
  Data.forEach(({timestamp}) => {
    if (!newRows[timestamp])
    {
      newRows[timestamp] = {timestamp}
     
    }
  });
  
  newRows = Object.values(newRows)
  let DataLen = newRows.length
  console.log(newRows.length)

  /*Nested for loop to find all timestamps*/
  for (let i = 0; i < DataLen; i++) {
    for (let j = 0; j < Data.length; j++)
    {
      if (Data[j]["timestamp"] == newRows[i]["timestamp"])
      {
        newRows[i][Data[j].name] = Number(Data[j].points)
      }
    }
  }
 
  return newRows
}

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

let driverNames = undefined
function F1_DriverStandings() {
  //websocket.send("HelloooooAhhhhh")
  if (Response != undefined)
  {
    driverNames = Object.keys(Drivers_Over_Season[0]).filter(k => k !== "timestamp");
  }
  
  return (
    ((Drivers != undefined) && (Response != undefined) && (driverNames != undefined)) && (
      <div>
        <div>
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
            </div>
            <div>
              
               {/*Is there any way to get colours in there, also want it to be aligned with drivers standings*/}
              <BarChart style = {{width: '100%', aspectRatio: 1.618, maxWidth: 600}} responsive data={Drivers}>
                <XAxis dataKey="name" interval={0} angle={-45} textAnchor="end" />
             
                <Bar dataKey = "points" fill="#8884d8" />
              
                <RechartsDevtools />
              </BarChart>
            </div>
            <div>
              <LineChart
                style={{ width: '100%', height: '100%', aspectRatio: 1.618 }}
                responsive
                data={Drivers_Over_Season}
                margin={{
                  top: 5,
                  right: 0,
                  left: 0,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-3)" />
                
                <XAxis dataKey="timestamp" angle={-45}/>
              
                <Tooltip />
                 
                {Object.keys(Drivers_Over_Season[0]).filter(k => k != "timestamp" ).map(driver => (
                  <Line
                    key={driver}
                    type="monotone"
                    dataKey={driver}
                    
                  />
                ))}
                
              <RechartsDevtools />
            </LineChart>
            </div>
            
          </div>
          
        <div>
          <div>
        
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
                      <th>{Teams.points}</th>
                    
                      
                    </tr>
                
                ))}
              
              </tbody>
            </table>
          </div>
          <div>
             <BarChart style = {{width: '100%', aspectRatio: 1.618, maxWidth: 600}} responsive data={Teams}>
              <XAxis dataKey="name" interval={0} angle={-45} textAnchor="end" />
             
              <Bar dataKey = "points" fill="#8884d8" />
              
              <RechartsDevtools />
            </BarChart>
          </div>
          <div>
            <LineChart
                style={{ width: '100%', height: '100%', aspectRatio: 1.618 }}
                responsive
                data={Teams_Over_Season}
                margin={{
                  top: 5,
                  right: 0,
                  left: 0,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-3)" />
                
                <XAxis dataKey="timestamp" angle={-45}/>
              
                <Tooltip />
                 
                {Object.keys(Teams_Over_Season[0]).filter(k => k != "timestamp" ).map(driver => (
                  <Line
                    key={driver}
                    type="monotone"
                    dataKey={driver}
                    
                  />
                ))}
                
              <RechartsDevtools />
            </LineChart>
          </div>
        </div>
      
      </div>
      
    )
    
  
    )
 
}


export default F1_DriverStandings