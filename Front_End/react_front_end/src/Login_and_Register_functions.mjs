import { useEffect, useState } from "react";
import {BrowserRouter, Routes, Route, Link, useNavigate} from 'react-router-dom'
import io from 'socket.io-client';
//Login Function - Getting to the other functions
const paramsSend = {
  withCredentials: true,
}
export async function CheckIfLoginValid(usernameInital,passwordInital,navigate){
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
  if (res.status == 200 && navigate == null)
  {
   return res.status; 
  }
  else if (res.status == 200 && navigate != null)
  {
    navigate("/LibaryHomePage");
    return res.status; 
  }
  else if (res.status == 401)
  {
    alert("Invalid Credentials!");
    return res.status; 
  }
  else if(res.status != 401 && this.status != 200){
    alert("something else went wrong")
    return res.status; 
  }
  
};
//Redesign this for fetch
export function CheckCookies()
{
  const CookiesRequest = new XMLHttpRequest();

    //some code here to deal with the cookies

    CookiesRequest.onload = function()
    {
      if (this.status === 200)
      {
        console.log(this.responseText)
      }
      else if (this.status === 401)
      {
        console.log("invalid credentials")
      }
    }

    CookiesRequest.open("GET", "http://localhost:82/CookiesRequest")
    CookiesRequest.setRequestHeader('Content-Type', "application/json")
    CookiesRequest.setRequestHeader('Access-Control-Allow-Credentials', true)
    CookiesRequest.withCredentials = true;
    CookiesRequest.send()
}

export async function WebSocketLibaryConnect(navigate)
{
  const socket = await io.connect("http://localhost:82/" || "",paramsSend)
  socket.emit("GetLibaryData","Data");

  //const [itemDataIn, itemData] = useState({});
  //const navigate = useNavigate();
  console.log("I am here!!!!!");
  socket.on("GetLibaryDataClient", function(msg){
    console.log(MessageEvent)
    if (msg == "No_Cookie" && navigate != null)
    {
      navigate("/Login");
      console.log(msg);
      return msg;
    }
    else if (msg == "No_Cookie" && navigate == null)
    {
      console.log("here!!!");
      return 200;
    }
    else 
    {
      //itemData(msg)
    }
  }) 
}

export async function CheckReg(usernameInital,passwordInital,emailInital,phonenumberInital,navigate){
  
    const res = await fetch("http://localhost:82/CheckRegistration", {
      method: 'POST',
      credentials: 'include',
      withCredentials: true,
      headers: {
        'Content-Type': "application/json",
        'Access-Control-Allow-Credentials': 'true'
      },
      body: JSON.stringify([{"username" :usernameInital,"password" : passwordInital, "email": emailInital, "phonenumber" : phonenumberInital}])
      
    });
    
    if (res.status == 200 && navigate == null)
    {
        return res.status;       
    }

    else if (res.status == 200 && navigate != null)
    {
        
        navigate("/LibaryHomePage");
        return res.status;
       
    }
    else if (res.status == 401)
    {
      alert("Username/Email/phonenumber already used");
      return res.status;
      
    }
    else{
      alert("Server Error");
      return res.status;
    }
    
  };
