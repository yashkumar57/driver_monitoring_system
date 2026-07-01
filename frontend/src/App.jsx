import { useEffect, useState } from "react"
import "./App.css"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Alerts from "./pages/Alerts"
const API = import.meta.env.VITE_API_URL;
function App() {
  const [stats, setStats] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [latestAlert, setLatestAlert] = useState(null)
  useEffect(() => {
    fetch(`${API}/stats`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setStats(data)
      })
    fetch(`${API}/alerts`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setAlerts(data)
      })
    fetch(`${API}/latest`)
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        setLatestAlert(data)
      })
  }, [])
return (

  <BrowserRouter>

    <div className="dashboard">

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={
            <Dashboard
              stats={stats}
              latestAlert={latestAlert}
            />
          }
        />

        <Route
          path="/alerts"
          element={
            <Alerts alerts={alerts} />
          }
        />

      </Routes>

      <Footer />

    </div>

  </BrowserRouter>
)
}
export default App