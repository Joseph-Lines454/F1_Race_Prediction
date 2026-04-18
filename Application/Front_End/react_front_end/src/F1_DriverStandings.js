import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect, useState } from 'react';
import { CartesianGrid, Line, LineChart, BarChart, Bar, XAxis, YAxis, Legend,Tooltip, Cell, ResponsiveContainer } from 'recharts';
import {AssignDriverColours, DriverColoursGraph, SortDataForGraph} from './UnitTestFunc.mjs'
import { RechartsDevtools} from '@recharts/devtools';

//This function gets the year that the usser selected, then we query the API for that year and return a new result 
let Seasons = null;
let DriverColours = ["#FF5733","#33FF57","#3357FF","#FF33A1","#33fff5","#F5FF33","#FF8C33","#"]

//Might need to use useeffect here...
let Response = null;

let ValidPrint = false;
let Teams = undefined;
let Drivers = undefined;
let Drivers_Over_Season = undefined;
let Teams_Over_Season = undefined;


let TeamColours = {"mercedes": "#b2bfb2","ferrari" : "darkred","mclaren" : "orange","haas": "lightgray", "red bull racing": "lightblue","racing bulls" :"darkyellow","alpine": "lightpink","Audi": "silver","Williams": "dark blue","Cadillac" : "black", "aston martin": "darkgreen"}
//Driver Colours here









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

//We need to assign random colours to the drivers in the graphs


