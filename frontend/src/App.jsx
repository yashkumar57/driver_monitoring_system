import { useEffect, useState } from "react"
import "./App.css"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Alerts from "./pages/Alerts"
function App() {
  const [stats, setStats] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [latestAlert, setLatestAlert] = useState(null)
  useEffect(() => {
    fetch("http://127.0.0.1:8000/stats")
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setStats(data)
      })
    fetch("http://127.0.0.1:8000/alerts")
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setAlerts(data)
      })
    fetch("http://127.0.0.1:8000/latest")
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