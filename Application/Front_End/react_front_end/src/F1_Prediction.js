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
  GetSeasonData.open("GET","http://127.0.0.1:2000/MLModelPerformance",true)
  GetSeasonData.send();


  
  return (

    
    <div>
      <h1>F1 Race Prediction</h1>
    </div>

 
  )
}

export default F1_Prediction
