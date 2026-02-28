import { useNavigate } from 'react-router-dom'
import './App.css'
import { useEffect, useState } from 'react';






let Response = undefined;


let Season = Array.from({length:  2026 + 1 - 1950}, (_,i) => i +  1950)

//Could maybe default to the 2026 season for simplicty
 var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    
    if (this.readyState == 4 && this.status == 200)
    {
      //console.log(this.responseText)
      //Seasons = JSON.parse(this.responseText)
      
      console.log("Season" + Season)
    }
    else{
     
    }
   


  }
  
  xhttp.open("GET","http://127.0.0.1:8001/Historical",true)
  xhttp.send();

/*
const websocket = new WebSocket("ws://127.0.0.1:8001/ws")

websocket.addEventListener("open", event => {
  websocket.send("Connection established")
});

websocket.addEventListener("message", event=> {
  console.log("Message Recived From Server: ", event.data)
});
*/


//We should return all of th seasons and display all of the races of that season

function Historical() {
  const [SeasonIn,SeasonSet] = useState(null)
  const GetSeasonData =  () => {
    //This  is where we make a request to get  that seasons  data to  the client
    console.log(Number(SeasonIn))

    if(Season.includes(Number(SeasonIn)) == false)
    {
      
      alert("Invalid Season Selection!")
    }
    else{
      alert("We got it right!!!")
    }

  }

  
  const SetSeasonSel = (Season)  => {
    //SeasonSet(Number(Season))
     SeasonSet(Number(Season))
      console.log(SeasonIn)
    //GetSeasonData()
  }

  const UpdateText = (e) => {
    //some validation here
    SeasonSet(Number(e.target.value))
   
    console.log(SeasonIn)
  }

  return (
    <div class = "FindSeason">
      <div class="dropdown">
        <button class="ButtonDis">Select Season</button>
        <div class="dropdownSeasons">

          {Season.map((Season, index) => (
                <label onClick={() => SetSeasonSel(Season)}>{Season}</label>
              ))}
                
        </div>
      </div>
      <div class="SearchBar">
        <input  onChange={UpdateText} type = "text" className='Bar' placeholder='Search for Season' />
        <button onClick={GetSeasonData} className='SearchButton'>Search</button>
      </div>
  </div>

  )
}


export default Historical