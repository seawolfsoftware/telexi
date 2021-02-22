import React, {Component} from 'react'

class Form extends Component {


    constructor(props) {
        super(props)

        this.state = {
             username: '',
             password: ''
        }
    }


    componentDidMount() {
        fetch('https://jsonplaceholder.typicode.com/posts')
        .then(response => response.json())
        .then(data => console.log({posts:data}))
    }


    usernameHandler = (event) => {
        this.setState({
            username:event.target.value
        })
    }


    passwordHandler = (event) => {
        this.setState({
            password:event.target.value
        })
    }



    render() {

        const {posts} = this.state



        return (
            <div className="container">
                <input type="text"
                       value={this.state.username}
                       placeholder="Enter username"
                       className="form-control"
                       onChange={this.usernameHandler}
                       />
                <input type="password"
                       value={this.state.password}
                       placeholder="Enter password"
                       className="form-control"
                       onChange={this.passwordHandler}
                       />

                <button className="btn btn-primary">Submit</button>








            </div>
        )
    }
}

export default Form
