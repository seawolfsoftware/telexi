import React from 'react'



function PresseventList(props) {

    return (

        <div>
          <table>
            <tr>
              <th>Event ID</th>
              <th>Device ID</th>
              <th>Button state</th>
              <th>Created at</th>
            </tr>

            {props.pressevents && props.pressevents.map(pressevent => {
            return (
                  <tr>
                    <td>{pressevent.id}</td>
                    <td>{pressevent.device_id}</td>
                    <td>{pressevent.is_button_on.toString()}</td>
                    <td>{pressevent.created_at}</td>
                  </tr>

            )
          })}
        </table>
        </div>
    )
}

export default PresseventList
