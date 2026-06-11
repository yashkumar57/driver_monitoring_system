function Alerts({ alerts }) {

  return (

    <div className="table-section">

      <h2 className="table-title">
        Alert History
      </h2>

      <table className="alerts-table">

        <thead>

          <tr>

            <th>ID</th>

            <th>Time</th>

            <th>Status</th>

            <th>Screenshot</th>

          </tr>

        </thead>

        <tbody>

          {alerts.map((alert) => (

            <tr key={alert.id}>

              <td>{alert.id}</td>

              <td>{alert.timestamp}</td>

              <td>{alert.status}</td>

              <td>{alert.screenshot}</td>

            </tr>
          ))}

        </tbody>

      </table>

    </div>
  )
}

export default Alerts