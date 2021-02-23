import React, {useState} from 'react'

function Login() {


    const [username, setUsername] = useState()
    const [password, setPassword] = useState()

    const loginButton = () => {

    }

    return (
        <div className="App">

            <h1>Login</h1>

            <div className="mb-3">
                <label htmlFor="username"
                        className="form-label">Username</label>
                <input type="text"
                        className="form-control"
                        id="username"
                        placeholder="Enter username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}/>
            </div>

            <div className="mb-3">
                <label htmlFor="password"
                        className="form-label">Username</label>
                <input type="password"
                        className="form-control"
                        id="password"
                        placeholder="Enter password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}/>
            </div>


            <button onClick={loginButton} className="btn btn-primary">Login</button>
        </div>
    )
}

export default Login
