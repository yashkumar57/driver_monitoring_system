function Dashboard({ stats, latestAlert }) {

  return (

    <>
      <h1 className="title">
        Driver Monitoring System
      </h1>

      <div className="card-container">

        <div className="card">

          <h2>Total Alerts</h2>

          <h1>{stats?.total_alerts}</h1>

        </div>

        <div className="card">

          <h2>Drowsy Alerts</h2>

          <h1>{stats?.drowsy_alerts}</h1>

        </div>

      </div>

      {latestAlert && (

        <div className="latest-alert">

          <h2>Latest Alert</h2>

          <p>
            <strong>Status:</strong> {latestAlert.status}
          </p>

          <p>
            <strong>Time:</strong> {latestAlert.timestamp}
          </p>

          <img
            src={`http://127.0.0.1:8000/${latestAlert.screenshot.replace("../", "")}`}
            alt="alert"
            className="alert-image"
          />

        </div>
      )}
    </>
  )
}

export default Dashboard