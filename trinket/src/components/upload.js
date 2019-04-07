import React, { Component } from 'react';
import axios, { post } from 'axios';

class Upload extends Component {
    constructor(props) {
        super(props)
        this.state = { source: "hidden" }
    }
    onChange = (e) => {
        let files = e.target.files;
        const url = "http://0.0.0.0:5000/upload"
        const formData = new FormData()
        this.setState({ "source": URL.createObjectURL(files[0]) })
        formData.append('file', files[0])
        formData.append('shop_name', 'GRT')
        formData.append('file_type', 'jpeg')
        post(url, formData).then(response => { if (response['data']['recommendations_url'] != 'failed') { this.setState({ 'recommendations_url': response['data']['recommendations_url'][0] }); this.props.history.push({ pathname: '/displayRecommendations', state: { data: this.state } }) } })
    }
    render() {
        return (
            <div>
                <input type="file" name="file" style={{ padding: "50px", textAlign: "center" }} onChange={(e) => this.onChange(e)} />
            </div>
        )
    }
}
export default Upload