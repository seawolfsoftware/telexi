import React from 'react'



function PresseventList(props) {


    const editButton = (pressevent) => {
        props.editButton(pressevent)
    }


    return (

        <div>
          <table>
            <tr>
              <th>Event ID</th>
              <th>Device ID</th>
              <th>Button state</th>
              <th>Created at</th>
              <th></th>
            </tr>

            {props.pressevents && props.pressevents.map(pressevent => {
            return (

                <tr>
                    <td>{pressevent.id}</td>
                    <td>{pressevent.device_id}</td>
                    <td>{pressevent.is_button_on.toString()}</td>
                    <td>{pressevent.created_at}</td>
                    <div className="row">
                        <div className="col-md-1">
                            <button onClick={() => editButton(pressevent)} className="btn btn-primary">Update</button>
                        </div>
                        <div className="col">
                            <button className="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </tr>


            )
          })}

        </table>
        </div>
    )
}

export default PresseventList
