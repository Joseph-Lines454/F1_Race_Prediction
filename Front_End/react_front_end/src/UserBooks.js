import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import {BrowserRouter, Routes, Route, Link, useNavigate} from 'react-router-dom'


//Send some JSON here

const paramsSend = {
  withCredentials: true,
}




function UserBooks() {
  const [itemDataIn, itemData] = useState(null);  
  const navigate = useNavigate();

  

   useEffect(() => {
        fetch("http://localhost:82/GetUserBooks", {
      method: 'GET',
      credentials: 'include',
      withCredentials: true,
      cache: "no-store",
      headers: {
        'Content-Type': "application/json",
        'Access-Control-Allow-Credentials': 'true'
      },
      
      
    }).then(res =>{ if (res.status == 200) {res.json() .then(json => itemData(json))}})

    }, []);
   
    //itemData( res.json());
    //console.log(await res.json());
    //console.log(await res.body);
   
    
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
        <h1>Your Books</h1>
        <div className = "Bookscontainer">
          {itemDataIn != null && itemDataIn.map((data) => {
            return(
                <div className='Books'  key = {data["_id"]}>
                  <p>Book: {data["Book-Title"]}</p>
                    
                    <img className='image' src = {data["Image-URL-L"]} />
                    <p>Author: {data["Book-Author"]}</p>
                    
                    
                    
                  
                </div>
            );
          })}
        </div>
      </div>
        
      


    </div>
  );
}

export default UserBooks;