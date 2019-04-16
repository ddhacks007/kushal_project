import React, {Component} from 'react'

class DisplayCategories extends Component{
    constructor(props){
        super(props)
        this.state = {category: this.props.match.params['0'], pages: this.props.match.params['1']}
    }
    componentDidMount(){
        
    }
    componentWillReceiveProps(props){
        if(this.state.category!=props.match.params['0']||this.state.pages!=props.match.params['1'])
        this.setState({category:props.match.params['0']}) 
    }
    render(){
        return(
            <h1>{this.state.category}{"and the page number is "}{this.state.pages}</h1>
        )
    }
}
export default DisplayCategories