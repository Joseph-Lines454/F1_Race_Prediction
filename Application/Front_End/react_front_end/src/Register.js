
import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import {BrowserRouter, Routes, Route, Link,useNavigate} from 'react-router-dom'
import {CheckReg} from './Login_and_Register_functions.js';



function RegisterUser() {
  const navigate = useNavigate();
  const[usernameInital, username] = useState("Name here");
  const[passwordInital, password] = useState("Password here");
  const[emailInital, email] = useState("Name here");
  const[phonenumberInital, phonenumber] = useState("Password here");
  let emailChange  = (e) => email(e.target.value);
  let usernameChange  = (e) => username(e.target.value);
  let passwordChange  = (e) => password(e.target.value);
  let phonenumberChange  = (e) => phonenumber(e.target.value);
  const Register = () => {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      console.log(this.status)
      if (this.readyState == 4 && this.status == 200)
      {
        console.log(this.responseText + "This is the response issue!")
        //Seasons = JSON.parse(this.responseText)
        navigate("/");
      }
    }
  
    xhttp.open("POST","http://127.0.0.1:8001/Register",true)
    xhttp.setRequestHeader('Content-Type', 'application/json')
    xhttp.send(JSON.stringify({"username": usernameInital, "password": passwordInital, "email": emailInital}));
  }
  
  return (
    <div className='MainBody'>
      <div className="FormAlign">
        
          
          <form className='textForm'>
            <h1>Registration</h1>
            <label>Email:</label>
            <br />
            <input type='text' value={emailInital} onChange={emailChange}></input>
            <br />
            <label>Username:</label>
            <br />
            <input type='text' value={usernameInital} onChange={usernameChange}></input>
            <br />
            <label>Password:</label>
            <br />
            <input type='text' value={passwordInital} onChange={passwordChange}></input>
            <br />
            <label>Phone Number:</label>
            <br />
            <input type='text' value={phonenumberInital} onChange={phonenumberChange}></input>
            <br />
            <br />
            <button type = "button" id = "buttonstyle" onClick = {() => Register(usernameInital,passwordInital,navigate)}>Register</button>
            <br />
            <br />
            <button id = "buttonstyle">
              <Link to="/LoginUser" class = "LinkStyle">Login Instead?</Link>
            </button>
            
          </form>
          
          
      </div>
    </div>
  );
}

export default RegisterUser;
