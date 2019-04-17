import React, {Component} from 'react'
import {get} from 'axios'
import { Pagination } from 'semantic-ui-react'
import _ from "lodash"

class DisplayCategories extends Component{
    constructor(props){
        super(props)
        this.state = {category: this.props.match.params['0'], pages: this.props.match.params['1'], image_urls:[], total_pages:"", recommendations_url:[], source:""}
    }
    componentDidMount(){
        get('http://0.0.0.0:5000/category/fetch/'.concat(this.state.category).concat('/').concat(this.state.pages)).then(res => this.setState({image_urls:res.data['image_urls']},() => {this.setState({total_pages:res.data['pages']})})).catch(err => console.log(err))
    }
    componentWillReceiveProps(props){
        console.log(props.match.params['1'])
        if(this.state.category!=props.match.params['0']||this.state.pages!=props.match.params['1'])
            this.setState({category:props.match.params['0']}, ()=>{this.setState({pages:props.match.params['1']}, () => {this.componentDidMount()})}) 
    }

    image_display = () =>{
        return (_.map(this.state.image_urls, (values)=>
        <img src={values} style={{ padding: "10px", marginLeft: "30px" }} height={"260"} width={"240"}  onClick={() => {
            get('http://0.0.0.0:5000/retrieve/' + (values).split('/').join('@')).then(response => { if (response['data']['recommendations_url'] != 'failed') { this.setState({ 'recommendations_url': response['data']['recommendations_url'][0] }); this.setState({ source: values } , () => {   this.props.history.push({ pathname: '/displayRecommendations', state: { data: this.state } })      }) } })
        }}/>
        ) 
        )
    }
    page_selected = (event, {activePage}) =>{
        this.props.history.push(`/category/type:${this.state.category}/pages:${(activePage.toString())}`)
    }

    render(){
        return(
            <div>
           {this.image_display()}
           <Pagination  defaultActivePage={5} totalPages={this.state.total_pages} style = {{marginLeft : "450px"}} onPageChange = {this.page_selected}/> 
           </div>
        )

    }
}
export default DisplayCategories