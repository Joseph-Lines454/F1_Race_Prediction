import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect, useState } from 'react';
import { CartesianGrid, Line, LineChart, BarChart, Bar, XAxis, YAxis, Legend,Tooltip, Cell } from 'recharts';
import { RechartsDevtools} from '@recharts/devtools';
//This function gets the year that the usser selected, then we query the API for that year and return a new result 
let Seasons = null;
let DriverColours = ["#FF5733","#33FF57","#3357FF","#FF33A1","#33fff5","#F5FF33","#FF8C33","#"]

//Might need to use useeffect here...
let Response = undefined;

let ValidPrint = false;
let Teams = undefined;
let Drivers = undefined;
let Drivers_Over_Season = undefined;
let Teams_Over_Season = undefined;
var xhttp = new XMLHttpRequest();

let TeamColours = {"mercedes": "#b2bfb2","ferrari" : "darkred","mclaren" : "orange","haas": "lightgray", "red bull racing": "lightblue","racing bulls" :"darkyellow","alpine": "lightpink","Audi": "silver","Williams": "dark blue","Cadillac" : "black", "aston martin": "darkgreen"}
//Driver Colours here

function AssignColoursGraph () {
  //Assign Colours By Team
}

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
    <div className = "BkrdWrapper">
      <div className='MainBody'>
        <h1>Driver Standings</h1>
        <div className='AlignItems'>
          
          <div className='DriversStandings'>
            
            <table>
              
                <thead>
                  <tr>
                    <th>Driver Name</th>
                    <th>Driver Position</th>
                    <th>Driver Points</th>
                  </tr>
                </thead>
                <tbody>
                {Drivers.map((Drivers, index) => (
                  
                    <tr key = {index}>
                      
                      <td>{Drivers.name}</td>
                      <td>{Drivers.position}</td>
                      <td>{Drivers.points}</td>
                      
                    </tr>
                
                ))}
              

                </tbody>
              </table>
          </div>
          <div className='AlignCharts'>
            <div>
                
                {/*Is there any way to get colours in there, also want it to be aligned with drivers standings*/}
                <BarChart layout="vertical" style = {{width: '100%', aspectRatio: 1.618, minHeight: 800,maxWidth: 800}} responsive data={Drivers} margin={{left: 150}}>
                  <YAxis type="category" dataKey="name" interval={0} angle={-0}  tick={({ x, y, payload }) => (
        <text x={x} y={y} textAnchor="end" dominantBaseline="middle">
          {payload.value}
        </text>
      )} />
                  <XAxis dataKey="points" type="number" angle={-0} />
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
                    top: 20,
                    right: 40,
                    left: 20,
                    bottom: 20,
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
        </div>
          
        <div>
          <h1>Team Standings</h1>
          <div className='AlignItems'>
          <div className='DriversStandings'>
        
            
            <table>
              <thead>
              <tr>
                <th>Team Name</th>
                <th>Team Points</th>
                
              </tr>
              </thead>
                  <tbody>
                {Teams != undefined && Teams.map((Teams, index) => (
                  
                    <tr key = {index}>
                      
                      <td>{Teams.name}</td>
                      <td>{Teams.points}</td>
                    
                      
                    </tr>
                
                ))}
              
              </tbody>
            </table>
          </div>
          <div className='AlignCharts'>
            <div>
              <BarChart style = {{width: '100%', aspectRatio: 1.618, maxWidth: 600}} responsive data={Teams} margin={{bottom: 80,left: 80}}>
                <XAxis dataKey="name" interval={0} angle={-45} textAnchor="end" />
                <YAxis dataKey="points" label = {{value: "Points Total", position: "left", offset: 10, angle: -90}} />
                <Bar dataKey = "points" >
                 {Teams.map(driver => (
                    <Cell key = {driver.name} fill={TeamColours[driver.name]} />
                  ))}
                  </Bar>
                <RechartsDevtools />
              </BarChart>
            </div>
            <div>
              <LineChart
                  style={{ width: '100%', height: '100%', aspectRatio: 1.618 }}
                  responsive
                  data={Teams_Over_Season}
                  margin={{
                    top: 20,
                    right: 40,
                    left: 20,
                    bottom: 20,
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
                      stroke = {TeamColours[driver]}
                    />
                  ))}
                  
                <RechartsDevtools />
              </LineChart>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>
      
    )
    
  
    )
 
}


export default F1_DriverStandings