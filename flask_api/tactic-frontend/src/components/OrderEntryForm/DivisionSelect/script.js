/* globals localStorage */

import axios from 'axios'

export default {
  name: 'DivisionSelect',
  props: ['client'],
  data () {
    return {
      selected_division: '',
      division_options: []
    }
  },
  methods: {
    loadDivisions: function () {
      var self = this

      // Clear out the division options, in case the client code changed
      self.division_options = []

      // Get the divisions from the api, using the client code in the URL
      axios.get('http://localhost:5000/api/v1/divisions/' + self.client, {
        params: {
          token: localStorage.tactic_token,
        }
      })
      .then(function (response) {
        console.log(response)
        let divisionData = response.data.divisions

        for (let i = 0; i < divisionData.length; i++) {
          self.division_options.push({text: divisionData[i].name, value: divisionData[i].code})
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  watch: {
    client: function () {
      this.loadDivisions()
    }
  },
  beforeMount: function () {
    this.loadDivisions()
  }
}