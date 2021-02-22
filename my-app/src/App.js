import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';



function App() {


  const [pressevents, setPressevents] = useState([])

  useEffect(() => {
    fetch('http://telexi.seawolfsoftware.io/api/v1', {
      'method': 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  .then(resp => resp.json())
  .then(resp => setPressevents(resp))
  .catch(error => console.log(error))

  }, [])


  return (
    <div className="App">

      <h3>telexi dashboard</h3>


      <table>
        <tr>
          <th>Event ID</th>
          <th>Device ID</th>
          <th>Button state</th>
          <th>Created at</th>
        </tr>
      </table>

      {pressevents.map(pressevent => {
        return (
              <tr>
                <td>{pressevent.id}</td>
                <td>{pressevent.device_id}</td>
                <td>{pressevent.is_button_on.toString()}</td>
                <td>{pressevent.created_at}</td>
              </tr>

        )
      })}



    </div>
  );
}

export default App;
