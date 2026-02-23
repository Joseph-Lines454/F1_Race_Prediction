
import './App.css'
import ReactDOM from "react-dom/client"
import F1_DriverStandings from "./F1_DriverStandings.js"
import F1_Prediction from './F1_Prediction.js'


import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  console.log("Here in app!")
  return (

    


    <BrowserRouter>
      <div className = "NavigationBar">

        <h1>F1 Race Prediction</h1>
        <nav className = "navigationLinks">
          <Link to="/" className = "individualElem">F1 Prediction</Link>
          <Link to="/F1_DriverStandings" className = "individualElem">F1 Standings</Link>
         
        </nav>
      </div>
     
      <Routes>
        <Route path="/" element={<F1_Prediction />} />
        <Route path="/F1_Prediction" element={<F1_Prediction />} />
        <Route path="/F1_DriverStandings" element={<F1_DriverStandings />} />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;
