/* globals localStorage */

import axios from 'axios'

export default {
  name: 'SelectableComponent',
  props: ['component', 'pipeline_code'],
  data () {
    return {
      pipeline: null,
      selected: false
    }
  },
  methods: {
    loadPipeline: function () {
      var self = this

      axios.get('/api/v1/pipelines/code/' + self.pipeline_code, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.pipeline = response.data.pipeline
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadPipeline()
  }
}