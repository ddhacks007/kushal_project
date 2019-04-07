import React, { Component } from "react"
import _ from "lodash"
import { get } from 'axios'
class DisplayRecommendations extends Component {
    constructor(props) {
        super(props)
        this.state = { source: this.props.location.state.data.source, recommendations_url: this.props.location.state.data.recommendations_url, s3_url: 'https://s3.ap-south-1.amazonaws.com/kushal-jewels/' }
        console.log(this.state)
    }

    recommendation_graph = () => {
        var keys = Object.keys(this.state.recommendations_url)
        var l = []
        for (var i = 0; i < keys.length; i++) {
            l.push(<h1>{keys[i]}</h1>)
        }
        return (l)
    }
    render() {
        return (
            <div>
                <h1 style={{ textAlign: "center", fontFamily: "courier" }}>Requested Image</h1>
                <img src={this.state.source} style={{ display: "block", marginLeft: "auto", marginRight: "auto", width: "15%" }} />
                {
                    Object.keys(this.state.recommendations_url).map(category_name => {
                        return (
                            <div>
                                <h1 style={{ fontFamily: "courier", textAlign: "center" }}>{category_name}</h1>
                                {
                                    this.state.recommendations_url[category_name].map(item => {
                                        return (<img src={this.state.s3_url + item} style={{ padding: "10px", marginLeft: "30px" }} height={"260"} width={"240"} onClick={() => {
                                            get('http://0.0.0.0:5000/retrieve/' + (this.state.s3_url + item).split('/').join('@')).then(response => { if (response['data']['recommendations_url'] != 'failed') { this.setState({ 'recommendations_url': response['data']['recommendations_url'][0] }, () => { this.setState({ source: this.state.s3_url + item }) }, () => { this.props.history.push({ pathname: '/displayRecommendations', state: { data: this.state } }) }) } })
                                        }} />)
                                    })
                                }
                            </div>
                        )
                    })
                }
            </div>)
    }
}
export default DisplayRecommendations;