let driverNames = undefined
function F1_DriverStandings() {


  useEffect(() => {
  var xhttp = new XMLHttpRequest();
  var GetSeasonData = new XMLHttpRequest();
  GetSeasonData.withCredentials = true;
  xhttp.withCredentials = true;
  xhttp.onreadystatechange = function() {

  if (this.readyState == 4 && this.status == 200 && this.responseText != null)
  {
    Response = this.responseText
    Response = JSON.parse(Response)
    Drivers = Response[0]
    Teams = Response[1]
      
    Drivers.sort(function(a,b){
      return b.points - a.points
    })
    Drivers = AssignDriverColours(Object.keys(Drivers).length, Drivers)
    console.log("Drivers Colour: " + Drivers[0].colour)
    ValidPrint = true;
  }
  else{
    Response = null;
  }
    


}


xhttp.open("GET","http://localhost:8001/F1_Statistics",true)

xhttp.send();

GetSeasonData.onreadystatechange = function()
{
  if (this.readyState == 4 && this.status == 200)
  {
    
    Response = JSON.parse(this.responseText)
    Drivers_Over_Season = Response[0]
    Teams_Over_Season = Response[1]
    console.log(Teams_Over_Season)
    console.log(Drivers_Over_Season)
    //We need to change the shape of the data, so we need to concatinate it all together
    Drivers_Over_Season = SortDataForGraph(Drivers_Over_Season)
    Teams_Over_Season = SortDataForGraph(Teams_Over_Season)
  }
  else{
    Response = null;
  }
}
GetSeasonData.open("GET","http://localhost:8001/F1_Standings_Over_Time",true)
GetSeasonData.send();



  //end
}, []);





  //websocket.send("HelloooooAhhhhh")
  if (Response != null)
  {
    driverNames = Object.keys(Drivers_Over_Season[0]).filter(k => k !== "timestamp");
  }
  
  return (
    ((Drivers != null) && (Response != null) && (driverNames != undefined)) && (
    <div className = "BkrdWrapper">
      <div className='MainBody'>
        <div className='PredCenter'>
          <h1>Driver Standings</h1>
        </div>
        
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
            <div style={{width: "100%", height: "100%"}}>
                <ResponsiveContainer width="100%" aspect={1.618}>
                  {/*Is there any way to get colours in there, also want it to be aligned with drivers standings*/}
                  <BarChart className='BarChartStyle' layout="vertical" responsive data={Drivers} margin={{left: 150, bottom: 60, top: 60, right: 150}}>
                    <text y = {30} x = "50%" textAnchor='middle' dominantBaseline="middle">Driver Points</text>
                    <YAxis type="category" dataKey="name" interval={0} angle={-0}  tick={({ x, y, payload }) => (
                    <text x={x} y={y} textAnchor="end" dominantBaseline="middle">
                      {payload.value}
                    </text>
                    )} 
                    label = {{value: "Driver Name", position: "left", offset: 100, angle: -90}} />
                    <XAxis dataKey="points" type="number" angle={-0} label = {{value: "Points", position: "bottom", offset: 20}} />
                    
                    <Bar dataKey = "points">
                      <Tooltip trigger="item" />
                    {Object.values(Drivers).map((value,index) => (
                      <Cell key = {index} fill = {value.colour} />
                    ))}
                    </Bar>
                    
                    <RechartsDevtools />
                  </BarChart>
                </ResponsiveContainer>
            </div>
            <div style={{width: "100%", height: "100%"}}>
                <ResponsiveContainer width="100%" aspect={1.618}>
                  <LineChart className='BarChartStyle'
                    
                    responsive
                    data={Drivers_Over_Season}
                    margin={{
                      top: 40,
                      right: 40,
                      left: 40,
                      bottom: 40,
                    }}
                  >
                    <text y = {30} x = "50%" textAnchor='middle' dominantBaseline="middle">Drivers Points Progression over season</text>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-3)" />
                    <Legend verticalAlign= "bottom" align="left"  layout = "horizontal" wrapperStyle = {{height: '120px',fontSize: '12px',width: '2500px',  display: 'flex', alignItems: 'center', paddingTop: '40px'}} />
                    <XAxis dataKey="timestamp" label = {{value: "Date", position: "bottom", offset: 20}} angle={0}/>
                    <YAxis label = {{value: "Drivers", position: "left", offset: 20, angle: -90}} />
                    <Tooltip />
                    
                    {Object.keys(Drivers_Over_Season[0]).filter(k => k != "timestamp" ).map(driver => (
                      <Line
                        key={driver}
                        type="monotone"
                        dataKey={driver}
                        stroke = {DriverColoursGraph[driver]}
                      />
                    ))}
                    
                  <RechartsDevtools />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
          
        <div>
          <div className='PredCenter'>
            <h1>Team Standings</h1>
          </div>
          
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
            <div style={{width: "100%", height: "100%"}}>
              <ResponsiveContainer width="100%" aspect={1.618}>
              <BarChart className='BarChartStyle' responsive data={Teams} margin={{bottom: 120,left: 80, top: 120, right: 80}}>
                 <text y = {30} x = "50%" textAnchor='middle' dominantBaseline="middle">Teams Points</text>
                <XAxis dataKey="name" interval={0} angle={-45} textAnchor="end" label = {{value: "Teams", position: "bottom", offset: 80}} />
                <YAxis dataKey="points" label = {{value: "Points Total", position: "left", offset: 30, angle: -90}} />
                <Tooltip trigger="item" />
                <Bar dataKey = "points" >
                 {Teams.map(driver => (
                    <Cell key = {driver.name} fill={TeamColours[driver.name]} />
                  ))}
                  </Bar>
                <RechartsDevtools />
              </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{width: "100%", height: "100%"}}>
                <ResponsiveContainer width="100%" aspect={1.618}>
                <LineChart className='BarChartStyle'
                    
                    responsive
                    data={Teams_Over_Season}
                    margin={{
                      top: 80,
                      right: 40,
                      left: 40,
                      bottom: 40,
                    }}
                  >
                    <text y = {30} x = "50%" textAnchor='middle' dominantBaseline="middle">Teams Points Progression over season</text>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-3)" />
                    
                    <XAxis label = {{value: "Date", position: "bottom", offset: 0, angle: 0}} dataKey="timestamp" angle={0}/>
                    <YAxis label = {{value: "Points", position: "left", offset: 0, angle: -90}}/>
                    <Legend  verticalAlign= "bottom" align="left"  layout = "horizontal" wrapperStyle = {{height: '120px',fontSize: '12px',width: '2000px',  display: 'flex', alignItems: 'center', paddingTop: '40px'}}/>
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
              </ResponsiveContainer>
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