import React, { Component } from 'react';
import './App.css';
import { HashRouter as Router, Route, Switch } from "react-router-dom";
import upload from './components/upload'
import { Menu, Container, Icon } from "semantic-ui-react"
import DisplayRecommendations from './components/displayRecommendations'
class App extends Component {
  render() {
    return (
      <div>
        <Menu fixed='top' inverted>
          <Container>
            <Menu.Item as='a' header>{'The EYE'}</Menu.Item>
          </Container>
        </Menu>
        <div style={{ marginTop: '5rem' }}>
          <Router>
            <Switch>
              <Route path="/upload" component={upload} />
              <Route path="/displayRecommendations" component={DisplayRecommendations} />
            </Switch>
          </Router>
        </div>
      </div>
    );
  }
}

export default App;
