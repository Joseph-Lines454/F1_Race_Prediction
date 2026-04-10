import { useState } from 'react';
import './App.css'
import ReactDOM from "react-dom/client"


function F1_Prediction() {
  const [dataRecived,dataSet] = useState(null)
  var GetSeasonData = new XMLHttpRequest();
  GetSeasonData.withCredentials = true;
  GetSeasonData.onreadystatechange = function()
  {
    if (this.readyState == 4 && this.status == 200)
    {
      console.log(this.responseText)
      
    }
  }
  var GetMLData = new XMLHttpRequest();
  GetMLData.onreadystatechange = function()
  {
    if (this.readyState == 4 && this.status == 200)
    {
      console.log(this.responseText)
      dataSet(JSON.parse(this.responseText))
      
    }
  }

  //GetSeasonData.open("GET","http://127.0.0.1:2000/MLModelPerformance",true)
  //GetSeasonData.send();

  //Test ML Models, Get Data From China and send that Data to the ML Models
  const TestMLModels = () => {
    GetMLData.open("GET","http://127.0.0.1:8001/TestMLModels",true)
    GetMLData.send();
  }
  
  return (
    <div>
      <h1>F1 Race Prediction - JapaneseGP</h1>
      <div className='MainBody'>
      
        <div className="dropdown">
          <button onClick={() => TestMLModels()} style={{margin: '20px'}} className="ButtonDis">Test ML Models</button>
          
          
        </div>
        
        <>
        {dataRecived && dataRecived.length > 0 && (
          <div>
            <div className='title'>
              <p>The prediction is seperated into 4 classes top 3, 3 - 10, 10 - 15 and 15 - 22</p>
            </div>
            <div className='DriversStandings'>

              <table>
                
                  <thead>
                    <tr>
                      <th>Driver Name</th>
                      <th>Driver Position</th>
                    
                    </tr>
                  </thead>
                  <tbody>
                  {dataRecived.map((driver, index) => (
          
                      <tr key = {index}>
                        <td>{driver.DriverName}</td>
                        <td>{(driver.DriverPosition) + 1}</td>        
                      </tr>

                  ))}
                

                  </tbody>
                </table>
            </div>
          </div>

 
        )
        }
  
        </>
    </div>
    </div>

     
    
  )
}

export default F1_Prediction
