/* globals localStorage */

import axios from 'axios'

function get_year_options() {
  let current_year = new Date().getFullYear();
  let years = [];

  for (let year_iterator = current_year; year_iterator >= 1888; year_iterator--) {
    years.push(year_iterator);
  }

  return years;
}

export default {
  name: 'AddTitleManually',
  data () {
    return {
      title_name: null,
      title_type: null,
      year: null,
      year_options: get_year_options()
    }
  },
  methods: {
    addTitleToTactic: function() {
      var self = this

      axios.post('http://localhost:5000/api/v1/titles', 
        JSON.stringify({
          'name': self.title_name,
          'type': self.title_type,
          'year': self.year
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            self.$router.go(self.$router.currentRoute)
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}