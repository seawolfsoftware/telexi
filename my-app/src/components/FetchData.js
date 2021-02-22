import React, {useState, useEffect} from 'react'
import axios from 'axios';



function FetchData() {


    const [pressevents, setPressevents] = useState([])

    useEffect(() => {

        // axios.get('https://jsonplaceholder.typicode.com/posts')
        axios.get('http://telexi.seawolfsoftware.io/api/v1')
        .then(resp => {
            console.log(resp.data)
            setPressevents(resp.data)
        })
        .catch(error => console.log(error))
    }, [])



    return (
        <div>
            {pressevents.map(pressevent =>

                <h3 key={pressevent.id}>{pressevent.title}</h3>

            )}
        </div>
    )
}

export default FetchData
