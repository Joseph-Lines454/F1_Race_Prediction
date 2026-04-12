import './App.css'
import ReactDOM from "react-dom/client"
import {useLocation} from "react-router-dom"
import { CartesianGrid, Line, LineChart, BarChart, Bar, XAxis, YAxis, Legend,Tooltip  } from 'recharts';
import { RechartsDevtools} from '@recharts/devtools';
import {barcharts, SortData} from './UnitTestFunc.mjs'
//Get drivers performance by points
//Add those drivers points - 2 bar charts


function F1_ShowRaceResults() {
  
  const location = useLocation()
  let {data} = location.state || []
  let DriverBar = SortData(data)
  
  // I need to sort to remove first duplicate

  
  return (
    <>
    {data && data.length > 0 && data != null && (
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
