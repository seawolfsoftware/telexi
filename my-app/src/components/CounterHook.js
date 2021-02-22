import React, {useState, useEffect} from 'react'

function CounterHook() {

    const [count, setCount] = useState(0)
    const [text, setText] = useState("This is a text")
    const [info, setInfo] = useState({name:'', email:''})
    const [pressevents, setPressevents] = useState(['Press Event One',
        'Press Event Two',
        'Press Event Three'])


    const addPressevent = () => {
        setPressevents([...pressevents, 'New Pres Event'])
    }

    useEffect(() => {
        console.log("use effect is called")
    })

    return (
        <div>
            <h2>{count}</h2>
            <button onClick={() => setCount(count+1)}
                    className="btn btn-primary">Submit</button>

            <h2>{text}</h2>
            <button className="btn btn-success"
                    onClick={() => setText("The text is changed")}>Change Text</button>

            <br/>
            <br/>
            <input type="text"
                    className="form-control"
                    value={info.name}
                    onChange={e => setInfo({...info, name:e.target.value})}/>
            <input type="text"
                    className="form-control"
                    value={info.email}
                    onChange={e => setInfo({...info, email:e.target.value})}/>


            <h2>Name is: {info.name}</h2>
            <h2>Email is: {info.email}</h2>


            {pressevents.map(pressevent => {
                return <h2 key={pressevent}>{pressevent}</h2>
            })}

            <button onClick={addPressevent} className="btn btn-primary">Add Press Event</button>

        </div>
    )
}

export default CounterHook
