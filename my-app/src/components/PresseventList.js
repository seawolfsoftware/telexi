import React from 'react';
import APIService from '../APIService';


function PresseventList(props) {


    const editButton = (pressevent) => {
        props.editButton(pressevent)
    }

    const deleteButton = (pressevent) => {
        APIService.DeletePressevent(pressevent.id)
        .then(() => props.deleteButton(pressevent))
        .catch(error => console.log(error))

    }


    return (

        <div>



        {props.pressevents && props.pressevents.map(pressevent => {
          return (
            <div key = {pressevent.id}>
            <h4>{pressevent.device_id}</h4>
            <h4>{pressevent.is_button_on.toString()}</h4>
            <h4>{pressevent.created_at}</h4>

          <div className = "row">
          <div className = "col-md-1">
          <button className = "btn btn-primary" onClick  = {() => editButton(pressevent)}>Update</button>
          </div>

          <div className = "col">
            <button onClick={() => deleteButton(pressevent)} className = "btn btn-danger">Delete</button>
          </div>


          </div>

          <hr className = "hrclass"/>
          </div>
          )
        })}





        </div>

    )
}

export default PresseventList

