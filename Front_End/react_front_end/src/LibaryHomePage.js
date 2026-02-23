import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import { use, useEffect, useState } from 'react';
import {BrowserRouter, Routes, Route, Link, useNavigate} from 'react-router-dom'


//Send some JSON here

const paramsSend = {
  withCredentials: true,
}

const socket = io.connect("http://localhost:82/" || "",paramsSend)


//socket.emit("GetLibaryData","Data");
//socket.emit("GetLibaryData","Data");
socket.emit("GetLibaryData","Data");
function LibaryHomePage() {
  const [itemDataIn, itemData] = useState(null);
  const navigate = useNavigate();

  

 
  useEffect(() => {
    socket.emit("GetLibaryData","Data");
    socket.on("GetLibaryDataClient", function(msg){
     
      itemData(msg);
      console.log(msg);
      console.log("We have returned here!aaaa");
      
    }) 
   
  }, []);

  function ReserveBook(ISBN)
  {
  //sending ISBN of book as well as cookie
    console.log(ISBN);
    socket.emit("ReserveBook",ISBN)
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
        <h1>Books available</h1>
        <div className = "Bookscontainer">
          {itemDataIn != null && itemDataIn != "No_Cookie" && itemDataIn.map((data) => {
            return(
                <div className='Books'  key = {data["_id"]}  onClick={() => ReserveBook(data.ISBN)}>
                    
                    <p>Book: {data["Book-Title"]}</p>
                    
                    <img className='image' src = {data["Image-URL-L"]} />
                    <p>Author: {data["Book-Author"]}</p>
                    <button onClick={() => ReserveBook(data.ISBN)}>Reserve Book</button>
                    
                </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default LibaryHomePage;