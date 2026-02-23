import LoginUser from './Login'
import RegisterUser from './Register'
import LibaryHomePage from './LibaryHomePage'
import UserBooks from './UserBooks'
import UpdateDetails from './UpdateDetails';
import {BrowserRouter, Routes, Route, Link, useLocation} from 'react-router-dom'

function App() {
  
    
  return (
    <BrowserRouter>
    
      

      <Routes>
        <Route path="/" element={<LoginUser />} />
        <Route path="/Login" element={<LoginUser />} />
        <Route path="/Register" element={<RegisterUser />} />
        <Route path="/LibaryHomePage" element={<LibaryHomePage />} />
        <Route path="/UserBooks" element={<UserBooks />} />
        <Route path="/UpdateDetails" element={<UpdateDetails />} />
      </Routes>
    </BrowserRouter>
   
    
  );
}

export default App;

