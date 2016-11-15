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

function ClientOptions(props) {
  return <option>{props.name}</option>
}

class ClientSelect extends React.Component {

  render() {
    var clients = [
      {
        "name": "sony",
        "divisions": [
            "Sony Division 1",
            "Sony Division 2"
        ]
      },
      {
        "name": "fox",
        "divisions": [
            "Fox Division 1",
            "Fox Division 2"
        ]
      }
    ];

    return (
      <div>
        <select>
          {clients.map(ClientOptions)}
        </select>
      </div>
    )
  }
}

ReactDOM.render(<ClientSelect />, document.getElementById('client_select'));
 
ReactDOM.render( <TestComponent />, document.getElementById('root'));