/* globals localStorage */

import bus from '../../../bus'

import axios from 'axios'
import Multiselect from 'vue-multiselect'

export default {
  name: 'DivisionSelect',
  props: ['client'],
  components: {
    Multiselect,
  },
  data () {
    return {
      selected_division: null,
      division_options: [],
      loaded: false
    }
  },
  methods: {
    loadDivisions: function () {
      var self = this

      self.loaded = false

      // Clear out the division options, in case the client code changed
      self.division_options = []

      // Get the divisions from the api, using the client code in the URL
      axios.get('/api/v1/divisions/' + self.client, {
        params: {
          token: localStorage.tactic_token,
        }
      })
      .then(function (response) {
        let divisionData = response.data.divisions

        for (let i = 0; i < divisionData.length; i++) {
          self.division_options.push({text: divisionData[i].name, value: divisionData[i].code})
        }

        self.loaded = true
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  watch: {
    client: function () {
      this.loadDivisions()
    },
    selected_division: function () {
      bus.$emit('division-selected', this.selected_division.value)
    }
  },
  beforeMount: function () {
    this.loadDivisions()
  }
}