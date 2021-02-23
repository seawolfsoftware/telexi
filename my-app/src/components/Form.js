import React, {useState, useEffect} from 'react';
import APIService from '../APIService';



function Form(props) {


    const [device_id, setDeviceID] = useState(props.pressevent.device_id)
    const [is_button_on, setIsButtonOn] = useState(props.pressevent.is_button_on)
    const [created_at, setCreatedAt] = useState(props.pressevent.created_at)


    useEffect(() => {
        setDeviceID(props.pressevent.device_id)
        setIsButtonOn(props.pressevent.is_button_on)
        setCreatedAt(props.pressevent.created_at)
    }, [props.pressevent])

    const updatePressevent = () => {
        APIService.UpdatePressevent(props.pressevent.id, {device_id, is_button_on, created_at})
        .then(resp => props.updatedInformation(resp))

    }

    const insertPressevent = () => {
        APIService.InsertPressevent({device_id, is_button_on, created_at})
        .then(resp => props.insertedInformation(resp))
    }



    return (


        <div>

            {props.pressevent ? (
                <div className="mb-3">

                    <label htmlFor="device_id"
                            className="form-label">Device ID</label>
                    <input type="text"
                            className="form-control"
                            id="device_id"
                            placeholder="Enter the device ID"
                            value={device_id}
                            onChange={e => setDeviceID(e.target.value)}/>


                    <label htmlFor="is_button_on"
                            className="form-label">Button state</label>
                    <input type="radio"
                            className="form-control"
                            id="is_button_on"
                            placeholder="Button state (ON / OFF)"
                            value={is_button_on}
                            onChange={e => setIsButtonOn(e.target.value)}/>



                    <label htmlFor="created_at"
                            className="form-label">Created at</label>
                    <input type="datetime"
                            className="form-control"
                            id="created_at"
                            placeholder="Enter date and timestamp"
                            value={created_at}
                            onChange={e => setCreatedAt(e.target.value)}/>

                    <br/>

                    {
                        props.pressevent.id ? <button onClick={updatePressevent} className="btn btn-success">Update Press Event</button>
                        : <button onClick={insertPressevent} className="btn btn-success">Insert Press Event</button>
                    }


                    <br/>
                    <br/>

                </div>
            ) : null}

        </div>
    )
}

export default Form
