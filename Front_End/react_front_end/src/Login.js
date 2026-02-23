import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import {CheckIfLoginValid, CheckCookies} from './Login_and_Register_functions'
import {BrowserRouter, Routes, Route, Link, useNavigate} from 'react-router-dom'





function LoginUser() {
  const navigate = useNavigate();
  console.log(location.pathname)
  
  useEffect(() => {
    //CheckCookies();
    //navigate("/LibaryHomePage");
  }, []);
  
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
    
    <div>
    
    <div className="FormAlign">
      
      
        <form className='textForm'>
          <h1>Login</h1>
          <label>Username:</label>
          <br />
          <input type='text' value={usernameInital} onChange={usernameChange}></input>
           <br />
          <label>Password:</label>
           <br />
          <input type='text' value={passwordInital} onChange={passwordChange}></input>
           <br />
           <br />
          <button type = "button" id = "buttonstyle" onClick = {() => CheckIfLoginValid(usernameInital,passwordInital,navigate)}>Login</button>
          <br />
          <br />
          <button id = "buttonstyle">
            <Link to="/Register" class = "LinkStyle" >Register Instead?</Link>
          </button>
          
        </form>
        
    </div>
    </div>
  );
}

export default LoginUser;

