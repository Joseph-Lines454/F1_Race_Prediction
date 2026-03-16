import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect, useState } from 'react';





let Response = undefined;


let Season = Array.from({length:  2026 + 1 - 1950}, (_,i) => i +  1950)

//Could maybe default to the 2026 season for simplicty






//We should return all of th seasons and display all of the races of that season

function Historical() {
  const [dataDisplay,dataDisplaySet] = useState(undefined)
  const [SeasonIn,SeasonSet] = useState(null)
  const navigation = useNavigate();
  const GetSeasonData =  () => {
    //This  is where we make a request to get  that seasons  data to  the client
    console.log(Number(SeasonIn))

    if(Season.includes(Number(SeasonIn)) == false)
    {
      alert("Invalid Season Selection!")
    }
    else{
      alert("We got it right!!!")
      GetHistoricalData()
    }

  }
  
  const GetHistoricalData = (season) => {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    
    if (this.readyState == 4 && this.status == 200)
    {
      console.log(this.responseText + "This is the response issue!")
      //Seasons = JSON.parse(this.responseText)
      dataDisplaySet((JSON.parse(this.responseText)).reverse())
    }
    }
  
    xhttp.open("POST","http://127.0.0.1:8001/Historical",true)
    xhttp.setRequestHeader('Content-Type', 'application/json')
    xhttp.send(JSON.stringify({year : Number(season)}));
  }
  const GetRaceResults = (data) => {
    
    console.log(data[0])
    console.log(data[1])
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    
    if (this.readyState == 4 && this.status == 200)
    {
      console.log(this.responseText)
      //Seasons = JSON.parse(this.responseText)
     navigation("/F1_ShowRaceResults", {state: {data : JSON.parse(this.responseText)}});
    }
    }
  
    xhttp.open("POST","http://127.0.0.1:8001/GetData",true)
    xhttp.setRequestHeader('Content-Type', 'application/json')
    xhttp.send(JSON.stringify({EventID : String(data[0]), RaceID : String(data[1])}));
  }

  const SetSeasonSel = (Season)  => {
    //SeasonSet(Number(Season))
    
    SeasonSet(Number(Season))
    console.log(Season)
    GetHistoricalData()
    //GetSeasonData()
  }

  const UpdateText = (e) => {
    //some validation here
    SeasonSet(Number(e.target.value))
   
    console.log(SeasonIn)
  }

  return (
    <div className='MainBody'>
      <div className = "FindSeason">
        <div className="dropdown">
          <button className="ButtonDis">Select Season</button>
          <div className="dropdownSeasons">

            {(Season).reverse().map((Season, index) => (
                  <label onClick={() => GetHistoricalData(Season)}>{Season}</label>
                ))}
                  
          </div>
        </div>
        <div className="SearchBar">
          <input  onChange={UpdateText} type = "text" className='Bar' placeholder='Search for Season' />
          <button onClick={() => GetHistoricalData(SeasonIn)} className='SearchButton'>Search</button>
        </div>
    </div>
    <div className='BodyCenter'>
       <table class='tableAlign'>
          <tbody>
            
              <tr>
                <th>Round</th>
                <th>Event</th>
                <th>Season</th>
              </tr>
              {dataDisplay != undefined && dataDisplay.map((data, index) => (
                      
                        <tr className='rows' key = {index} onClick={ () =>  GetRaceResults([data["Eventid"],data["Raceid"]])}>
                         
                            <td>{data["round"]}</td>
                            <td>{data["name"]}</td>
                            <td>{data["season"]}</td>
                         
                        </tr>
                        
                    ))}
             
            
            </tbody>
          </table>
         </div>
  </div>         
  )
}


export default Historical