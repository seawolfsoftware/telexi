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

  const updatedInformation= (pressevent) => {
      const new_pressevent = pressevents.map(mypressevent => {
        if(mypressevent.id == pressevent.id){
          return pressevent;
        }
        else{
          return mypressevent;
        }
      })

      setPressevents(new_pressevent)
  }


  const presseventForm= () => {
    setEditPressevent({device_id: '', is_button_on: true, created_at: ''})
  }


  return (
    <div className="App">

    <div className="row">
      <div className="col">
        <h3>telexi stream</h3>
        <br/>
      </div>

      <div className="col">
        <button onClick={presseventForm} className="btn btn-primary">Insert Press Event</button>
      </div>


    </div>


      <PresseventList pressevents={pressevents} editButton={editButton} />

      {editPressevent ? <Form pressevent={editPressevent} updatedInformation = {updatedInformation}/> : null}


    </div>
  );
}

export default App;
