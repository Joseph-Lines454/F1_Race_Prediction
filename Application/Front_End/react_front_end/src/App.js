
import './App.css'
import ReactDOM from "react-dom/client"
import F1_DriverStandings from "./F1_DriverStandings.js"
import F1_Prediction from './F1_Prediction.js'
import Historical from './historical.js'
import F1_Live_Timings from "./F1_Live_Timings.js"
import { BrowserRouter, Routes, Route, Link,  useLocation } from 'react-router-dom';
import F1_ShowRaceResults from './F1_ShowRaceResults.js'
import RegisterUser from "./Register.js"
import LoginUser from "./Login.js"



function App(){
  return(
    <BrowserRouter>
    < RenderNav />
  </BrowserRouter>
  );
  
}


function RenderNav() {
  console.log("Here in app!")
  const location = useLocation();
  const hidePaths = ["/LoginUser","/RegisterUser"];
  const showNav = !hidePaths.includes(location.pathname)
  return (

    
    
    <>
    {showNav && (
    
      <div className = "NavigationBar">

        <h1>F1 Race Prediction</h1>
        <nav className = "navigationLinks">
          <Link to="/" className = "individualElem">F1 Prediction</Link>
          <Link to="/F1_DriverStandings" className = "individualElem">F1 Standings</Link>
          <Link to ="/historical" className = "individualElem">Historical</Link>
          <Link to = "/F1_Live_Timings" className="individualElem">Live Timings</Link>
          <Link to = "/F1_Live_Timings" className="individualElem">Live Timings</Link>
          
        </nav>
      </div>
      )}
      <Routes>
        <Route path="/" element={<F1_Prediction />} />
        <Route path="/F1_Prediction" element={<F1_Prediction />} />
        <Route path="/F1_DriverStandings" element={<F1_DriverStandings />} />
        <Route path="/historical" element={<Historical />} />
        <Route path = "/F1_Live_Timings" element={<F1_Live_Timings />} />
        <Route path = "/F1_ShowRaceResults" element={<F1_ShowRaceResults/>} />
        <Route path = "/LoginUser" element={<LoginUser/>} />
         <Route path = "/RegisterUser" element={<RegisterUser/>} />
      </Routes>
  
   
    
    </>
  );
}

export default App;
