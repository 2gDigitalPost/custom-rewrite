/* globals localStorage */

import axios from 'axios'
import DivisionSelect from '../DivisionSelect/index.vue'

export default {
  name: 'ClientSelect',
  components: {
    'division-select': DivisionSelect
  },
  data () {
    return {
      selected_client: '',
      client_options: []
    }
  },
  methods: {
    loadClients: function () {
      var self = this

      axios.get('http://0.0.0.0:5000/api/v1/clients', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let clientData = response.data.clients

        for (let i = 0; i < clientData.length; i++) {
          self.client_options.push({text: clientData[i].name, value: clientData[i].code})
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadClients()
  }
}