import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';
import PresseventList from './components/PresseventList';
import Form from './components/Form';


function App() {


  const [pressevents, setPressevents] = useState([])
  const [editPressevent, setEditPressevent] = useState(null)

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



  const editButton = (pressevent) => {
    setEditPressevent(pressevent)
  }



  return (
    <div className="App">

      <h3>telexi dashboard</h3>


      <PresseventList pressevents={pressevents} editButton={editButton} />
      <Form pressevent={editPressevent}/>

    </div>
  );
}

export default App;
