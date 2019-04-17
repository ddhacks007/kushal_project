import React, {Component} from 'react'
import { Menu, Container, Dropdown, DropdownDivider } from 'semantic-ui-react'
import {get} from 'axios'
import _ from 'lodash'
import { Route , withRouter} from 'react-router-dom';
import { Link } from 'react-router-dom'
import DisplayCategories from './displayCategories';

class Home extends Component{
    constructor(props){
        super(props)
        this.state = {categories : []}    
    }
    
    componentDidMount = () => {
        this.fetchTotalCategories()
    }
    
    fetchTotalCategories = () =>{
        get('http://0.0.0.0:5000/categories').then(res => this.setState({categories: res.data['list_of_categories']})).catch(err => console.log(err))
    }

    render(){
        if(_.isEmpty(this.state.categories)) return null
        return(
        <Menu fixed='top' inverted>
          <Container>
            <Menu.Item as='a' header onClick = {()=>{this.props.history.push('/')}}>{'The EYE'}</Menu.Item>
            <Menu.Item onClick = {() => {this.props.history.push("/upload")}}>{'Upload'}</Menu.Item>
            <Dropdown item simple text='Categories' >
              <Dropdown.Menu>
               {
                   _.map(this.state.categories, (category)=>
                    <Dropdown.Item onClick = {() => {this.props.history.push(`/category/type:${category}/pages:${1}`)}}>{category}</Dropdown.Item>          
                   )
               }
              </Dropdown.Menu>
            </Dropdown>
          </Container>
        </Menu>
        )
    }
}
export default withRouter(Home)