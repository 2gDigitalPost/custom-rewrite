import Search from 'react-search'
import ReactDOM from 'react-dom'
import React, { Component, PropTypes } from 'react'
 
class TestComponent extends Component {
 
  HiItems(items) {
    console.log(items)
  }

  constructor (props) {
    super(props);
    this.state = { repos: [] }
  }

  getItemsAsync(searchValue, cb) {
    let ticket_div = document.getElementById('ticket');
    let ticket = ticket_div.dataset.ticket;

    let url = `/titles/` + ticket;

    fetch(url).then( (response) => {
      return response.json();
    }).then((results) => {
      if(results.titles != undefined){
        let items = results.titles.map( (res, i) => { return { id: i, value: res.name } });
        this.setState({ repos: items });
        cb(searchValue)
      }
    });
  }

  render () {
    return (
      <div>
        <Search items={this.state.repos}
                getItemsAsync={this.getItemsAsync.bind(this)}
                onItemsChanged={this.HiItems.bind(this)} />
      </div>
    )
  }
}
 
ReactDOM.render( <TestComponent />, document.getElementById('root'));