/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../../bus'

import FileFlowEditable from '../../FileFlowEditableList/FileFlowEditable/index.vue'

export default {
  name: 'FileFlowInTaskList',
  props: ['component'],
  components: {
    FileFlowEditable
  },
  data () {
    return {
      loading: true,
      fileFlows: []
    }
  },
  methods: {
    loadFileFlows: function () {
      let self = this
      self.loading = true

      axios.get('/api/v1/component/' + self.component.code + '/file-flows', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.fileFlows = response.data.file_flows

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadFileFlows()
  }
}