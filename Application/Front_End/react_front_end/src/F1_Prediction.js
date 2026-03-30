import './App.css'
import ReactDOM from "react-dom/client"


function F1_Prediction() {
  

  var GetSeasonData = new XMLHttpRequest();
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
      <h1>F1 Race Prediction</h1>
      <div className='MainBody'>
      
        <div className="dropdown">
          <button onClick={() => TestMLModels()} style={{margin: '20px'}} className="ButtonDis">Test ML Models</button>
         
        </div>
        
    </div>
    </div>

 
  )
}

export default F1_Prediction
