import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';
import PresseventList from './components/PresseventList'



function App() {


  const [pressevents, setPressevents] = useState([])

  useEffect(() => {
    fetch('https://telexi.seawolfsoftware.io/api/v1', {
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


      <PresseventList pressevents={pressevents}/>


    </div>
  );
}

export default App;
