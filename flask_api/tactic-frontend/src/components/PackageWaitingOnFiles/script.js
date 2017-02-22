/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'PackageWaitingOnFiles',
  props: ['packageCode'],
  data () {
    return {
      waitingFileFlows: []
    }
  },
  methods: {
    loadData: function () {
      let self = this

      axios.get('/api/v1/package/' + self.packageCode + '/waiting-files', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.waitingFileFlows = response.data.file_flows
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadData()
  },
  computed: {
    numberOfWaitingFiles: function () {
      return this.waitingFileFlows.length
    }
  }
}
