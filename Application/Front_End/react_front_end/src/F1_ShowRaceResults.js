import './App.css'
import ReactDOM from "react-dom/client"
import {useLocation} from "react-router-dom"
import { CartesianGrid, Line, LineChart, BarChart, Bar, XAxis, YAxis, Legend,Tooltip  } from 'recharts';
import { RechartsDevtools} from '@recharts/devtools';
//Get drivers performance by points
//Add those drivers points - 2 bar charts


function F1_ShowRaceResults() {
  
  const location = useLocation()
  let {data} = location.state || []

  // I need to sort to remove first duplicate

  data = data.filter(item => !(item.FinishedPosition == 1 && item.Finaltime == "N/A"));
  // I need to make a constructors array which adds the drivers performances together
  let DriverBar = data

  /*Nested for loop to find all timestamps*/
  let points = 0;
  let TeamsArray = []
  for (let i = 0; i < data.length; i++) {
    points = points + data[i].points
    for (let j = 0; j < data.length; j++)
    {
      if (data[j].fullName == data[i].fullName && i != j)
      {
        points = points + data[j].points
      }
    }
    TeamsArray.push({teamname: data[i].fullName, points: points})
    points = 0
  }
  //This function filters out duplicats by comparing the name and points, not equal to index is ensuring we are not filting out the same index
  //We can now makae graphs with this data
  let barcharts = TeamsArray.filter((item, index,arr) => arr.findIndex(i => i.teamname == item.teamname && i.points == item.points) != index);
  for (let j = 0; j < barcharts.length; j++) { 
    console.log(barcharts[j])
  }

  for (let i = DriverBar.length - 1; i > 0; i--) { 
    
    // Generate random index 
    const j = Math.floor(Math.random() * (i + 1));
                  
    // Swap elements at indices i and j
    const temp = DriverBar[i];
    DriverBar[i] = DriverBar[j];
    DriverBar[j] = temp;
  }
  DriverBar.sort(function(a,b){
      return b.points - a.points
    })
  console.log(data.length)
  return (
    <>
    {data && data.length > 0 && (
    <div className='MainBody'>
      <h1 className='HistoricalData'>Race Data</h1>
        <table className='HistoricalData'>
                <tbody>
                <tr>
                  <th>Driver Name</th>
                  <th>Finishing Position</th>
                  <th>Points</th>
                  <th>Constructor</th>
                  <th>Final Time</th>
                  <th>Country</th>
                  
                </tr>
                
                {Object.values(data).sort().map((rows, index) => (
                  
                    <tr key = {index}>
                      
                      <td>{rows.DriverName}</td>
                      <td>{rows.FinishedPosition}</td>
                      <td>{rows.points}</td>
                      <td>{rows.fullName}</td>
                      <td>{rows.Finaltime}</td>
                      <td>{rows.country}</td>
                      
                    </tr>
                
                ))}
              

                </tbody>
              </table>
              <div className='AlignHistoricalCharts'>
                <div style = {{padding: '20px'}}>
                

                  <BarChart className='BarChartStyle' layout="vertical" style = {{width: '100%', aspectRatio: 1.618, minHeight: 800,maxWidth: 800}} responsive data={DriverBar} margin={{left: 150, bottom: 60, top: 60, right: 150}}>
                                    <text y = {30} x = {400} dominantBaseline="central">Driver Points</text>
                                    <YAxis type="category" dataKey="DriverName" interval={0} angle={-0}  tick={({ x, y, payload }) => (
                          <text x={x} y={y} textAnchor="end" dominantBaseline="middle">
                            {payload.value}
                          </text>
                        )} label = {{value: "Driver Name", position: "left", offset: 100, angle: -90}} />
                                    <XAxis dataKey="points" type="number" angle={-0} label = {{value: "Points", position: "bottom", offset: 20}} />
                                    
                                    <Bar dataKey = "points" fill="#8884d8" />
                                    
                                    <RechartsDevtools />
                                  </BarChart>

                </div>
                <div style = {{padding: '20px'}}>
                 
                
                  <BarChart className='BarChartStyle' layout="vertical" style = {{width: '100%', aspectRatio: 1.618, minHeight: 800,maxWidth: 800}} responsive data={barcharts} margin={{left: 220, bottom: 60, top: 60, right: 150}}>
                                    <text y = {30} x = {400} dominantBaseline="central">Team Points</text>
                                    <YAxis type="category" dataKey="teamname" interval={0} angle={-0}  tick={({ x, y, payload }) => (
                          <text x={x} y={y} textAnchor="end" dominantBaseline="middle">
                            {payload.value}
                          </text>
                        )} label = {{value: "Team Name", position: "left", offset: 200, angle: -90}} />
                                    <XAxis dataKey="points" type="number" angle={-0} label = {{value: "Points", position: "bottom", offset: 20}} />
                                    
                                    <Bar dataKey = "points" fill="#8884d8" />
                                    
                                    <RechartsDevtools />
                                  </BarChart>

                
                </div>
            </div> 
          </div>
  
  )}

    {data && data.length == 0 && (
    <div className='NoData'>
      <h1>Race is not currently available</h1>
      
              

            

    </div> )}

  </>
  )
}

export default F1_ShowRaceResults
