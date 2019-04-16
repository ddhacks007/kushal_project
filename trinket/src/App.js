import React, { Component } from 'react';
import './App.css';
import { HashRouter , Route, Switch } from "react-router-dom";
import Home from "./components/home"
import upload from './components/upload'
import DisplayRecommendations from './components/displayRecommendations'
import DisplayCategories from './components/displayCategories'
class App extends Component {


  render() {
    return (
      <div>
        <HashRouter>
       <Home/>
        <div style={{ marginTop: '5rem' }}>
            <Switch>
              <Route path="/upload" component={upload} />
              <Route path="/displayRecommendations" component={DisplayRecommendations} />
              <Route path='/category/type:*/pages:*' component = {DisplayCategories} />
            </Switch>
        </div>
        </HashRouter>
      </div>
    );
  }
}

export default App;
