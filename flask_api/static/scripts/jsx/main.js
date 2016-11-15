import Search from 'react-search'
import ReactDOM from 'react-dom'
import React, { Component, PropTypes } from 'react'
 
class TestComponent extends Component {
 
  HiItems(items) {
    console.log(items)
  }

  constructor (props) {
    super(props)
    this.state = { repos: [] }
  }

  getItemsAsync(searchValue, cb) {
    // let url = `https://api.github.com/search/repositories?q=${searchValue}&language=javascript`

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
                multiple={true}
                getItemsAsync={this.getItemsAsync.bind(this)}
                onItemsChanged={this.HiItems.bind(this)} />
      </div>
    )
  }
  /*
  render () {
    let items = [
      { id: 0, value: 'ruby' },
      { id: 1, value: 'javascript' },
      { id: 2, value: 'lua' },
      { id: 3, value: 'go' },
      { id: 4, value: 'julia' }
    ];
 
    return (
      <div>
        <Search items={items} />
 
        <Search items={items}
                placeholder='Pick your language'
                maxSelected={3}
                multiple={true}
                onItemsChanged={this.HiItems.bind(this)} />
      </div>
    )
  }
  */
}
 
ReactDOM.render( <TestComponent />, document.getElementById('root'));