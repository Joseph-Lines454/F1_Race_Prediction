import './App.css'
import ReactDOM from "react-dom/client"
import {useLocation} from "react-router-dom"

function F1_ShowRaceResults() {
  
  const location = useLocation()
  const {data} = location.state || []


  return (

    (data && data.length > 0) && (
    <div>
      <h1>This is the page for showing Race Dataa!!</h1>
      <table>
              <tbody>
              <tr>
                <th>Driver Name</th>
                <th>Driver Position</th>
                <th>Constructor</th>
                <th>Final Time</th>
                <th>Country</th>
              </tr>
              
                {Object.values(data).map((rows, index) => (
                  
                    <tr key = {index}>
                      
                      <th>{rows.DriverName}</th>
                      <th>{rows.FinishedPosition}</th>
                      <th>{rows.fullName}</th>
                      <th>{rows.Finaltime}</th>
                      <th>{rows.country}</th>
                      
                    </tr>
                
                ))}
              

                </tbody>
              </table>
    </div> )

 
  )
}

export default F1_ShowRaceResults
