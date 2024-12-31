import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Register from "./components/Register/Register";
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer"

function App() {
  return (
    <Routes>
        <Route path="/dealer/:id" element={<Dealer/>} />
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/register" element={<Register />} />  
        <Route path="/dealers" element={<Dealers/>} />
    </Routes>
  );
}
export default App;
