import React, {Component} from 'react'

export class Counter extends Component {

    constructor(props) {
        super(props)

        this.state = {
             count: 0
        }
    }

    clickME = () => {
        this.setState({
            count:this.state.count +1
        })
    }

    render() {
        return (
            <div>

                <h2>{this.state.count}</h2>


                <button onClick={this.clickME} className="btn btn-success">Submit</button>
            </div>
        )
    }
}

export default Counter
