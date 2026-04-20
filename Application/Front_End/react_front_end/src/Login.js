
import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';

import {BrowserRouter, Routes, Route, Link, useNavigate} from 'react-router-dom'





function LoginUser() {
  const navigation = useNavigate();
  console.log(location.pathname)
  
  
   const Login = () => {
     var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    
    if (this.readyState == 4 && this.status == 200)
    {
      console.log(this.responseText + "This is the response issue!")
      //Seasons = JSON.parse(this.responseText)
       navigation("/F1_Prediction");
    }
    else if(this.readyState == 4 && this.status == 401)
    {
      alert(this.responseText)
    }
    }
  
    xhttp.open("POST","http://localhost:8001/Login",true)
    xhttp.withCredentials = true;
    xhttp.setRequestHeader('Content-Type', 'application/json')
    xhttp.send(JSON.stringify({"username": usernameInital, "password": passwordInital}));
  }
  
  
  const[usernameInital, username] = useState("Name here");
  const[passwordInital, password] = useState("Password here");
  let usernameChange  = (e) => username(e.target.value);
  let passwordChange  = (e) => password(e.target.value);
  /*
  async function CheckIfLoginValid(usernameInital,passwordInital){
     //socket.emit("CheckLogin", [{username: usernameInital, password: //passwordInital}])
    
    const res = await fetch("http://localhost:82/CheckLogin", {
      method: 'POST',
      credentials: 'include',
      withCredentials: true,
      headers: {
        'Content-Type': "application/json",
        'Access-Control-Allow-Credentials': 'true'
      },
      body: JSON.stringify([{username: usernameInital, password: passwordInital}])
      
    });
    
    if (res.status == 200)
    {
      navigate("/LibaryHomePage");
    }
    else if (res.status == 401)
    {
      alert("Invalid Credentials!");
    }
    else if(this.status != 401 && this.status != 200){
      alert("something else went wrong")
    }

    return res.status;
  };
  
  */
  
  
     
     
  
  return (
    
    <div className='MainBody'>
    
      <div className="FormAlign">
        
        
          <form className='textForm'>
            <h1>Login</h1>
            <label>Username:</label>
            <br />
            <input type='text' value={usernameInital} onChange={usernameChange}></input>
            <br />
            <label>Password:</label>
            <br />
            <input type='password' value={passwordInital} onChange={passwordChange}></input>
            <br />
            <br />
            <button style = {{backgroundColor: "#56a595", color: "white", border: "none"}} type = "button" id = "buttonstyle" onClick = {() => Login(usernameInital,passwordInital)}>Login</button>
            <br />
            <br />
            <button id = "buttonstyle" style = {{backgroundColor: "#009879", color: "white", border: "none"}}>
              <Link to="/RegisterUser" className = "LinkStyle" style = {{color: "white"}}  >Register Instead?</Link>
            </button>
            
          </form>
          
      </div>
    </div>
  );
}

export default LoginUser;

