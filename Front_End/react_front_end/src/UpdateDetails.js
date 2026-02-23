import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import {BrowserRouter, Routes, Route, Link, useNavigate} from 'react-router-dom'


//Send some JSON here

const paramsSend = {
  withCredentials: true,
}


//some function to send this data

function UpdateDetails() {
  const[passwordConfirm_First, passwordFirst] = useState("");
  const[newPassword, newpassword] = useState("");
  const navigate = useNavigate();
  let PasswordFirstFunc  = (e) => passwordFirst(e.target.value);
  let newPasswordFunc  = (e) => newpassword(e.target.value);
  //change password

  
    
  async function PasswordChange()
  {
    //Post some code
      const res = await fetch("http://localhost:82/PasswordChange", {
        method: 'POST',
        credentials: 'include',
        withCredentials: true,
        headers: {
        'Content-Type': "application/json",
        'Access-Control-Allow-Credentials': 'true'
      },
      body: JSON.stringify([{password: passwordConfirm_First, NewPassword: newPassword}])
     
    });

    if(res.status == 200)
    {
      alert("Password has been changed successfully");
    }
    else{
      alert("Password has not been changed. Check origonal password");
    }

  }

  return (
    
    <div>
       <div className = "NavigationBar">

        <h1>Libary</h1>
        <nav className = "navigationLinks">
          
          <Link to="/LibaryHomePage" className = "individualElem">HomePage</Link>
          <Link to="/UserBooks" className = "individualElem">User Books</Link>
          <Link to="/UpdateDetails" className = "individualElem">Update Details</Link>
        </nav>
      </div>
      {/*Main Body*/}
      <div>
        
        
        <form className='textForm'>
          <h1>Reset Password</h1>
          <label>Comfirm Password</label>
          <br />
          <input type='text' value = {passwordConfirm_First}  onChange={PasswordFirstFunc}></input>
           <br />
          <label>Input New Password</label>
           <br />
         <input type='text' value = {newPassword}  onChange={newPasswordFunc}></input>
          <br />
          <br />
          <button type = "button" className = "buttonPass" onClick={() => PasswordChange()}>Button</button>
          
        </form>

      </div>
        
      


    </div>
  );
}

export default UpdateDetails;