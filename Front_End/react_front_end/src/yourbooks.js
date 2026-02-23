import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom'

function LibaryHomePage() {
   
  


 
  
  //Get socket stuff working here
  //Get sockets broadcasting aswell
  

  
  return (
    
    <div>
       <div className = "NavigationBar">

        <h1>Libary</h1>
        <nav className = "navigationLinks">
          <Link to="/" className = "individualElem">Login</Link>
          <Link to="/Register" className = "individualElem">Register</Link>
          <Link to="/LibaryHomePage" className = "individualElem">HomePage</Link>
        </nav>
      </div>
      {/*Main Body*/}
      <div>
        <h1>Books available</h1>
      </div>



    </div>
  );
}

export default LibaryHomePage;