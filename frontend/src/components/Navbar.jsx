import { Link } from "react-router-dom"

function Navbar() {

  return (

    <nav className="navbar">

      <h1 className="logo">
        Driver Monitor
      </h1>

      <div className="nav-links">

        <Link to="/">Dashboard</Link>

        <Link to="/alerts">Alerts</Link>

      </div>

    </nav>
  )
}

export default Navbar